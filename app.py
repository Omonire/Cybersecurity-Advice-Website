from flask import Flask, render_template, request, jsonify
import socket
import feedparser
import re

app = Flask(__name__)

def check_password_strength(password):
    score = 0
    if len(password) >= 8:
        score += 1
    if re.search(r'[A-Z]', password):
        score += 1
    if re.search(r'[a-z]', password):
        score += 1
    if re.search(r'[0-9]', password):
        score += 1
    if re.search(r'[@$!%*?&]', password):
        score += 1
    if score <= 2:
        return "Weak"
    elif score <= 4:
        return "Moderate"
    else:
        return "Strong"

def get_cyber_news():
    feeds = [
        "https://krebsonsecurity.com/feed/",
        "https://threatpost.com/feed/"
    ]
    news_items = []
    for feed in feeds:
        parsed_feed = feedparser.parse(feed, request_headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/115.0.0.0 Safari/537.36'
        })
        if hasattr(parsed_feed, "entries"):
            for entry in parsed_feed.entries[:5]:
                news_items.append({
                    "title": entry.title,
                    "link": entry.link,
                    "published": getattr(entry, "published", "No date")
                })
    return news_items


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/news")
def news():
    return render_template("news.html", news=get_cyber_news())

@app.route("/password-checker")
def password_checker():
    return render_template("password_checker.html")

@app.route("/password-check", methods=["POST"])
def password_check():
    password = request.json.get("password", "")
    return jsonify({"strength": check_password_strength(password)})

@app.route("/port-scanner", methods=["GET", "POST"])
def port_scanner():
    results = []
    if request.method == "POST":
        target = request.form.get("target")
        try:
            start_port = int(request.form.get("start_port"))
            end_port = int(request.form.get("end_port"))
        except:
            return render_template("port_scanner.html", results=["Invalid port range"])
        for port in range(start_port, end_port + 1):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0.5)
                if sock.connect_ex((target, port)) == 0:
                    results.append(f"Port {port} is OPEN")
                sock.close()
            except:
                pass
    return render_template("port_scanner.html", results=results)

@app.route("/tools")
def tools():
    return render_template("tools.html")

@app.route("/checklist")
def checklist():
    return render_template("checklist.html")

@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True)
