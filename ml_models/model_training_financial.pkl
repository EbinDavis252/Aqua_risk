import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import pickle

# Load data
df = pd.read_csv('data/farmer_data.csv')

# Encode categorical
df['region'] = df['region'].astype('category').cat.codes
df['farm_type'] = df['farm_type'].astype('category').cat.codes

# Features & target
X = df[['age', 'income', 'loan_amount', 'region', 'loan_term', 'previous_default', 'farm_type']]
y = df['loan_default']

# Train model
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
clf = RandomForestClassifier()
clf.fit(X_train, y_train)

# Save model
with open('ml_models/financial_model.pkl', 'wb') as f:
    pickle.dump(clf, f)
