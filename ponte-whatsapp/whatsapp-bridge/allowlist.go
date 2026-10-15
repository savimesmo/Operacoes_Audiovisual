package main

// ADICIONADO: lista de permissao de chats. Somente chats listados em
// allowed_chats.txt (um JID por linha, "#" para comentarios) sao guardados.
// Sem o arquivo, NADA e guardado (padrao seguro).

import (
	"bufio"
	"fmt"
	"os"
	"strings"
	"sync"
)

var (
	allowMu   sync.RWMutex
	allowSet  = map[string]bool{}
	allowLoad bool
)

func loadAllowlist() {
	allowMu.Lock()
	defer allowMu.Unlock()
	allowSet = map[string]bool{}
	f, err := os.Open("allowed_chats.txt")
	if err != nil {
		fmt.Println("allowed_chats.txt nao encontrado: nenhuma conversa sera guardada.")
		allowLoad = true
		return
	}
	defer f.Close()
	sc := bufio.NewScanner(f)
	for sc.Scan() {
		line := strings.TrimSpace(sc.Text())
		if i := strings.Index(line, "#"); i >= 0 {
			line = strings.TrimSpace(line[:i])
		}
		if line != "" {
			allowSet[line] = true
		}
	}
	allowLoad = true
	fmt.Printf("Lista de permissao carregada: %d chats.\n", len(allowSet))
}

func chatAllowed(jid string) bool {
	allowMu.RLock()
	loaded := allowLoad
	ok := allowSet[jid]
	allowMu.RUnlock()
	if !loaded {
		loadAllowlist()
		return chatAllowed(jid)
	}
	return ok
}
