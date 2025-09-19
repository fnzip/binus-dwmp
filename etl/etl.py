import pandas as pd
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

# 1. Load dataset
df = pd.read_csv("data/insurance.csv")

# 2. Transform
df["age_group"] = pd.cut(
  df["age"],
  bins=[0, 25, 35, 50, 100],
  labels=["18-25", "26-35", "36-50", "50+"]
)

# 3. Connect PostgreSQL
engine = create_engine(f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

# 4. Load dimension tables (insert unik)
df[["sex"]].drop_duplicates().to_sql("dim_sex", engine, if_exists="append", index=False)
df[["smoker"]].drop_duplicates().rename(columns={"smoker": "status"}).to_sql("dim_smoker", engine, if_exists="append", index=False)
df[["region"]].drop_duplicates().to_sql("dim_region", engine, if_exists="append", index=False)
df[["age_group"]].drop_duplicates().to_sql("dim_age", engine, if_exists="append", index=False)
df[["children"]].drop_duplicates().rename(columns={"children": "jumlah_anak"}).to_sql("dim_children", engine, if_exists="append", index=False)

# 5. Ambil dimensi dari DB untuk mapping
dim_sex = pd.read_sql("SELECT sex_id, sex FROM dim_sex", engine)
dim_smoker = pd.read_sql("SELECT smoker_id, status FROM dim_smoker", engine)
dim_region = pd.read_sql("SELECT region_id, region FROM dim_region", engine)
dim_age = pd.read_sql("SELECT age_id, age_group FROM dim_age", engine)
dim_children = pd.read_sql("SELECT children_id, jumlah_anak FROM dim_children", engine)

# 6. Merge ke df → ganti string jadi ID
df = df.merge(dim_sex, on="sex", how="left") \
  .merge(dim_smoker, left_on="smoker", right_on="status", how="left") \
  .merge(dim_region, on="region", how="left") \
  .merge(dim_age, on="age_group", how="left") \
  .merge(dim_children, left_on="children", right_on="jumlah_anak", how="left")

# 7. Pilih kolom sesuai fact schema
fact_df = df[["age_id", "sex_id", "bmi", "children_id", "smoker_id", "region_id", "charges"]]

# 8. Insert fact table
fact_df.to_sql("fact_insurance", engine, if_exists="append", index=False)

print("✅ ETL selesai, data masuk ke dimensi + fact_insurance")
