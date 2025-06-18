from flask import Flask
import threading
import requests
import time
import os

app = Flask(__name__)

TOKEN = os.getenv("GH_TOKEN")
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/vnd.github+json"
}

WORKFLOWS = [
    {"repo": "att_reporte", "workflow": "reporte.yml"},
    {"repo": "backlog", "workflow": "backlog.yml"},
    {"repo": "reportes_sp5", "workflow": "prod-sp5.yml"},
   # {"repo": "piso_exp", "worklow": "piso-playwright.yml"},
]

def trigger_loop():
    while True:
        for wf in WORKFLOWS:
            url = f"https://api.github.com/repos/luis-tiberio/{wf['repo']}/actions/workflows/{wf['workflow']}/dispatches"
            data = {"ref": "main"}
            try:
                res = requests.post(url, headers=HEADERS, json=data)
                print(f"[OK] {wf['workflow']} -> {res.status_code}")
            except Exception as e:
                print(f"[ERRO] {wf['workflow']} -> {e}")
        time.sleep(600)

@app.route('/')
def home():
    return "GitHub Actions Pinger rodando!"

if __name__ == '__main__':
    threading.Thread(target=trigger_loop).start()
    app.run(host="0.0.0.0", port=3000)
