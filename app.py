import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

st.set_page_config(page_title="AI Health Dashboard", layout="wide")

# Load Data
df = pd.read_csv("cleaned_hospital_data.csv")
st.title("🏥 AI-Driven Healthcare Dashboard")

# KPIs
total_patients = df.shape[0]
readmission_rate = round(df['Readmitted'].mean() * 100, 2)
avg_cost = round(df['TreatmentCost'].mean(), 2)
avg_los = round(df['LengthOfStay'].mean(), 2)

col1, col2, col3, col4 = st.columns(4)
col1.metric("👨‍⚕️ Total Patients", total_patients)
col2.metric("🔁 Readmission Rate", f"{readmission_rate}%")
col3.metric("💰 Avg. Treatment Cost", f"₹{avg_cost}")
col4.metric("🛏️ Avg. Length of Stay", f"{avg_los} days")

st.markdown("---")

# Section: Visual Insights
st.subheader("📊 Department-wise Analysis")

col5, col6 = st.columns(2)

with col5:
    dept_cost = df.groupby('Department')['TreatmentCost'].mean().sort_values()
    fig1, ax1 = plt.subplots()
    dept_cost.plot(kind='barh', ax=ax1, color='skyblue')
    ax1.set_title("Avg. Treatment Cost by Department")
    st.pyplot(fig1)

with col6:
    diag_readmit = df.groupby('Diagnosis')['Readmitted'].mean().sort_values()
    fig2, ax2 = plt.subplots()
    diag_readmit.plot(kind='barh', ax=ax2, color='salmon')
    ax2.set_title("Readmission Rate by Diagnosis")
    st.pyplot(fig2)

st.markdown("---")

# Section: Readmission Prediction
st.subheader("🤖 Predict Readmission")

user_age = st.selectbox("Age Group", df['AgeGroup'].unique())
user_gender = st.selectbox("Gender", df['Gender'].unique())
user_dept = st.selectbox("Department", df['Department'].unique())
user_diag = st.selectbox("Diagnosis", df['Diagnosis'].unique())
user_cost = st.number_input("Treatment Cost (₹)", min_value=0.0, step=500.0)
user_los = st.number_input("Length of Stay (days)", min_value=0, step=1)
user_satis = st.slider("Satisfaction Score (1 to 10)", 1, 10)

# Preprocess for prediction
X = df.drop(columns=['PatientID', 'DischargedDate', 'Readmitted'])
y = df['Readmitted']
X = pd.get_dummies(X, drop_first=True)

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)
model = LogisticRegression(max_iter=1000, class_weight='balanced')
model.fit(X_train, y_train)

# Prepare user input
input_dict = {
    'TreatmentCost': user_cost,
    'LengthOfStay': user_los,
    'SatisfactionScore': user_satis
}
for col in X.columns:
    if 'Gender_' in col:
        input_dict[col] = 1 if col == f"Gender_{user_gender}" else 0
    elif 'Department_' in col:
        input_dict[col] = 1 if col == f"Department_{user_dept}" else 0
    elif 'Diagnosis_' in col:
        input_dict[col] = 1 if col == f"Diagnosis_{user_diag}" else 0
    elif 'AgeGroup_' in col:
        input_dict[col] = 1 if col == f"AgeGroup_{user_age}" else 0
    elif col not in input_dict:
        input_dict[col] = 0

input_df = pd.DataFrame([input_dict])
input_df = input_df.reindex(columns=X.columns, fill_value=0)

input_scaled = scaler.transform(input_df)

# Prediction
if st.button("Predict Readmission"):
    prediction = model.predict(input_scaled)[0]
    if prediction == 1:
        st.error("🔁 Patient is likely to be **READMITTED**.")
    else:
        st.success("✅ Patient is **NOT likely** to be readmitted.")

