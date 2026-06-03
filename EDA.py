#load csv   
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
data = pd.read_csv('india_housing_prices original.csv')

# Feature Engineering
data['Price_per_SqFt'] = data['Price_in_Lakhs'] / data['Size_in_SqFt']
data['Age_of_Property'] = 2025 - data['Year_Built']


# ----------------------------------------
# 🔹 1–5: Price & Size Analysis
# ----------------------------------------

#1.What is the distribution of property prices?
plt.figure(figsize=(9,6))
plt.hist(data['Price_in_Lakhs'], bins=30, color='blue', edgecolor='black')
plt.title('Distribution of Property Prices')
plt.xlabel('Price in Lakhs')
plt.ylabel('Frequency')
plt.show()

#2. What is the distribution of property sizes?
plt.figure(figsize=(9,6))
plt.hist(data['Size_in_SqFt'], bins=30, color='red', edgecolor='black')
plt.title('Distribution of Property Sizes')
plt.xlabel('Size in Square Feet')
plt.ylabel('Frequency')
plt.show()

#3.How does price per sq ft vary by property type?
data.groupby('Property_Type')['Price_per_SqFt'].mean().plot(kind='bar', color='green')
plt.title('Price per SqFt by Property Type')
plt.xlabel('Property Type')
plt.ylabel('Avg Price per SqFt')
plt.show()

#4. Is there a relationship between property size and price?
plt.figure(figsize=(9,6))
plt.scatter(data['Size_in_SqFt'], data['Price_in_Lakhs'], color='purple')
plt.title('Size vs Price')
plt.xlabel('Size in SqFt')
plt.ylabel('Price in Lakhs')
plt.show()

#5. Are there any outliers in price per sq ft or property size?
plt.figure(figsize=(9,6))
data.boxplot(column='Price_per_SqFt')
plt.title('Outliers in Price per SqFt')
plt.show()


# ----------------------------------------
# 🔹 6–10: Location-based Analysis
# ----------------------------------------

#6. What is the average price per sq ft by state?
data.groupby('State')['Price_per_SqFt'].mean().sort_values().plot(kind='bar', color='orange')
plt.title('Avg Price per SqFt by State')
plt.xlabel('State')
plt.ylabel('Avg Price per SqFt')
plt.show()

#7. What is the average property price by city?
data.groupby('City')['Price_in_Lakhs'].mean().sort_values().plot(kind='bar', color='brown')
plt.title('Avg Price by City')
plt.xlabel('City')
plt.ylabel('Avg Price in Lakhs')
plt.show()

#8. What is the median age of properties by locality?
data.groupby('Locality')['Age_of_Property'].median().sort_values().head(10)

#9. How is BHK distributed across cities?
plt.figure(figsize=(10,6))
sns.countplot(x='BHK', data=data)
plt.title('BHK Distribution')
plt.show()

#10. What are the price trends for the top 5 most expensive localities?
top_localities = data.groupby('Locality')['Price_in_Lakhs'].mean().sort_values(ascending=False).head(5)
top_localities.plot(kind='bar', color='red')
plt.title('Top 5 Costly Localities')
plt.show()


# ----------------------------------------
# 🔹 11–14: Feature Relationship & Correlation
# ----------------------------------------

#11. How are numeric features correlated with each other?
plt.figure(figsize=(10,8))
sns.heatmap(data.corr(numeric_only=True), annot=True, cmap='coolwarm')
plt.title('Correlation Heatmap')
plt.show()

#12. How do nearby schools relate to price per sq ft?
data.groupby('Nearby_Schools')['Price_per_SqFt'].mean()

#13. How do nearby hospitals relate to price per sq ft?
data.groupby('Nearby_Hospitals')['Price_per_SqFt'].mean()

#14. How does price vary by furnished status?
data.groupby('Furnished_Status')['Price_in_Lakhs'].mean().plot(kind='bar', color='cyan')
plt.title('Price by Furnished Status')
plt.show()


# ----------------------------------------
# 🔹 16–20: Investment / Amenities / Ownership Analysis
# ----------------------------------------

#16. How many properties belong to each owner type?
data['Owner_Type'].value_counts().plot(kind='bar', color='pink')
plt.title('Owner Type Distribution')
plt.show()

#17. How many properties are available under each availability status?
data['Availability_Status'].value_counts().plot(kind='bar', color='gray')
plt.title('Availability Status Distribution')
plt.show()

#18. Does parking space affect property price?
data.groupby('Parking_Space')['Price_in_Lakhs'].mean().plot(kind='bar', color='green')
plt.title('Parking Space vs Price')
plt.show()

#19. How do amenities affect price per sq ft?
data.groupby('Amenities')['Price_per_SqFt'].mean().plot(kind='bar', color='purple')
plt.title('Amenities vs Price per SqFt')
plt.show()

#20. How does public transport accessibility relate to price per sq ft?
data.groupby('Public_Transport_Accessibility')['Price_per_SqFt'].mean().plot(kind='bar', color='blue')
plt.title('Transport Accessibility vs Price per SqFt')
plt.show()