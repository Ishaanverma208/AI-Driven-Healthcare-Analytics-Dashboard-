import pandas as pd
import random
from datetime import datetime, timedelta
import numpy as np

departments = ['Cardiology', 'Oncology', 'Surgery', 'Orthopedics', 'Neurology']
diagnoses = ['Diabetes', 'Cancer', 'Fracture', 'Heart Attack', 'Stroke']

def random_date():
    return datetime.today() - timedelta(days=random.randint(0, 730))

data = []

for i in range(1000):
    age = random.randint(18, 90)
    gender = random.choice(['Male', 'Female'])
    dept = random.choice(departments)
    diag = random.choice(diagnoses)
    cost = random.randint(10000, 200000)
    los = random.randint(1, 15)
    readmit = np.random.binomial(1, 0.2 if age < 60 else 0.35)
    score = random.randint(1, 5)
    date = random_date().date()
    
    data.append([i+1, age, gender, dept, diag, cost, los, readmit, score, date])

columns = ['PatientID', 'Age', 'Gender', 'Department', 'Diagnosis', 'TreatmentCost', 'LengthOfStay', 'Readmitted', 'SatisfactionScore', 'DischargedDate']
df = pd.DataFrame(data, columns=columns)

df.to_csv("hospital_data.csv", index=False)
df.head()
