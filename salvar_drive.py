"""Copia os 3 PDFs do dia para o Google Drive (Meu Drive): RELATORIOS/ANO/MÊS/DIA, com a data no nome.
Lê saida/drive_info.json (gerado pelo build_all.py)."""
import json, os, shutil, sys
AQUI = os.path.dirname(os.path.abspath(__file__))
info = json.load(open(os.path.join(AQUI, "saida", "drive_info.json"), encoding="utf-8"))
if not info["pasta"]:
    print("SEM_DRIVE: defina pasta_local em drive.json (pasta RELATÓRIOS da conta diana.savi@vanguardamartech.com.br no Drive para computador).")
    sys.exit(4)
os.makedirs(info["pasta"], exist_ok=True)
filtro = sys.argv[1:]  # opcional: prefixos (1, 2, 3) dos PDFs a salvar
for origem, nome in info["nomes"].items():
    if filtro and origem[0] not in filtro:
        continue
    shutil.copyfile(os.path.join(AQUI, "saida", origem), os.path.join(info["pasta"], nome))
    print("salvo:", os.path.join(info["pasta"], nome))
print("busca:", info["link_busca"])
