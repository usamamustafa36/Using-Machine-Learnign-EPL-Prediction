#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests


# In[3]:


standings_url = "https://fbref.com/en/comps/9/Premier-League-Stats"


# In[6]:


data = requests.get(standings_url) # It'll request the server to download the HTML of above URL


# In[7]:


data.text # It will get the complete HTML page String, but skipping this part as it wont be neccesary


# In[ ]:




