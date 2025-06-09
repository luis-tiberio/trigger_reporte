from flask import Flask, request
import requests
import os

app = Flask(__name__)

TOKEN = os.getenv("GH_TOKEN")
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/vnd.github+json"
}

REPO = "att_reporte"           # seu repo com a workflow Reporte HxH
WORKFLOW_FILE = "reporte.yml" # seu arquivo workflow, ex: 'Reporte_HxH.yml' ou 'att10.yml'

@app.route('/trigger', methods=['POST'])
def trigger_workflow():
    ref = request.json.get("ref", "main")  # opcional: branch default main
    url = f"https://api.github.com/repos/luis-tiberio/{REPO}/actions/workflows/{WORKFLOW_FILE}/dispatches"
    payload = {"ref": ref}

    res = requests.post(url, headers=HEADERS, json=payload)
    if res.status_code == 204:
        return {"message": "Workflow disparado com sucesso!"}, 200
    else:
        return {"error": f"Falha ao disparar workflow. Status: {res.status_code}, Resposta: {res.text}"}, 500

@app.route('/')
def home():
    return "API para disparar workflow rodando."

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3000)
