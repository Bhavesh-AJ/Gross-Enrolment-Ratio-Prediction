import numpy as np
import pandas as pd
import streamlit as st
from sklearn.linear_model import Ridge
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import PolynomialFeatures, StandardScaler


df = pd.read_csv("final_dataset.csv")

df["students_per_uni"] = df["students"] / df["universities"]
df["faculty_per_student"] = df["faculty"] / df["students"]
df["universities_per_lakh_population"] = (
    df["universities"] / df["population_18_23"]
) * 100000
df["faculty_per_lakh_population"] = (
    df["faculty"] / df["population_18_23"]
) * 100000
df = df.replace([np.inf, -np.inf], np.nan).dropna()

features = [
    "students_per_uni",
    "faculty_per_student",
    "universities_per_lakh_population",
    "faculty_per_lakh_population",
    "year",
]

X = df[features]
y = df["ger"]

model = Pipeline([
    ("poly", PolynomialFeatures(degree=2, include_bias=False)),
    ("scaler", StandardScaler()),
    ("model", Ridge(alpha=0.001)),
])
model.fit(X, y)

st.title("GER Predictor (AISHE ML Model)")
st.write("Predict Gross Enrollment Ratio using AISHE infrastructure and demographic features.")

students = st.number_input("Number of Students", min_value=1, value=100000)
universities = st.number_input("Number of Universities", min_value=1, value=50)
faculty = st.number_input("Number of Faculty", min_value=1, value=5000)
population_18_23 = st.number_input("Population Age 18-23", min_value=1, value=500000)
year = st.number_input("Year", min_value=2018, max_value=2025, value=2021)

students_per_uni = students / universities
faculty_per_student = faculty / students
universities_per_lakh_population = (universities / population_18_23) * 100000
faculty_per_lakh_population = (faculty / population_18_23) * 100000

input_data = pd.DataFrame([{
    "students_per_uni": students_per_uni,
    "faculty_per_student": faculty_per_student,
    "universities_per_lakh_population": universities_per_lakh_population,
    "faculty_per_lakh_population": faculty_per_lakh_population,
    "year": year,
}])

if st.button("Predict GER"):
    prediction = model.predict(input_data)[0]
    st.success(f"Predicted GER: {prediction:.2f}")
