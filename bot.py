import json
from flask import Flask, request
from github_webhook import Webhook  # Simple GitHub Webhook handler

# Flask app and webhook initialization
app = Flask(__name__)
webhook = Webhook(app, secret="my_webhook_secret")  # Keep your secret safe!

# JSON file for storing PR data
JSON_FILE = "prs.json"


@webhook.hook(event_type="pull_request")
def on_pr_event(data):
    """Handle pull request events and update the PR list in prs.json."""
    try:
        action = data.get("action")
        pr_number = data["pull_request"]["number"]
        repo_name = data["repository"]["name"]
    except KeyError as e:
        print(f"KeyError: Missing key in webhook payload - {e}")
        return "Bad Request", 400

    # Load existing PRs from JSON
    try:
        with open(JSON_FILE, "r") as file:
            prs = json.load(file)
    except FileNotFoundError:
        prs = []

    # Handle different PR actions
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
            "status": "open"
        })
    elif action == "closed":
        prs = [pr for pr in prs if pr["id"] != pr_number]

    # Save the updated PR list to JSON
    with open(JSON_FILE, "w") as file:
        json.dump(prs, file, indent=4)

    print(f"PR event handled: {action} for PR #{pr_number}")
    return "OK", 200


if __name__ == "__main__":
    app.run(port=5000, debug=False, use_reloader=False)
