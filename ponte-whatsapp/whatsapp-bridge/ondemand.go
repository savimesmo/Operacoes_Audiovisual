package main

// ADICIONADO: o historico antigo foi gravado sem o remetente real das mensagens
// de grupo. Ao iniciar, pede ao celular (pedido on-demand, somente leitura) de novo
// as mensagens recentes dos grupos permitidos; o handler de historico regrava
// com o remetente correto.

import (
	"context"
	"fmt"
	"strings"
	"time"

	"go.mau.fi/whatsmeow"
	"go.mau.fi/whatsmeow/types"
	waLog "go.mau.fi/whatsmeow/util/log"
)

func backfillSenders(client *whatsmeow.Client, ms *MessageStore, logger waLog.Logger) {
	time.Sleep(15 * time.Second)
	rows, err := ms.db.Query(`SELECT chat_jid, id, timestamp FROM messages
		WHERE chat_jid LIKE '%@g.us'
		AND sender = substr(chat_jid, 1, instr(chat_jid, '@') - 1)
		AND timestamp >= datetime('now', '-3 days')
		AND is_from_me = 0
		ORDER BY timestamp DESC`)
	if err != nil {
		logger.Warnf("backfill: %v", err)
		return
	}
	type anchor struct {
		chat, id string
		ts       time.Time
	}
	seen := map[string]bool{}
	var list []anchor
	for rows.Next() {
		var a anchor
		if err := rows.Scan(&a.chat, &a.id, &a.ts); err != nil {
			continue
		}
		if !seen[a.chat] {
			seen[a.chat] = true
			list = append(list, a)
		}
	}
	rows.Close()
	for _, a := range list {
		jid, err := types.ParseJID(a.chat)
		if err != nil {
			continue
		}
		info := &types.MessageInfo{
			MessageSource: types.MessageSource{Chat: jid, IsFromMe: false, IsGroup: strings.HasSuffix(a.chat, "@g.us")},
			ID:            a.id,
			Timestamp:     a.ts,
		}
		req := client.BuildHistorySyncRequest(info, 50)
		if _, err := client.SendPeerMessage(context.Background(), req); err != nil {
			logger.Warnf("backfill: %v", err)
		}
		time.Sleep(2 * time.Second)
	}
	fmt.Printf("Pedido de reenvio de historico para %d grupos.\n", len(list))
}
