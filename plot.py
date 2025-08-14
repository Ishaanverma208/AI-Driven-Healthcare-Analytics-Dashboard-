import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("cleaned_hospital_data.csv")

sns.set(style="whitegrid")

# 1. Readmission by Department
plt.figure(figsize=(8, 5))
sns.countplot(data=df, x='Department', hue='Readmitted')
plt.title("Readmissions by Department")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 2. Readmission by Age Group
plt.figure(figsize=(6, 4))
sns.countplot(data=df, x='AgeGroup', hue='Readmitted')
plt.title("Readmissions by Age Group")
plt.tight_layout()
plt.show()

# 3. Average Treatment Cost by Department
plt.figure(figsize=(8, 5))
sns.barplot(data=df, x='Department', y='TreatmentCost', estimator='mean')
plt.title("Avg Treatment Cost by Department")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 4. Satisfaction Score vs Readmission
plt.figure(figsize=(6, 4))
sns.boxplot(data=df, x='Readmitted', y='SatisfactionScore')
plt.title("Satisfaction Score vs Readmission")
plt.tight_layout()
plt.show()

# 5. Cost vs Length of Stay
plt.figure(figsize=(6, 4))
sns.scatterplot(data=df, x='LengthOfStay', y='TreatmentCost', hue='Readmitted')
plt.title("Treatment Cost vs Length of Stay")
plt.tight_layout()
plt.show()
