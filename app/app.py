from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")

engine = create_engine(f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
query = """
SELECT a.age_group AS age, s.sex, f.bmi, c.child_count AS children, sm.status AS smoker, f.charges, r.region
FROM fact_insurance f
JOIN dim_age a ON f.age_id = a.age_id
JOIN dim_sex s ON f.sex_id = s.sex_id
JOIN dim_children c ON f.children_id = c.children_id
JOIN dim_smoker sm ON f.smoker_id = sm.smoker_id
JOIN dim_region r ON f.region_id = r.region_id;
"""
df = pd.read_sql(query, engine)

from flask import render_template, send_from_directory
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "ui")
app = Flask(__name__, static_folder=STATIC_DIR, template_folder=STATIC_DIR)

@app.route('/api/region-avg', methods=['GET'])
def region_avg():
    region_avg = df.groupby("region")["charges"].mean().reset_index()
    return jsonify(region_avg.to_dict(orient="records"))

@app.route('/api/boxplot-smoker', methods=['GET'])
def boxplot_smoker():
    # Return average charges for each smoker status
    data = df.groupby("smoker")["charges"].mean().reset_index()
    data.rename(columns={"charges": "avg_charges"}, inplace=True)
    return jsonify(data.to_dict(orient="records"))

@app.route('/api/age-avg', methods=['GET'])
def age_avg():
    age_avg = df.groupby("age")["charges"].mean().reset_index()
    return jsonify(age_avg.to_dict(orient="records"))

@app.route('/api/corr', methods=['GET'])
def corr():
    corr = df[["bmi", "children", "charges"]].corr()
    return jsonify(corr.to_dict())

@app.route('/api/predict', methods=['POST'])
def predict():
    data = request.json
    age = data.get("age", 30)
    sex = data.get("sex", "male")
    children = data.get("children", 0)
    smoker = data.get("smoker", "no")
    bmi = data.get("bmi", 25.0)
    region = data.get("region", "southeast")

    base = 2000
    coef_age = 250
    coef_bmi = 350
    coef_children = 400
    coef_smoker = 12000
    coef_sex = -500 if sex == "female" else 0
    coef_region = 0
    if region == "southeast":
        coef_region = 1000
    elif region == "southwest":
        coef_region = 500
    elif region == "northwest":
        coef_region = 700
    elif region == "northeast":
        coef_region = 800

    est_charges = (
        base
        + coef_age * (age / 50)
        + coef_bmi * (bmi / 30)
        + coef_children * children
        + (coef_smoker if smoker == "yes" else 0)
        + coef_sex
        + coef_region
    )

    suggestion = []
    if smoker == "yes":
        non_smoker_charges = est_charges - coef_smoker
        suggestion.append(f"Jika Anda berhenti merokok, estimasi biaya bisa turun ke ${non_smoker_charges:,.0f}/tahun (hemat ${coef_smoker:,.0f}).")
    else:
        suggestion.append("Biaya Anda sudah optimal terkait status merokok.")
    suggestion.append("Jaga BMI di kisaran sehat untuk menekan biaya.")
    suggestion.append("Pertimbangkan gaya hidup sehat untuk mengurangi risiko dan biaya.")
    if region == "southeast":
        suggestion.append("Region Southeast cenderung lebih tinggi, pertimbangkan faktor regional jika relevan.")

    return jsonify({
        "estimated_charges": round(est_charges, 2),
        "suggestion": suggestion
    })


# Home page for dashboard stats
@app.route("/")
def index():
    return render_template("index.html")

# Prediction page
@app.route("/predict")
def predict_page():
    return render_template("predict.html")

@app.route("/robots.txt")
def robots():
    return send_from_directory(app.static_folder, "robots.txt")

@app.route("/sitemap.xml")
def sitemap():
    return send_from_directory(app.static_folder, "sitemap.xml")

# Serve static files (js, svg, etc.) from /ui
@app.route("/ui/<path:filename>")
def ui_static(filename):
    return send_from_directory(app.static_folder, filename)

if __name__ == "__main__":
    app.run(debug=True)
