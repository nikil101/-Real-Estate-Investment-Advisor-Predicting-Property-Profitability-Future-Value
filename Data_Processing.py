# Data Processing for india_housing_prices original.csv
import pandas as pd 
# Load the dataset
data = pd.read_csv('india_housing_prices original.csv')
#check for null values
print(data.isnull().sum())
data.drop_duplicates(inplace=True)
print(data.duplicated().sum())

#Ml part of the project which is optional 
import sklearn.preprocessing

scaler = sklearn.preprocessing.StandardScaler()

data[['Size_in_SqFt', 'Price_in_Lakhs']] = scaler.fit_transform(
    data[['Size_in_SqFt', 'Price_in_Lakhs']]
)
#Label encoding 
from sklearn.preprocessing import LabelEncoder

le = LabelEncoder()

data['City'] = le.fit_transform(data['City'])
data['Property_Type'] = le.fit_transform(data['Property_Type'])
pd.set_option('display.max_columns', None)
print(data.head())