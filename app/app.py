
import streamlit as st
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from dotenv import load_dotenv
import pydeck as pdk
import os

# Load environment variables
load_dotenv()
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")

# Connect to DB and load data
engine = create_engine(f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
query = """
SELECT a.age_group AS age, s.sex, f.bmi, c.jumlah_anak AS children, sm.status AS smoker, f.charges, r.region
FROM fact_insurance f
JOIN dim_age a ON f.age_id = a.age_id
JOIN dim_sex s ON f.sex_id = s.sex_id
JOIN dim_children c ON f.children_id = c.children_id
JOIN dim_smoker sm ON f.smoker_id = sm.smoker_id
JOIN dim_region r ON f.region_id = r.region_id;
"""
df = pd.read_sql(query, engine)

# Sidebar navigation
st.sidebar.title("Menu")
page = st.sidebar.radio("Pilih Halaman", ["Dashboard Infografis", "Prediksi Biaya"])

if page == "Dashboard Infografis":
	st.title("📊 Insurance Cost Dashboard")

	# US region coordinates (approximate)
	region_avg = df.groupby("region")["charges"].mean().reset_index()
	# Define polygons (rectangles) for each region
	region_polygons = {
		"northeast": [[[-80, 40], [-80, 45], [-70, 45], [-70, 40]]],
		"northwest": [[[-125, 45], [-125, 50], [-115, 50], [-115, 45]]],
		"southeast": [[[-90, 30], [-90, 36], [-80, 36], [-80, 30]]],
		"southwest": [[[-115, 30], [-115, 36], [-105, 36], [-105, 30]]],
	}
	region_colors = {
		"northeast": [66, 135, 245, 120],    # blue
		"northwest": [76, 175, 80, 120],     # green
		"southeast": [255, 193, 7, 120],     # yellow
		"southwest": [244, 67, 54, 120],     # red
	}
	# Prepare polygon data
	polygon_data = []
	for _, row in region_avg.iterrows():
		region = row['region']
		polygon_data.append({
			"region": region,
			"polygon": region_polygons[region],
			"color": region_colors[region],
			"charges": int(row['charges']),
			"info": f"{region.capitalize()} (${int(row['charges']):,})",
			"lat": np.mean([p[1] for p in region_polygons[region][0]]),
			"lon": np.mean([p[0] for p in region_polygons[region][0]]),
		})
	polygon_df = pd.DataFrame(polygon_data)

	st.subheader("Peta Rerata Biaya Asuransi per Region (US)")
	polygon_layer = pdk.Layer(
		"PolygonLayer",
		data=polygon_df,
		get_polygon="polygon",
		get_fill_color="color",
		get_line_color=[0,0,0,200],
		pickable=True,
		auto_highlight=True,
	)
	text_layer = pdk.Layer(
		"TextLayer",
		data=polygon_df,
		get_position='[lon, lat]',
		get_text='info',
		get_color=[0, 0, 0, 255],
		get_size=40,  # larger text for visibility
		get_alignment_baseline="center",
		get_anchor="middle",  # center the text horizontally
	)
	view_state = pdk.ViewState(
		longitude=-95,
		latitude=39,
		zoom=2.5,
		pitch=0,
	)
	tooltip = {"text": "{info}"}
	st.pydeck_chart(pdk.Deck(layers=[polygon_layer, text_layer], initial_view_state=view_state, tooltip=tooltip))

	st.subheader("Distribusi biaya perokok vs non-perokok")
	import seaborn as sns
	import matplotlib.pyplot as plt
	fig, ax = plt.subplots()
	sns.boxplot(x="smoker", y="charges", data=df, ax=ax)
	st.pyplot(fig)

	st.subheader("Rerata biaya berdasarkan usia")
	age_avg = df.groupby("age")["charges"].mean().reset_index()
	st.line_chart(age_avg.set_index("age"))

	st.subheader("Korelasi antar fitur (heatmap)")
	# Only use numeric columns for correlation
	corr = df[["bmi", "children", "charges"]].corr()
	fig2, ax2 = plt.subplots()
	sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax2)
	st.pyplot(fig2)

	st.markdown("""
	### Insight & Saran
	- **Perokok** rata-rata mengeluarkan biaya jauh lebih tinggi (sering >2× non-perokok).
	- **BMI tinggi** berkorelasi dengan kenaikan biaya.
	- Ada variasi regional → Southeast cenderung lebih tinggi.
	""")

elif page == "Prediksi Biaya":
	st.title("💡 Prediksi Biaya Asuransi & Saran")
	st.write("Masukkan data Anda untuk estimasi biaya dan rekomendasi personal.")

	# Form input
	age = st.number_input("Usia", min_value=18, max_value=100, value=30)
	sex = st.selectbox("Jenis Kelamin", ["male", "female"])
	children = st.number_input("Jumlah Anak", min_value=0, max_value=10, value=0)
	smoker = st.selectbox("Status Merokok", ["yes", "no"])
	bmi = st.number_input("BMI", min_value=10.0, max_value=60.0, value=25.0)
	region = st.selectbox("Region", sorted(df["region"].unique()))

	# Simple prediction model (linear regression coefficients from public dataset)
	# These are example coefficients, adjust as needed
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

	if st.button("Estimasi Biaya"):
		st.success(f"Estimasi biaya Anda: ${est_charges:,.0f}/tahun.")
		if smoker == "yes":
			non_smoker_charges = est_charges - coef_smoker
			st.info(f"Jika Anda berhenti merokok, estimasi biaya bisa turun ke ${non_smoker_charges:,.0f}/tahun (hemat ${coef_smoker:,.0f}).")
		else:
			st.info("Biaya Anda sudah optimal terkait status merokok.")

		st.markdown("""
		#### Saran Personal
		- Jaga BMI di kisaran sehat untuk menekan biaya.
		- Pertimbangkan gaya hidup sehat untuk mengurangi risiko dan biaya.
		- Region Southeast cenderung lebih tinggi, pertimbangkan faktor regional jika relevan.
		""")
