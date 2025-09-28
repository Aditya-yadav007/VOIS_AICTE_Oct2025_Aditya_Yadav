# %%
import numpy as np
import pandas as pd 
import matplotlib .pyplot as plt
import seaborn as sns
import plotly.express as px
import pickle

# %%
# read the airbnb data
df = pd.read_csv('Airbnb_Open_Data.csv', low_memory = False)

# %%
df.head()

# %%
df.info()

# %%
df.duplicated().value_counts()

# %%
df[df['neighbourhood group']=='brookIn']

# %%
# Drop duplicate records
df.drop_duplicates(inplace= True)
# Drop house_rules and license column with insufficient data
df.drop(['house_rules', 'license'], axis = 1, inplace= True)
# Remove all dollar signs in the price and service fee column
df['price'] = df['price'].str.replace('$','', regex= False)
df['service fee'] = df['service fee'].str.replace('$','', regex= False)
#Remove all commas in the price and service fee columns
df['price'] = df['price'].str.replace(',' ,'', regex=False)
df['service fee'] = df['service fee'].str.replace(',' ,'', regex=False)
# Rename the price and service fee columns to include a dollar sign
df.rename(columns={
    'price':'price_$',
    'service fee':'service_fee_$'
}, inplace= True)
# Drop all records with missing values
df.dropna(inplace = True)
#change all mismatched data types to the appropriate once
df['price_$'] = df['price_$'].astype(float)
df['service_fee_$'] = df['service_fee_$'].astype(float)
df['id'] = df['id'].astype(str)
df['host id'] = df['host id'].astype(str)
df['last review'] = pd.to_datetime(df['last review'])
df['Construction year'] = df['Construction year'].astype(int)

# Correct the Spelling of 'brookln' to 'Brooklyn'
df.loc[df['neighbourhood group'] == 'brookln','neighbourhood group'] = 'Brooklyn'
df = df.drop(df[df['availability 365']>500].index)

# %%
df.duplicated().value_counts()

# %%
df.info()

# %%
df.describe()

# %%
property_types = df['room type'].value_counts().to_frame()
property_types

# %%
room_type_bar = plt.bar(property_types.index, property_types.loc[:,"count"]);
plt.bar_label(room_type_bar, labels =property_types.loc[:,"count"], padding=4);
plt.ylim([0,50000]);
plt.xlabel('Room Type');
plt.ylabel('Room Typw Count');
plt.title('property Type and their count in the Dataset');

# %%
hood_group = df['neighbourhood group'].value_counts().to_frame()
hood_group

# %%
hood_group_bar = plt.bar(hood_group.index, hood_group.loc[:,"count"]);
plt.bar_label(hood_group_bar, labels =hood_group.loc[:,"count"], padding=4);
plt.ylim([0,40000]);
plt.xlabel('Neighborhood Groups');
plt.ylabel('Number of Listings');
plt.title('Which Neighborhood Groups has the highest number of Listings');

# %%
#Which neighborhoods group have the highest average prices for Airbnb listings?
avg_price = df.groupby('neighbourhood group')['price_$' ].mean().sort_values(ascending=False).to_frame()
avg_price_bar= plt.bar(avg_price.index, avg_price.loc[:, 'price_$']);
plt.bar_label(avg_price_bar, labels =round(avg_price.loc[:,"price_$"], 2),label_type ='edge', padding=4);
plt.ylim([0,700]);
plt.xlabel('Neighborhood Group');
plt.ylabel('Average Price per Listings ($)');
plt.xticks (rotation=45);
plt.title('Average Price per Listings ($) in each Neighborhood Group');

# %%
# is there a relationship between the construction year of property and price?
df.groupby(df['Construction year'])['price_$'].mean().to_frame().plot();
plt.xlabel('Construction Year');
plt.ylabel('Average Price ($)');
plt.title('Average Price ($) for properties in each construction Year');

# %%
# Who are the top 10 hosts by calculated host listing count?
hosts = df.groupby('host name') ['calculated host listings count'].sum().sort_values(ascending=False).nlargest(10).to_frame()
hosts_bar = plt.bar(hosts.index, hosts.loc[:, 'calculated host listings count']);
plt.bar_label(hosts_bar, label = hosts.loc[:, 'calculated host listings count'], label_type ='edge', padding=1);
plt.xlabel('Hosts Name');
plt.ylabel('Calculated Host Listings count');
plt.xticks(rotation =80);
plt.ylim([10, 120000]);
plt.title('Top 10 Hosts by calculated bust Listings Count');

# %%
#Are hosts with verified identities more likely to receive positive reviews
review = df.groupby('host_identity_verified')['review rate number'].mean().sort_values(ascending= False).to_frame()
review

# %%
review_bar = plt.bar(review.index, review.loc[:,"review rate number"]);
plt.bar_label(review_bar, labels =round(review.loc[:,"review rate number"],2), padding=4);
plt.ylim([0,4]);
plt.xlabel('Host Verification Status');
plt.ylabel('Average Review Rate Number');
plt.title('Average Review Rate for each Varification Statistics.')

# %%
base_color = sns.color_palette()[0]
sns.boxplot(data = df, x = "host_identity_verified", y = "review rate number", color = base_color);
plt.xlabel('Host Verification status');
plt.ylabel('Review Rate Number');
plt.title('Average Review Rate for each Verification Status');

# %%
#Is there a correlation between the price of a listing and its service fee?
df['price_$'].corr(df['service_fee_$'])

# %%
sns.regplot(df, x= 'price_$', y = 'service_fee_$');
plt.xlabel('Price ($)');
plt.ylabel('Service Fee ($)');
plt.title('A Regression Plot showing the Correlation of the Price of a Listing and its Service Fee.');

# %%
# What is the average review rate number (e.g., stars) for listings, and does it vary based on the neighborhood group and room type 

ARRN = df.groupby(['neighbourhood group','room type'])['review rate number'].mean().to_frame()
ARRN

# %%
plt.figure(figsize = [12,10]);
sns.barplot(data = df, x = 'neighbourhood group', y = 'review rate number', hue = 'room type');
plt.xlabel('Neighbourhood Group');
plt.ylabel('Average Review Rate');
plt.title('Average Review Rate for each Room/Property Type in each Neighbourhood Group.');

# %%
#Are hosts with a higher calculated host listings count more likely to maintain higher availability throughout the year?
sns.regplot (df, x = 'calculated host listings count', y = 'availability 365');
plt.xlabel('Calculated Host Listings');
plt.ylabel('Availability 365');
plt.title('A Regression Plot of the Relationship between Calculated Host Listings Count and Availability 365');

# %%
df['calculated host listings count'].corr(df['availability 365']);

# %%
# to save the ipynb file into pickle file 
with open ("Aditya_yadav.pkl", "wb") as f:
    pickle.dump(df, f)


