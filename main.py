
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import json
from weasyprint import HTML
from jinja2 import Environment, FileSystemLoader
import os

app = Flask(__name__)
CORS(app)

# 設定路徑
TAROT_JSON_PATH = os.getenv("TAROT_JSON_PATH", "Tarot_Major_Arcana_Full.json")
TEMPLATE_FOLDER = "templates"
env = Environment(loader=FileSystemLoader(TEMPLATE_FOLDER))

# 讀取資料庫
def load_tarot_data():
    with open(TAROT_JSON_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

# 產出單張牌報告
def generate_pdf_report(data):
    template = env.get_template("report_single.html")
    html_out = template.render(card=data)
    output_path = "Tarot_Report_Single.pdf"
    HTML(string=html_out).write_pdf(output_path)
    return output_path

# 產出三張牌報告
def generate_pdf_3cards(data):
    template = env.get_template("report_3cards.html")
    html_out = template.render(cards=data)
    output_path = "Tarot_Report_3cards.pdf"
    HTML(string=html_out).write_pdf(output_path)
    return output_path

@app.route("/")
def home():
    return "Ethan Tarot API v1.2 - Running"

@app.route("/draw", methods=["GET"])
def draw_one():
    try:
        tarot_data = load_tarot_data()
        import random
        card = random.choice(tarot_data)
        force_upright = request.args.get("force_upright", "false").lower() == "true"
        if not force_upright:
            card["position"] = random.choice(["正位", "逆位"])
        else:
            card["position"] = "正位"
        return jsonify(card)
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/draw/3", methods=["GET"])
def draw_three():
    try:
        tarot_data = load_tarot_data()
        import random
        cards = random.sample(tarot_data, 3)
        positions = ["愛情", "事業", "未來"]
        for i, card in enumerate(cards):
            card["topic"] = positions[i]
            card["position"] = random.choice(["正位", "逆位"])
        return jsonify(cards)
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/report", methods=["POST"])
def report_single():
    try:
        data = request.get_json()
        pdf_path = generate_pdf_report(data)
        return send_file(pdf_path, as_attachment=True)
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/report/3", methods=["POST"])
def report_three():
    try:
        data = request.get_json()
        pdf_path = generate_pdf_3cards(data)
        return send_file(pdf_path, as_attachment=True)
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
