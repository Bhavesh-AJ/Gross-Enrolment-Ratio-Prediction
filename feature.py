import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load final dataset
df = pd.read_csv("final_dataset.csv")

# Select only numeric columns for correlation analysis
numeric_columns = [
    "ger",
    "students",
    "universities",
    "faculty",
    "population_18_23",
    "students_per_uni",
    "faculty_per_student",
    "enrollment_rate_proxy",
    "universities_per_lakh_population",
    "faculty_per_lakh_population",
    "year"
]

df_numeric = df[numeric_columns]

# =========================================================
# 1. CORRELATION ANALYSIS
# =========================================================

# Generate correlation matrix
corr_matrix = df_numeric.corr()

# Print correlation values with GER
print("\nCorrelation of Features with GER:\n")
print(corr_matrix["ger"].sort_values(ascending=False))

# Plot heatmap
plt.figure(figsize=(12, 8))
sns.heatmap(
    corr_matrix,
    annot=True,
    fmt=".2f",
    cmap="coolwarm",
    linewidths=0.5
)

plt.title("Feature Correlation Heatmap - GER Project")
plt.tight_layout()
plt.show()


# =========================================================
# 2. HISTOGRAM (Distribution of GER)
# =========================================================

plt.figure(figsize=(8, 5))
sns.histplot(df["ger"], kde=True)

plt.title("Distribution of GER")
plt.xlabel("GER")
plt.ylabel("Frequency")
plt.tight_layout()
plt.show()


# =========================================================
# 3. BOXPLOT (Outlier Detection for GER)
# =========================================================

plt.figure(figsize=(8, 5))
sns.boxplot(x=df["ger"])

plt.title("Boxplot of GER (Outlier Detection)")
plt.xlabel("GER")
plt.tight_layout()
plt.show()


# =========================================================
# 4. SCATTER PLOT (GER vs Enrollment Rate Proxy)
# =========================================================

plt.figure(figsize=(8, 6))
sns.scatterplot(
    x=df["enrollment_rate_proxy"],
    y=df["ger"]
)

plt.title("GER vs Enrollment Rate Proxy")
plt.xlabel("Enrollment Rate Proxy")
plt.ylabel("GER")
plt.tight_layout()
plt.show()


# =========================================================
# 5. SCATTER PLOT (GER vs Universities per Lakh Population)
# =========================================================

plt.figure(figsize=(8, 6))
sns.scatterplot(
    x=df["universities_per_lakh_population"],
    y=df["ger"]
)

plt.title("GER vs Universities per Lakh Population")
plt.xlabel("Universities per Lakh Population")
plt.ylabel("GER")
plt.tight_layout()
plt.show()


# =========================================================
# 6. PAIRPLOT (Relationship Between Important Features)
# =========================================================

important_features = [
    "ger",
    "enrollment_rate_proxy",
    "faculty_per_lakh_population",
    "universities_per_lakh_population"
]

sns.pairplot(df[important_features])

plt.show()