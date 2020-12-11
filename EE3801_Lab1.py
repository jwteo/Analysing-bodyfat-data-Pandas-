#!/usr/bin/env python
# coding: utf-8

# In[85]:


import pandas as pd


# # Qn1(a)

# In[86]:


bodyfat2 = pd.read_csv("bodyfat2.csv") # reading in the bodyfat2.csv file


# In[87]:


bodyfat2.head() # printing out the top 5 datasets to see 


# In[88]:


columns = list(bodyfat2.columns) # getting the column names for slicing purposes later, see next cell 


# In[89]:


required_features = columns[5:] # from neck all the way to wrist


# In[90]:


# getting the mean, median, and sum from the required features 
meanFromRequiredFeatures = bodyfat2[required_features].mean(axis=1)
medianFromRequiredFeatures = bodyfat2[required_features].median(axis=1)
sumFromRequiredFeatures = bodyfat2[required_features].sum(axis=1)


# In[91]:


# getting the top 3 and bottom 3 datasets 
topThreeMeans = meanFromRequiredFeatures.head(3)
bottomThreeMeans = meanFromRequiredFeatures.tail(3)
topThreeMedians = medianFromRequiredFeatures.head(3)
bottomThreeMedians = medianFromRequiredFeatures.tail(3)
topThreeSums = sumFromRequiredFeatures.head(3)
bottomThreeSums = sumFromRequiredFeatures.tail(3)

meanColumn = topThreeMeans.append(bottomThreeMeans)
medianColumn = topThreeMedians.append(bottomThreeMedians)
sumColumn = topThreeSums.append(bottomThreeSums)

# creating a dictionary using the above values so that a dataframe can be formed at the next cell
stats = {"Mean": meanColumn, "Median": medianColumn, "Sum": sumColumn}


# In[134]:


# creating a dataframe for the top 3 and bottom 3 datasets
# the row names represent the actual indexes of the datasets in bodyfat2.csv
description_df = pd.DataFrame(stats)
description_df
print("Qn 1(a):")
"\n"
description_df


# #  Qn 1(b)

# In[136]:


# getting the mean, median, and sum for each feature
stats_df = pd.DataFrame({'Mean': bodyfat2.iloc[:,:].mean(), 'Median': bodyfat2.iloc[:,:].median(), 'Sum': bodyfat2.iloc[:,:].sum()})
print("Qn 1b: ")
"\n"
stats_df


# ## Qn 2

# In[94]:


# Getting the names of the required columns
columns = list(bodyfat2.columns)
columns[:2] + columns[5:]


# In[95]:


# maxValues of various features, from "density" ... "wrist"
maxValues = list(bodyfat2[columns[:2] + columns[5:]].max())
maxValues


# In[96]:


# Individual IDs for maxValues
maxValuesIDs = list(bodyfat2[columns[:2] + columns[5:]].idxmax())
maxValuesIDs


# In[97]:


# minValues of various features, from "density" ... "wrist"
minValues = list(bodyfat2[columns[:2] + columns[5:]].min())
minValues


# In[98]:


# Individual IDs for minValues
minValuesIDs = list(bodyfat2[columns[:2] + columns[5:]].idxmin())
minValuesIDs


# In[137]:


# getting the required dataframe, maxAndMinFat_df
list_of_tuples = list(zip(maxValues, maxValuesIDs, minValues, minValuesIDs))
maxAndMinFat_df = pd.DataFrame(list_of_tuples, columns = ["Max Value", "Individual ID", "Min Value", "Individual ID"])
maxAndMinFat_df.index = [columns[:2] + columns[5:]]
print("Qn2: ")
"\n"
maxAndMinFat_df


# # Qn 3

# In[100]:


# To merely observe the respective means and medians of the features
description = bodyfat2.describe()
description


# In[101]:


# extract the mean row from description
means = description.loc["mean"]
means


# In[102]:


medians = description.loc["50%"]
medians


# In[138]:


# find the number of entries in each feature that fall within 10% of standard deviation from its respective mean and median

columns = bodyfat2.columns #getting the column names

# j and k are used to create a 2D dataframe at the end
j= [] 
for column in columns:
    k = []
    k.append(bodyfat2[column][(bodyfat2[column]<=(means[column] + 0.1*description.loc['std',column])) & 
                           (bodyfat2[column]>=(means[column] - 0.1*description.loc['std',column]))].count())
             
    k.append(bodyfat2[column][(bodyfat2[column]<=(medians[column] + 0.1*description.loc['std',column])) &
                           (bodyfat2[column]>=(medians[column] - 0.1*description.loc['std',column]))].count())
    j.append(k)

noOfEntriesWithin10percentSD_df = pd.DataFrame(j, columns=['Mean','Medians'],index=[means.index])
print("Qn3: ")
"\n"
noOfEntriesWithin10percentSD_df


# # Qn 4

# In[104]:


bodyfat3 = pd.read_csv("bodyfat3.csv") # reading in bodyfat3.csv


# In[105]:


bodyfat3.head() # printing out the first 5 datasets to see


# In[139]:


# find the number of missing values in each feature
numOfMissingValues = bodyfat3.isnull().sum()

# Converting it into a dataframe
noOfMissingValues_df = pd.DataFrame(numOfMissingValues).transpose().rename(index={0:"missing values"})
print("Qn 4: ")
"\n"
noOfMissingValues_df 


# # Qn 5(a), part 1 - replacing missing values with mean

# In[107]:


# reading in bodyfat3.csv
bodyfat3b = pd.read_csv("bodyfat3b.csv")


# In[108]:


# replacing the missing values with the mean of that particular feature
columns = list(bodyfat3b.columns)
for column in columns:
    bodyfat3b[column].fillna(value=bodyfat3b[column].mean(), inplace = True)


# In[140]:


# printing the first 5 datasets to check if it works
print("Qn 5(a), part 1: ")
"\n"
bodyfat3b.head()


# # Qn 5(a), part 2 - compute the difference in mean value for each feature

# In[110]:


# getting the mean row from bodyfat3b using the .describe() method
description_3b = bodyfat3b.describe()
mean_3b = description_3b.loc["mean"]
mean_3b


# In[111]:


# getting the mean row from the bodyfat2 using the .descirbe() method
description_2 = bodyfat2.describe()
mean_2 = description_2.loc["mean"]
mean_2


# In[112]:


# getting the difference between the two means 
mean_differnces = abs(mean_3b - mean_2)
mean_differnces


# In[141]:


# putting the means from bodyfat2, bodyfat3b, and their differences into a single dataframe
diff = pd.DataFrame(list(zip(mean_2, mean_3b, mean_differnces)), columns = ["bodyfat2_mean", "bodyfat3b_mean", "diff_mean"], index=[mean_3b.index])
print("Qn 5(a), part 2: ")
"\n"
diff


# # Qn 5(b), part 1 - replacing missing values with median

# In[114]:


# reading in bodyfat3c.csv
bodyfat3c = pd.read_csv("bodyfat3c.csv")


# In[115]:


# replacing the missing values with the median of that particular feature
columns = list(bodyfat3c.columns)
for column in columns:
    bodyfat3c[column].fillna(value=bodyfat3c[column].median(), inplace = True)


# In[142]:


# printing the first 20 datasets to check if it works
print("Qn 5(b), part 1: ")
"\n"
bodyfat3c.head()


# # Qn 5(b), part 2 - compute the difference in median value for each feature

# In[117]:


# getting the median row from bodyfat3c using the .describe() method
description_3c = bodyfat3c.describe()
median_3c = description_3c.loc["50%"]
median_3c


# In[118]:


# getting the median row from the bodyfat2 using the .descirbe() method
description_2 = bodyfat2.describe()
median_2 = description_2.loc["50%"]
median_2


# In[119]:


# getting the difference between the two medians 
median_differnces = abs(median_3c - median_2)
median_differnces


# In[143]:


# putting the medians from bodyfat2, bodyfat3c, and their differences into a single dataframe
diff = pd.DataFrame(list(zip(median_2, median_3c, median_differnces)), columns = ["bodyfat2_median", "bodyfat3b_median", "diff_median"], index=[mean_differnces.index])
print("Qn 5b, part 2: ")
"\n"
diff


# # Qn 6(i)

# In[121]:


bodyfat2.describe() # see the mean and standard deviation 


# In[122]:


columns = list(bodyfat2.columns) # create a list of column names 


# In[123]:


# getting the new dataframe with normalized values

normalized_df = bodyfat2.copy() # have a new copy for bodyfat2 for editing purposes
for column in columns:
    feature_SD = normalized_df[column].std()
    feature_mean = normalized_df[column].mean()
    normalized_df[column] = (normalized_df[column] - feature_mean) / feature_SD

normalized_df.head() # printing out the first 5 datasets for checking 


# In[124]:


# printing the top 3 and bottom 3 rows from normalized_df
topThree = normalized_df.head(3)
bottomThree = normalized_df.tail(3)


# In[144]:


# getting the dataset that represents the top 3 and bottom 3 rows
topThreeAndBottomThree_normalized_df = pd.concat([topThree, bottomThree])
print("Qn 6(i): ")
"\n"
topThreeAndBottomThree_normalized_df


# #  Qn 6(ii)

# In[145]:


noOfFeaturesGreaterThanItsMean = {} # creating an empty dictionary to store key-value pairs
columns = list(normalized_df.columns)
for column in columns:
    count = normalized_df[column].loc[normalized_df[column] > 0].count()
    noOfFeaturesGreaterThanItsMean[column] = [count] # key-value pair representation

noOfFeaturesGreaterThanItsMean_df = pd.DataFrame(noOfFeaturesGreaterThanItsMean, index = ["No. of features more than its mean"] )
print("Qn 6(ii): ")
"\n"
noOfFeaturesGreaterThanItsMean_df


# In[ ]:




