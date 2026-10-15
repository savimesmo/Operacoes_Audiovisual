"""Envia o e-mail do dia com os 3 PDFs em anexo, por SMTP do Gmail.

Precisa do arquivo email_config.json (criado uma vez pela Diana, nunca por Claude):
  {"usuario": "diana.savi@vanguardamartech.com.br", "senha_app": "<senha de app do Google, 16 letras>",
   "para": ["luana.rocha@vanguardamartech.com.br"], "cc": []}
Uso: python enviar_email.py            (envia saida/email.html + 3 PDFs)
     python enviar_email.py --testar   (envia só para o próprio usuário, assunto com [TESTE])
Códigos de saída: 0 enviado, 2 sem configuração, 3 falha no envio.
"""
import json, os, smtplib, ssl, sys
from email.message import EmailMessage

AQUI = os.path.dirname(os.path.abspath(__file__))
SAIDA = os.path.join(AQUI, "saida")
cfg_path = os.path.join(AQUI, "email_config.json")
if not os.path.exists(cfg_path):
    print("SEM_CONFIG: crie email_config.json (veja o início deste arquivo).")
    sys.exit(2)
cfg = json.load(open(cfg_path, encoding="utf-8"))
testar = "--testar" in sys.argv

assunto = open(os.path.join(SAIDA, "assunto.txt"), encoding="utf-8").read().strip()
corpo = open(os.path.join(SAIDA, "email.html"), encoding="utf-8").read()
msg = EmailMessage()
msg["From"] = cfg["usuario"]
msg["To"] = cfg["usuario"] if testar else ", ".join(cfg["para"])
if cfg.get("cc") and not testar:
    msg["Cc"] = ", ".join(cfg["cc"])
msg["Subject"] = ("[TESTE] " if testar else "") + assunto
msg.set_content("Pauta do dia: o resumo está em HTML. Os três PDFs seguem em anexo (início do dia, fim do dia e relatório completo).")
msg.add_alternative(corpo, subtype="html")
for nome in ("1-inicio-do-dia.pdf", "2-fim-do-dia.pdf", "3-relatorio-do-dia.pdf"):
    with open(os.path.join(SAIDA, nome), "rb") as f:
        msg.add_attachment(f.read(), maintype="application", subtype="pdf", filename=nome)
try:
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=ssl.create_default_context(), timeout=60) as s:
        s.login(cfg["usuario"], cfg["senha_app"])
        s.send_message(msg)
except Exception as e:  # sem expor credenciais
    print("FALHA_ENVIO:", type(e).__name__, str(e)[:200])
    sys.exit(3)
print("ENVIADO para", msg["To"])
