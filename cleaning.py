import pandas as pd

# Load dataset
df = pd.read_csv("hospital_data.csv")

# 1. Check data types and missing values
print(df.info())
print(df.isnull().sum())

# 2. Convert 'DischargedDate' to datetime (if not already)
df['DischargedDate'] = pd.to_datetime(df['DischargedDate'])

# 3. Create Age Groups
def age_group(age):
    if age < 30:
        return '18-29'
    elif age < 45:
        return '30-44'
    elif age < 60:
        return '45-59'
    else:
        return '60+'

df['AgeGroup'] = df['Age'].apply(age_group)

# 4. Create Cost Per Day column
df['CostPerDay'] = (df['TreatmentCost'] / df['LengthOfStay']).round(2)

# 5. Check class balance for Readmitted
print(df['Readmitted'].value_counts())

# 6. Save updated file
df.to_csv("cleaned_hospital_data.csv", index=False)

# Preview
df.head()
