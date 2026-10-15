package main

// ADICIONADO: pede ao WhatsApp um historico mais completo no pareamento.

import (
	"go.mau.fi/whatsmeow/proto/waCompanionReg"
	"go.mau.fi/whatsmeow/store"
	"google.golang.org/protobuf/proto"
)

func init() {
	store.DeviceProps.RequireFullSync = proto.Bool(true)
	store.DeviceProps.HistorySyncConfig = &waCompanionReg.DeviceProps_HistorySyncConfig{
		FullSyncDaysLimit:   proto.Uint32(90),
		FullSyncSizeMbLimit: proto.Uint32(200),
		StorageQuotaMb:      proto.Uint32(1000),
	}
}
