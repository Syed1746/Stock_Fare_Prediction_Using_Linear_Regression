import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import joblib

# Load your dataset (replace 'data.csv' with the actual filename)
data = pd.read_csv('company_stock_data.csv')

# Define the features (X) and target (y)
X = data[['Company', 'Open', 'Low', 'High']]
y = data['Close/Last'].str.replace('$', '').astype(float)

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Define preprocessing steps (one-hot encoding for 'Company')
preprocessor = ColumnTransformer(
    transformers=[
        ('cat', OneHotEncoder(), ['Company'])
    ],
    remainder='passthrough'
)

# Create a linear regression model pipeline
model = Pipeline([
    ('preprocessor', preprocessor),
    ('regressor', LinearRegression())
])

# Fit the model to the training data
model.fit(X_train, y_train)

# Evaluate the model on the test data (optional)
score = model.score(X_test, y_test)
print(f'Model Score: {score:.2f}')

# Save the trained model as a 'model.pkl' file
joblib.dump(model, 'model.pkl')
