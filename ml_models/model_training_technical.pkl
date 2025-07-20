import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import pickle

# Load data
df = pd.read_csv('data/water_quality_data.csv')

X = df[['temp', 'pH', 'ammonia', 'DO', 'turbidity']]
y = df['failure']

# Train model
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
clf = RandomForestClassifier()
clf.fit(X_train, y_train)

# Save model
with open('ml_models/technical_model.pkl', 'wb') as f:
    pickle.dump(clf, f)
