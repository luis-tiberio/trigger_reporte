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
WORKFLOW_FILE = "reporte.yml" # nome exato do arquivo .yml

@app.route('/trigger', methods=['POST'])
def trigger_workflow():
    ref = request.json.get("ref", "main")  # padrão: main
    url = f"https://api.github.com/repos/luis-tiberio/{REPO}/actions/workflows/{WORKFLOW_FILE}/dispatches"
    payload = {"ref": ref}

    print(f"[INFO] Disparando workflow '{WORKFLOW_FILE}' no repositório '{REPO}' (ref: {ref})")
    print(f"[DEBUG] Endpoint: {url}")
    print(f"[DEBUG] Payload: {payload}")

    res = requests.post(url, headers=HEADERS, json=payload)

    print(f"[DEBUG] Status Code: {res.status_code}")
    print(f"[DEBUG] Response Text: {res.text}")

    if res.status_code == 204:
        print("[SUCCESS] Workflow disparado com sucesso!")
        return {"message": "Workflow disparado com sucesso!"}, 200
    else:
        print("[ERROR] Falha ao disparar workflow.")
        return {
            "error": "Falha ao disparar workflow.",
            "status_code": res.status_code,
            "response": res.text
        }, 500

@app.route('/')
def home():
    return "API para disparar workflow rodando."

if __name__ == '__main__':
    print("[INFO] Servidor Flask iniciado na porta 3000")
    app.run(host="0.0.0.0", port=3000)
