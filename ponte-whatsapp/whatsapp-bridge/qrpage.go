package main

// ADICIONADO: pagina local (somente 127.0.0.1) que mostra o QR de pareamento
// como imagem preto-no-branco, mais confiavel de escanear que o QR do terminal.
// Nao expoe nenhuma outra funcao e so atende em localhost.

import (
	"fmt"
	"net/http"
	"sync"

	"rsc.io/qr"
)

var (
	qrMu   sync.RWMutex
	qrCode string
)

func setQR(c string) {
	qrMu.Lock()
	qrCode = c
	qrMu.Unlock()
}

const qrHTML = `<!doctype html><meta charset="utf-8"><title>Conectar WhatsApp</title>
<body style="margin:0;background:#fff;color:#111;font:18px system-ui;display:flex;flex-direction:column;align-items:center;justify-content:center;min-height:100vh;gap:16px">
<div id="msg">Escaneie com o WhatsApp Business: Configuracoes, Aparelhos conectados, Conectar um aparelho</div>
<img id="q" width="420" height="420" alt="QR">
<small>O codigo se renova sozinho. Esta pagina so existe no seu computador.</small>
<script>
var img=document.getElementById('q'),msg=document.getElementById('msg');
function tick(){fetch('/qr.png?'+Date.now()).then(function(r){
 if(r.ok){img.style.display='';img.src='/qr.png?'+Date.now();}
 else{img.style.display='none';msg.textContent='Conectado. Pode fechar esta pagina.';}
}).catch(function(){});}
tick();setInterval(tick,3000);
</script></body>`

func startQRPage() {
	mux := http.NewServeMux()
	mux.HandleFunc("/qr.png", func(w http.ResponseWriter, r *http.Request) {
		qrMu.RLock()
		c := qrCode
		qrMu.RUnlock()
		if c == "" {
			http.Error(w, "sem codigo", http.StatusNotFound)
			return
		}
		code, err := qr.Encode(c, qr.M)
		if err != nil {
			http.Error(w, "erro", http.StatusInternalServerError)
			return
		}
		code.Scale = 10
		w.Header().Set("Content-Type", "image/png")
		w.Header().Set("Cache-Control", "no-store")
		w.Write(code.PNG())
	})
	mux.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "text/html; charset=utf-8")
		fmt.Fprint(w, qrHTML)
	})
	go func() {
		if err := http.ListenAndServe("127.0.0.1:8099", mux); err != nil {
			fmt.Printf("Pagina do QR indisponivel: %v\n", err)
		}
	}()
	fmt.Println("Pagina do QR em http://127.0.0.1:8099 (somente neste computador)")
}
