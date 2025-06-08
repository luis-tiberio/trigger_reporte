from flask import Flask
import requests

app = Flask(__name__)

GITHUB_TOKEN = "ghp_SEU_TOKEN_AQUI"
REPO = "seu-usuario/seu-repo"
WORKFLOW = "queue_list_sp5.yml"
BRANCH = "main"  # ou "master"

def trigger_workflow():
    url = f"https://api.github.com/repos/{REPO}/actions/workflows/{WORKFLOW}/dispatches"
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }
    data = {"ref": BRANCH}
    r = requests.post(url, headers=headers, json=data)
    return r.status_code, r.text

@app.route("/")
def home():
    status, response = trigger_workflow()
    return f"✅ Disparado: {status} - {response}", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
