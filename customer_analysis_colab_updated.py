# -*- coding: utf-8 -*-
"""customer_analysis_colab_updated.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1XrhRjEgVAihuKh3OSrXggthqB7U6P0p7

# 📊 Customer Data Analysis & Machine Learning
This notebook performs:
- Data Cleaning
- Exploratory Data Analysis (EDA) with Graphs
- Machine Learning (Customer Segmentation or Churn Prediction)

🔹 **By: Your Name**
🔹 **Dataset: customers-10000.csv**
"""

# Install necessary libraries (if not already installed)
!pip install pandas numpy matplotlib seaborn scikit-learn

# Import required libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

print("Libraries imported successfully!")

"""## 📂 Load and Inspect Data"""

# Load dataset (Upload in Colab)
from google.colab import files
uploaded = files.upload()

# Read CSV
df = pd.read_csv(list(uploaded.keys())[0])
df.head(5)

"""## 🔍 Data Cleaning"""

# Drop unnecessary columns
df_cleaned = df.drop(columns=['Index', 'Phone 1', 'Phone 2'])

# Convert Subscription Date to datetime format
df_cleaned['Subscription Date'] = pd.to_datetime(df_cleaned['Subscription Date'], errors='coerce')

# Display dataset info
df_cleaned.info()

"""## 📊 Customer Distribution by Country"""

# Top 10 countries with most customers
top_countries = df_cleaned['Country'].value_counts().head(10)

# Plot
plt.figure(figsize=(6,3))
sns.barplot(x=top_countries.index, y=top_countries.values, palette='coolwarm')
plt.title('Top 10 Countries with Most Customers')
plt.xticks(rotation=45)
plt.show()

"""## 📈 Subscription Trend Over Time"""

# Aggregate subscriptions by year
df_cleaned['Year'] = df_cleaned['Subscription Date'].dt.year
subscriptions_per_year = df_cleaned['Year'].value_counts().sort_index()

# Plot
plt.figure(figsize=(6,3))
sns.lineplot(x=subscriptions_per_year.index, y=subscriptions_per_year.values, marker='o', color='blue')
plt.title('Customer Subscription Trend Over the Years')
plt.xlabel('Year')
plt.ylabel('Number of Subscriptions')
plt.grid(True)
plt.show()

"""## 🤖 Machine Learning: Customer Segmentation (Clustering)"""

# Prepare data for clustering
features = df_cleaned[['Year']]
scaler = StandardScaler()
features_scaled = scaler.fit_transform(features)

# Apply K-Means Clustering
kmeans = KMeans(n_clusters=3, random_state=42)
df_cleaned['Cluster'] = kmeans.fit_predict(features_scaled)

# Plot Clusters
plt.figure(figsize=(7,3))
sns.scatterplot(x=df_cleaned['Year'], y=df_cleaned.index, hue=df_cleaned['Cluster'], palette='coolwarm')
plt.title('Customer Segmentation Based on Subscription Year')
plt.show()

"""# 🔥 Classification Models (Logistic Regression, Random Forest, SVM)"""

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score

# Encode categorical target variable (Example: 'Country' as classification target)
label_encoder = LabelEncoder()
df_cleaned['Country_Label'] = label_encoder.fit_transform(df_cleaned['Country'])

# Define features and target
X = df_cleaned[['Year']]
y = df_cleaned['Country_Label']

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train and evaluate models
models = {
    'Logistic Regression': LogisticRegression(),
    'Random Forest': RandomForestClassifier(n_estimators=100),
    'Support Vector Machine': SVC()
}

for name, model in models.items():
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f'{name} Accuracy: {accuracy:.2f}')

"""# 📈 Regression Models (Linear Regression, Decision Trees)"""

from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_absolute_error

# Define target variable (Example: Predicting year of subscription)
y_reg = df_cleaned['Year']

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(X, y_reg, test_size=0.2, random_state=42)

# Train models
regression_models = {
    'Linear Regression': LinearRegression(),
    'Decision Tree': DecisionTreeRegressor()
}

for name, model in regression_models.items():
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    print(f'{name} MAE: {mae:.2f}')

"""# 🎯 Clustering (K-Means, Expectation Maximization)"""

from sklearn.mixture import GaussianMixture

# Apply Gaussian Mixture Model (Expectation Maximization)
gmm = GaussianMixture(n_components=3, random_state=42)
df_cleaned['GMM_Cluster'] = gmm.fit_predict(features_scaled)

# Visualize clustering
plt.figure(figsize=(7,3))
sns.scatterplot(x=df_cleaned['Year'], y=df_cleaned.index, hue=df_cleaned['GMM_Cluster'], palette='viridis')
plt.title('Customer Segmentation with GMM')
plt.show()

"""# 🔥 Collaborative Filtering (ALS, Matrix Factorization)"""

!pip install scikit-surprise
from surprise import SVD, Dataset, Reader
from surprise.model_selection import train_test_split

# Simulated collaborative filtering dataset (needs real user-product data)
reader = Reader(rating_scale=(1, 5))
data = Dataset.load_from_df(df_cleaned[['Customer Id', 'Year', 'Country_Label']], reader)

# Split dataset
trainset, testset = train_test_split(data, test_size=0.2)

# Train Matrix Factorization model (SVD)
model = SVD()
model.fit(trainset)

# Make predictions
predictions = model.test(testset)
print(predictions[:5])  # Show sample predictions

"""# 🎭 Dimensionality Reduction (PCA)"""

pca = PCA(n_components=1)
pca_result = pca.fit_transform(features_scaled)
df_cleaned['PCA1'] = pca_result[:, 0]


# Scatter plot of PCA (updated for 1 PCA component)
plt.figure(figsize=(6,3))
sns.scatterplot(x=df_cleaned['PCA1'], y=df_cleaned.index, hue=df_cleaned['GMM_Cluster'], palette='coolwarm')
plt.show()