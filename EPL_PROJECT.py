#!/usr/bin/env python
# coding: utf-8

# In[12]:


import requests


# In[14]:


standings_url = "https://fbref.com/en/comps/9/2021-2022/2021-2022-Premier-League-Stats"


# In[15]:


data = requests.get(standings_url) # It'll request the server to download the HTML of above URL


# In[17]:


data.text # It will get the complete HTML page String, but skipping this part as it wont be neccesary


# In[19]:


from bs4 import BeautifulSoup


# In[21]:


soup = BeautifulSoup(data.text) # we will use beautiful soup library for parsing the html 


# In[23]:


standings_table = soup.select('table.stats_table')[0] # now here i will use the table tag from the URL HTML as shown in the ppt, stats_table is the class and we require only the first table because all the URLs of teams are in that table


# In[25]:


standings_table # now i have narrowed it down to the HTML of the table which have the URLs of the other teams


# In[30]:


# now i have to find all the anchor tags, for that u/m command will be used 
links = standings_table.find_all('a')


# In[31]:


# now we have to get the hypertext reference property of each link(a tag),
links = [l.get("href") for l in links]


# In[32]:


# we want each squad stats, now this command will check if that anchor tag link has the string squad in it'll display the link,otherwise it'll discard it
links = [l for l in links if '/squads/' in l]


# In[33]:


links


# In[34]:


# this command will concatenate this string with the a/m links
# we require the absolute links rather than the relative links 
team_urls = [f"https://fbref.com{l}" for l in links]


# In[35]:


team_urls


# In[36]:


# extracting arsenal stats
team_url=team_urls[4]


# In[37]:


#now we will extract the stats from the team URLs as per our own wish
data = requests.get(team_url)


# In[38]:


data.text


# In[39]:


import pandas as pd

# Assuming 'data' contains the HTML content
tables = pd.read_html(data.text)

for i, table in enumerate(tables):
    print(f"Table {i}:")
    print(table)




# In[40]:


desired_table = tables[1]


# In[41]:


desired_table 


# In[42]:


# now the stats from the scores and fixtures table is presented.However, to train my model, i require more stats. 
# for that i will again parse the URL of Arsenal

soup = BeautifulSoup(data.text)
links = soup.find_all('a')
links = [l.get("href") for l in links]
links = [l for l in links if l and 'all_comps/shooting/' in l]


# In[43]:


links
# these are the same links , now again we will again use beautiful soup, yes but first i'll concatenate


# In[46]:


data = requests.get(f"https://fbref.com{links[0]}")


# In[47]:


data.text


# In[48]:


shooting = pd.read_html(data.text, match="Shooting")[0]


# In[59]:


shooting.head()



# In[67]:


team_data = desired_table.merge(shooting[["Date", "Sh", "SoT", "Dist", "FK", "PK", "PKatt"]], on="Date")
# Here i can add any  other stats after running my model for better accuracy / precision


# In[68]:


team_data.head()


# In[70]:


rows, columns = shooting.shape
print(f"Number of rows: {rows}")
print(f"Number of columns: {columns}")


# In[72]:


rows, columns = desired_table.shape
print(f"Number of rows: {rows}")
print(f"Number of columns: {columns}")
# now there is difference in these tables that we have merged, which is fine because only intersected part is shown 


# In[78]:


rows, columns = team_data.shape
print(f"Number of rows: {rows}")
print(f"Number of columns: {columns}")


# In[81]:


years = list(range(2022, 2020, -1))
all_matches = []


# In[ ]:


years


# In[97]:


import time

for year in years:
    data = requests.get(standings_url)
    soup = BeautifulSoup(data.text)
    standings_table = soup.select(tables[1])
    links = [l.get("href") for l in standings_table.find_all('a')]
    links = [l for l in links if '/squads/' in l]
    team_urls = [f"https://fbref.com{l}" for l in links]

    for team_url in team_urls:
        team_name = team_url.split("/")[-1].replace("-Stats", "").replace("-", " ")
        data = requests.get(team_url)
        desired_table = pd.read_html(data.text, match="Scores & Fixtures")[0]

