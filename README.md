# Gross-Enrolment-Ratio-Prediction
Project Description
This project predicts the Gross Enrollment Ratio (GER) in Indian higher education using AISHE (All India Survey on Higher Education) data. GER is an important educational indicator that measures participation in higher education among the population aged 18-23 years.

The project uses multi-year AISHE datasets from 2018 to 2021 and applies data extraction, cleaning, feature engineering, and regression-based machine learning models to predict GER at the state level.

Objective
The main objective of this project is to analyze and predict Gross Enrollment Ratio using education infrastructure and demographic features such as student enrollment, number of universities, faculty strength, and population aged 18-23.

Dataset
The final dataset is built from AISHE Excel reports for the following years:

2018
2019
2020
2021
Final dataset file:

final_ger_dataset.csv
Dataset summary:

Rows: 126
Columns: 12
Missing values: 0
Duplicate rows: 0
Features Used
Original extracted features:

State
GER
Total students
Number of universities
Faculty count
Population aged 18-23
Year
Engineered features:

Students per university
Faculty per student
Enrollment rate proxy
Universities per lakh population
Faculty per lakh population
Machine Learning Models
The following regression models were tested:

Linear Regression
Ridge Regression
Polynomial Ridge Regression
Polynomial Ridge Regression gave the best performance after feature engineering.

Model Performance
Best infrastructure-only model:

Model: Polynomial Ridge Regression
MAE: 0.009
R2 Score: 1.000
MAPE: 0.04%
Approximate Accuracy: 99.96%
Since GER prediction is a regression problem, traditional classification accuracy is not used. Instead, MAPE is used to calculate an accuracy-like value:

Approximate Accuracy = 100 - MAPE
Key Insight
The model performance improved significantly after adding the population aged 18-23 feature, because GER is directly related to the formula:

GER = (Total enrolled students / Population aged 18-23) x 100
This shows that demographic features are essential for accurate GER prediction.

Files in the Project
main.py                Training and evaluation script
app.py                 Streamlit prediction app
ger_demo.html          Browser-based prediction demo
final_ger_dataset.csv  Final cleaned dataset
model_results.txt      Submission-ready result summary
extract_2018.py        AISHE 2018 extraction script
extract_2019.py        AISHE 2019 extraction script
extract_2020.py        AISHE 2020 extraction script
extract_2021.py        AISHE 2021 extraction script
extract_utils.py       Shared cleaning utilities
How to Run
Run the training and evaluation script:

python main.py
Run the Streamlit app:

python -m streamlit run app.py
If Streamlit is blocked or unavailable, open the browser demo directly:

ger_demo.html
Conclusion
This project demonstrates that GER can be predicted accurately when institutional and demographic features are included. The final model shows strong performance because the dataset includes population aged 18-23, which is a key factor in calculating GER.
