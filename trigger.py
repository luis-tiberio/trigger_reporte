from flask import Flask, request
import requests
import os

app = Flask(__name__)

GITHUB_TOKEN = os.environ.get("GH_TOKEN")  # Salvo em variáveis de ambiente do Render
USERNAME = "luis-tiberio"

@app.route("/run", methods=["GET"])
def run_workflow():
    repo = request.args.get("repo")
    workflow = request.args.get("workflow")

    if not repo or not workflow:
        return "Parâmetros ausentes", 400

    url = f"https://api.github.com/repos/{USERNAME}/{repo}/actions/workflows/{workflow}/dispatches"
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {
        "ref": "main"  # Ou a branch que seus workflows estão
    }

    response = requests.post(url, headers=headers, json=data)
    return f"{workflow} acionado: {response.status_code} - {response.text}", response.status_code

@app.route("/")
def root():
    return "Servidor GitHub Actions Pinger está ativo!"
