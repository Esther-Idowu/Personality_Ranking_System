#!/usr/bin/env python
# coding: utf-8

# # PERSONALITY PREDICTION

# In[1]:


#Import Pandas library for reading in the data
import pandas as pd
Data = pd.read_csv("data-final.csv", sep = "\t")


# In[2]:


print(Data)


# In[3]:


#We can view the columns present in our dataset
columns = Data.columns
for column in columns:
    print(column)


# In[4]:


#The data contains 50 reponses to personality data and also some metadata collected during the data gathering.


# In[5]:


#We will limit our data to only 50 columns 


# In[6]:


import numpy as np


# In[7]:


coln = Data[Data.columns[0:50]]


# In[8]:


coln


# In[9]:


#Display all the columns
pd.set_option("display.max_columns", None)


# In[10]:


coln


# In[11]:


coln = coln.fillna(0)


# In[12]:


from sklearn.cluster import MiniBatchKMeans


# In[13]:


kmeans = MiniBatchKMeans(n_clusters=10, random_state = 0, batch_size =100, max_iter =100).fit(coln)


# In[14]:


#the length of our cluster


# In[15]:


len(kmeans.cluster_centers_)


# In[16]:


one = kmeans.cluster_centers_[0] #personality type 1


# In[17]:


two = kmeans.cluster_centers_[1] #personality type 2


# In[18]:


three = kmeans.cluster_centers_[2] #personality type 3


# In[19]:


four = kmeans.cluster_centers_[3] #personality type 4


# In[20]:


five = kmeans.cluster_centers_[4] #personality type 5


# In[21]:


six = kmeans.cluster_centers_[5] #personality type 6


# In[22]:


seven = kmeans.cluster_centers_[6] #personality type 7


# In[23]:


eight = kmeans.cluster_centers_[7] #personality type 8


# In[24]:


nine = kmeans.cluster_centers_[8] #personality type 9


# In[25]:


ten = kmeans.cluster_centers_[9] #personality type 10


# In[26]:


#Below will be the response of the individual with personality type onw


# In[27]:


one


# In[28]:


#Assuming we are dealing with Extraversion, to get the score we add and subtract according to the first question
#I am the life of the party. # you add
#I don't talk a lot. # you subtract
#I feel comfortable around people. #you add
#I keep in the background. #you subtract
#I start conversations. # you add
#I have little to say. # you subtract I have little to say. # you subtract
#I talk to a lot of different people at parties. # you add
#I don't mind being the center of attention. # you add
#I am quiet around strangers. # you subtract


# In[29]:


one_scores = {}

one_scores['extroversion_score'] = one[0] - one[1] + one[2] - one[3] + one[4] - one[5] + one[6] - one[7] + one[8] - one[9]
one_scores['neuroticism_score'] = one[0] - one[1] + one[2] - one[3] + one[4] + one[5] + one[6] + one[7] + one[8] + one[9]
one_scores['agreeableness_score'] = -one[0] + one[1] - one[2] + one[3] - one[4] - one[5] + one[6] - one[7] + one[8] + one[9]
one_scores['conscientiousness_score'] = one[0] - one[1] + one[2] - one[3] + one[4] - one[5] + one[6] - one[7] + one[8] + one[9]
one_scores['openness_score'] = one[0] - one[1] + one[2] - one[3] + one[4] - one[5] + one[6] + one[7] + one[8] + one[9]


# In[30]:


one_scores


# In[31]:


all_types = {'one': one, 'two' : two, 'three' : three, 'four' : four, 'five': five, 'six' : six, 'seven' : seven, 
             'eight' : eight,'nine' : nine, 'ten': ten}


# In[32]:


all_types_scores = {}

for name, personality_type in all_types.items():
    personality_trait = {}
    personality_trait['extroversion_score'] =  personality_type[0] - personality_type[1] + personality_type[2] - personality_type[3] + personality_type[4] - personality_type[5] + personality_type[6] - personality_type[7] + personality_type[8] - personality_type[9]
    personality_trait['neuroticism_score'] = personality_type[0] - personality_type[1] + personality_type[2] - personality_type[3] + personality_type[4] + personality_type[5] + personality_type[6] + personality_type[7] + personality_type[8] + personality_type[9]
    personality_trait['agreeableness_score'] = -personality_type[0] + personality_type[1] - personality_type[2] + personality_type[3] - personality_type[4] - personality_type[5] + personality_type[6] - personality_type[7] + personality_type[8] + personality_type[9]
    personality_trait['conscientiousness_score'] = personality_type[0] - personality_type[1] + personality_type[2] - personality_type[3] + personality_type[4] - personality_type[5] + personality_type[6] - personality_type[7] + personality_type[8] + personality_type[9]
    personality_trait['openness_score'] = personality_type[0] - personality_type[1] + personality_type[2] - personality_type[3] + personality_type[4] - personality_type[5] + personality_type[6] + personality_type[7] + personality_type[8] + personality_type[9]
    
    all_types_scores[name] = personality_trait
    
    
    


# In[33]:


all_types_scores


# In[34]:


all_extroversion = []
all_neuroticism = []
all_agreeableness = []
all_conscientiousness = []
all_openness = []

for personality_type, personality_trait in all_types_scores.items():
    all_extroversion.append(personality_trait['extroversion_score'])
    all_neuroticism.append(personality_trait['neuroticism_score'])
    all_agreeableness.append(personality_trait['agreeableness_score'])
    all_conscientiousness.append(personality_trait['conscientiousness_score'])
    all_openness.append(personality_trait['openness_score'])
    
    


# In[35]:


all_extroversion_normalized = (all_extroversion-min(all_extroversion))/(max(all_extroversion)-min(all_extroversion))
all_neuroticism_normalized = (all_neuroticism-min(all_neuroticism))/(max(all_neuroticism)-min(all_neuroticism))
all_agreeableness_normalized = (all_agreeableness-min(all_agreeableness))/(max(all_agreeableness)-min(all_agreeableness))
all_conscientiousness_normalized = (all_conscientiousness-min(all_conscientiousness))/(max(all_conscientiousness)-min(all_conscientiousness))
all_openness_normalized = (all_openness-min(all_openness))/(max(all_openness)-min(all_openness))




# In[36]:


all_extroversion_normalized


# In[37]:


all_neuroticism_normalized


# In[38]:


all_agreeableness_normalized


# In[43]:


counter = 0
nomalized_all_types_scores = {}

for personality_type, personality_trait in all_types_scores.items():
    normalized_personality_trait = {}
    normalized_personality_trait['extroversion_score'] = all_extroversion_normalized[counter]
    normalized_personality_trait['neuroticism_score'] = all_neuroticism_normalized[counter]
    normalized_personality_trait['agreeableness_score'] = all_agreeableness_normalized[counter]
    normalized_personality_trait['conscientiousness_score'] = all_conscientiousness_normalized[counter]
    normalized_personality_trait['openness_score'] = all_openness_normalized[counter]
    
    nomalized_all_types_scores[personality_type] = normalized_personality_trait
    counter+= 1
    
    


# In[44]:


nomalized_all_types_scores


# In[45]:


import matplotlib.pyplot as plt


# In[46]:


plt.figure(figsize =(15,5))
plt.ylim(0,1)
plt.bar(list(nomalized_all_types_scores['one'].keys()), nomalized_all_types_scores['one'].values(), color = 'y')


# In[47]:


plt.figure(figsize =(15,5))
plt.ylim(0,1)
plt.bar(list(nomalized_all_types_scores['two'].keys()), nomalized_all_types_scores['two'].values(), color = 'g')


# In[48]:


import pickle


# In[49]:


pickle.dump(kmeans, open('model.pkl', 'wb'))


# In[ ]:




