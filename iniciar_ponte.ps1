# Liga a ponte do WhatsApp (somente leitura) em segundo plano, se ainda não estiver rodando.
$dir = "D:\Vibecodas\Claude\whatsapp-mcp\whatsapp-bridge"
if (-not (Get-Process whatsapp-bridge -ErrorAction SilentlyContinue)) {
  Start-Process -FilePath "$dir\whatsapp-bridge.exe" -WorkingDirectory $dir -WindowStyle Hidden -RedirectStandardOutput "$dir\bridge.out.log" -RedirectStandardError "$dir\bridge.err.log"
  Start-Sleep 20
  "ponte iniciada"
} else { "ponte ja estava rodando" }
