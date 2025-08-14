import pandas as pd
import sqlite3
# Load cleaned CSV
df = pd.read_csv("cleaned_hospital_data.csv")

# Create SQLite DB in memory
conn = sqlite3.connect(":memory:")
df.to_sql("patients", conn, index=False, if_exists='replace')

# 1. Top 3 Costliest Departments
q1 = """
SELECT Department, ROUND(AVG(TreatmentCost), 2) AS AvgCost
FROM patients
GROUP BY Department
ORDER BY AvgCost DESC
LIMIT 3;
"""

# 2. Avg Cost for Readmitted vs Not
q2 = """
SELECT Readmitted, ROUND(AVG(TreatmentCost), 2) AS AvgCost
FROM patients
GROUP BY Readmitted;
"""

# 3. Readmission % by Diagnosis
q3 = """
SELECT Diagnosis,
       COUNT(*) AS Total,
       SUM(Readmitted) AS ReadmittedCount,
       ROUND(100.0 * SUM(Readmitted) / COUNT(*), 2) AS ReadmitRate
FROM patients
GROUP BY Diagnosis
ORDER BY ReadmitRate DESC;
"""

# 4. Avg Length of Stay per Age Group
q4 = """
SELECT AgeGroup, ROUND(AVG(LengthOfStay), 2) AS AvgStay
FROM patients
GROUP BY AgeGroup
ORDER BY AvgStay DESC;
"""

# 5. Satisfaction Breakdown by Department
q5 = """
SELECT Department,
       ROUND(AVG(SatisfactionScore), 2) AS AvgSatisfaction
FROM patients
GROUP BY Department
ORDER BY AvgSatisfaction DESC;
"""

# Run and display each query
for i, q in enumerate([q1, q2, q3, q4, q5], start=1):
    print(f"\nQuery {i} Result:")
    print(pd.read_sql(q, conn))
