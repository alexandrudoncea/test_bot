import json
from flask import Flask, request
from github_webhook import Webhook
from config import GITHUB_WEBHOOK_SECRET, JSON_FILE_PATH, PORT
from utils import calculate_pr_age

# Flask app and webhook initialization
app = Flask(__name__)
webhook = Webhook(app, secret=GITHUB_WEBHOOK_SECRET)

@webhook.hook(event_type="pull_request")
def on_pr_event(data):
    """Handle pull request events and update the PR list."""
    try:
        action = data.get("action")
        pr_number = data["pull_request"]["number"]
        repo_name = data["repository"]["name"]
    except KeyError as e:
        print(f"KeyError: Missing key in webhook payload - {e}")
        return "Bad Request", 400

    try:
        with open(JSON_FILE_PATH, "r") as file:
            prs = json.load(file)
    except FileNotFoundError:
        prs = []

    if action in ["opened", "review_requested"]:
        prs.append({
            "id": pr_number,
            "title": data["pull_request"].get("title", "Unknown Title"),
            "url": data["pull_request"].get("html_url", "#"),
            "repo": repo_name,
            "author": data["pull_request"].get("user", {}).get("login", "Unknown Author"),
            "created_at": data["pull_request"].get("created_at", "Unknown Date"),
            "last_updated": data["pull_request"].get("updated_at", "Unknown Date"),
            "approvals": 0,
            "status": "open",
            "age": calculate_pr_age(data["pull_request"].get("created_at", "Unknown Date"))
        })
    elif action == "closed":
        prs = [pr for pr in prs if pr["id"] != pr_number]

    with open(JSON_FILE_PATH, "w") as file:
        json.dump(prs, file, indent=4)

    print(f"PR event handled: {action} for PR #{pr_number}")
    return "OK", 200

if __name__ == "__main__":
    app.run(port=PORT, debug=False, use_reloader=False)
