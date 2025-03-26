import json
from flask import Flask, request
from github_webhook import Webhook  # Simple GitHub Webhook handler

# Flask app and webhook initialization
app = Flask(__name__)
webhook = Webhook(app, secret="my_webhook_secret")  # Keep your secret safe!

# JSON file for storing PR data
JSON_FILE = "prs.json"

@app.route("/webhook", methods=["POST"])
def handle_webhook():
    """Handle incoming GitHub PR events."""
    # Get the event data
    data = request.json
    print("Received webhook data:", json.dumps(data, indent=4))
    # Handle the PR event
    return on_pr_event(data)

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
        print("No existing PRs found, initializing empty list.")

    # Handle different PR actions
    if action in ["opened", "review_requested"]:
        new_pr = {
            "id": pr_number,
            "title": data["pull_request"].get("title", "Unknown Title"),
            "url": data["pull_request"].get("html_url", "#"),
            "repo": repo_name,
            "author": data["pull_request"].get("user", {}).get("login", "Unknown Author"),
            "created_at": data["pull_request"].get("created_at", "Unknown Date"),
            "last_updated": data["pull_request"].get("updated_at", "Unknown Date"),
            "approvals": 0,
            "status": "open"
        }
        prs.append(new_pr)
        print(f"Added new PR: {new_pr}")  # Debugging line

    elif action == "closed":
        prs = [pr for pr in prs if pr["id"] != pr_number]
        print(f"Removed closed PR #{pr_number}")  # Debugging line

    # Save the updated PR list to JSON
    with open(JSON_FILE, "w") as file:
        json.dump(prs, file, indent=4)
        print("Updated prs.json file.")  # Debugging line

    print(f"PR event handled: {action} for PR #{pr_number}")
    return "OK", 200

if __name__ == "__main__":
    app.run(port=5000, debug=False, use_reloader=False)
