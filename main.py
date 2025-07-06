
import os
import random
import json
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# 讀取塔羅 JSON 資料
TAROT_PATH = os.environ.get("TAROT_JSON_PATH", "Tarot_Major_Arcana_Full.json")
try:
    with open(TAROT_PATH, encoding="utf-8") as f:
        tarot_cards = json.load(f)
except Exception as e:
    print("❌ 讀取 JSON 失敗：", e)
    tarot_cards = []

@app.route("/")
def home():
    return "🔮 Ethan Tarot API 啟動成功"

@app.route("/draw", methods=["GET"])
def draw_card():
    return jsonify(random.sample(tarot_cards, 1))

@app.route("/draw/3", methods=["GET"])
def draw_three_cards():
    return jsonify(random.sample(tarot_cards, 3))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
