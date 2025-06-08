import os
import time
import threading
import requests
from flask import Flask

# Seu token e repositórios
GH_TOKEN = os.getenv("GH_TOKEN")
HEADERS = {"Authorization": f"Bearer {GH_TOKEN}"}
REPOS = [
    ("luis-tiberio", "piso_exp", "att10.yml"),
    ("luis-tiberio", "piso_exp", "shopee_automation.yml"),
    ("luis-tiberio", "queue_list", "att10.yml"),
    ("luis-tiberio", "queue_list", "queue_list_sp5.yml"),
]

def trigger_workflows():
    for owner, repo, workflow in REPOS:
        url = f"https://api.github.com/repos/{owner}/{repo}/actions/workflows/{workflow}/dispatches"
        print(f"Disparando: {url}")
        res = requests.post(url, headers=HEADERS, json={"ref": "main"})
        print(f"Status: {res.status_code} | {res.text}")
    print("Disparo concluído.")

# Roda periodicamente
def scheduler():
    while True:
        print("⌛ Aguardando 10 minutos...")
        time.sleep(600)
        trigger_workflows()

# Iniciar thread paralela
threading.Thread(target=scheduler, daemon=True).start()

# Criar servidor Flask (obrigatório pro Render aceitar)
app = Flask(__name__)

@app.route('/')
def home():
    return "GitHub Actions Pinger rodando!"

# Rodar servidor (escuta na porta exigida pelo Render)
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
