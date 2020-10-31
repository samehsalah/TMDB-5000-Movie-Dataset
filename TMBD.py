#!/usr/bin/env python
# coding: utf-8

# 
# # Project: Investigate TMBD Dataset
# 
# ## Table of Contents
# <ul>
# <li><a href="#intro">Introduction</a></li>
# <li><a href="#wrangling">Data Wrangling</a></li>
# <li><a href="#eda">Exploratory Data Analysis</a></li>
# <li><a href="#conclusions">Conclusions</a></li>
# </ul>

# <a id='intro'></a>
# ## Introduction
# This data set contains information about 10,000 movies collected from The Movie Database (TMDb), including user ratings and revenue and we will dive into this data set to know what is properties of successful movies by answering the follwing question :
# ### <li><a href="#q1"> Which genres are most popular from year to year?</a></li>
# ###  <li><a href="#q2"> What kinds of properties are associated with movies that have high revenues?</a></li>

# In[1]:


import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

get_ipython().run_line_magic('matplotlib', 'inline')


# In[2]:


df=pd.read_csv('tmdb-movies.csv')
df.head()


# <a id="wrangling"></a>
# ## Cleaning Data:
# <ul>
#     <li>get type for each column to explore columns</li>
#     <li>Delete duplicated rows</li>
#     <li>Drop unnessecary columns</li>
#     <li>plot a histogram to make visual view for numeric data</li>
# </ul>

# In[3]:


df.info()


# In[4]:


df.drop_duplicates(inplace=True) #drop duplicated columns 


# In[5]:


df.duplicated().sum() #insure that it is deleted from datframe


# In[6]:


#drop unnessasery columns
df.drop(['homepage', 'tagline','keywords','production_companies','imdb_id','overview','budget','revenue'], axis=1,inplace=True)


# In[7]:


df.shape #insure that colums are deleted


# <a id='eda'></a>
# ## Explanatory data Analysis

# In[8]:


df.describe()


# In[9]:


df.hist(figsize=(15,15));


# ## Q1 : Which genres are most popular from year to year?
# <li> first we calculate the frequncy of each gener over years to discover which gener is more repeated (i assumed that if movie with certain geners is sucess they will produce it over years)</li>
# <li> second we will take mean of popularity for each gener for each year over year </li>

# In[10]:


df = df[df["genres"].isnull() == False]  #choose only no null values for geners


# In[11]:


df.shape


# In[12]:


df['genres'].value_counts() #take a look about what is a unique value for each gener


# <b> We have a problem that in gener field there is more than one gener so we will split by using str.split which return a list of generes </b>

# In[13]:


df["genres"] = df["genres"].str.split('|') #split geners column


# In[14]:


df["cast"] = df["cast"].str.title()  #make all name title 
df["cast"] = df["cast"].str.split('|') #also split cast column (we will use it in second question)


# In[15]:


df["director"] = df["director"].str.title()
df["director"] = df["director"].str.split('|')


# In[16]:


#get unique years to use it as key of dictionary (key : years , value: frequancies) 
unique_years = df['release_year'].unique().tolist()
unique_years.sort() #sort years Ascendind


# In[17]:


df_geners_and_years = df[['genres','release_year']]


# In[18]:


#print (unique_years)
#make dictinary for every year contain the number appear this gener in this year
#this cell and the next two cell is to convert dictinary to data frame 
year_gener_dict= {}
for year in unique_years :
    df_geners_and_years = df[['genres','release_year']]
    df_geners_and_years = df_geners_and_years[df_geners_and_years['release_year']==year]
    year_gener_dict[year]={}
    for index, value in df_geners_and_years['genres'].items():
             for item in value:
                  if item in year_gener_dict[year]:
                        year_gener_dict[year][item] +=1
                  else:
                        year_gener_dict[year][item]=1


# In[19]:


years_as_index = unique_years
g_df_columns = []
for year in years_as_index:
    for k,v in year_gener_dict[year].items():
        if k not in g_df_columns:
            g_df_columns.append(k) 


# In[20]:


geners_dict ={}
for col in g_df_columns :
    geners_dict[col] = []
for year in years_as_index:
    for gener in geners_dict:
        if gener in year_gener_dict[year]:
            geners_dict[gener].append(year_gener_dict[year][gener])
        elif gener not in year_gener_dict[year]:
            geners_dict[gener].append(0)


# In[21]:


#make a new data frame contains only years as index and geners are column data are teh frequancies
years_and_geners_df = pd.DataFrame(data=geners_dict,index=years_as_index)


# In[22]:


#change geners over years
years_and_geners_df.plot.bar(stacked=True, figsize=(20,15),title='number of gener over years');


# In[23]:


years_and_geners_df.describe()


# <b>From the previous graph and statistic we observe that drama is the most frequent gener but it does not mean is the most popular gener beacuse as we notice there are a many combination of geners for the single movie  </b><br/>
# 
# <b>so we will use mean of popularity score to know what is the most popular gener over years  </b>
# 

# In[24]:


geners = years_and_geners_df.columns  #get genres as a list 
popularity_rate_over_years ={} #make dict for popularity mean
years_for_pop_geners = {} #dict for corresponding year (gener may appear in year and not appear in another)
for gener in geners:
    popularity_rate_over_years[gener] = df[df['genres'].apply(lambda x :True if gener in x else False )==True].groupby('release_year').mean()['popularity'].tolist()
    years_for_pop_geners[gener] = df[df['genres'].apply(lambda x :True if gener in x else False )==True].groupby('release_year').mean().index


# In[25]:


#use the previous two dictionary and matplot to draw stacked bar 
plt.style.use('fivethirtyeight')

colors = ['black','springgreen','red','blue','green','gray','black','lime','teal','orange','burlywood','coral','cyan','darkkhaki','darkseagreen','darkturquoise','greenyellow','indigo','lightgray','magenta','salmon']
# Fixing random state for reproducibility
fig, ax = plt.subplots(figsize=(25,20))
i=0
for gener in geners:
    i+=1
    ax.bar(years_for_pop_geners[gener],popularity_rate_over_years[gener],label=gener,color=colors[i])    
plt.legend(loc='upper left')

ax.set_title("popularity_rate_over_years")

plt.show()


# <li> in 60'S Animation movies is the most popular <br/></li>
# <li> in 70's Tv movies take the lead i think because TV invented in the last of 60's</li>
# <li> in 80 's Mystery movies is most popular  </li>
# <li>90's Mystery and Animation take the lead </li>
# <li>2000 -2015  Mystery and fantasy is the most popular movies</li>
# 

# <b>even though Drama is most frequencies over years but it isn’t the most popular that is mean drama with combination with other geners like Action and Adventure make a good movie </b>

# <a id="q2"></a>
# ## Q2 : What kinds of properties are associated with movies that have high revenues?

# to answer this question, we make the following steps:<br/>
# 1- sort data frame according to revenue_adj column<br/>
# 2- Select top 50 movie then compare with whole data frame statistical
# 

# In[26]:


#sort df according to revenue_adj
top_50 = df.sort_values(by='revenue_adj',ascending=False).head(50)


# In[27]:


top_50.describe() #get descriptive statstics to top 50 movies data frame


# <b> dependent variable is "revenue_adj"<br/> 
# independents variables are :<br/>
# 1-budget_adj<br/>
# 2-popularity<br/>
# 3-geners<br/>
# 4-runtime<br/> </b>

# In[28]:


#revenue_adj vs budget_adj
df.plot.scatter(x='budget_adj',y='revenue_adj',figsize=(8,6),grid=False);


# In[29]:


df.plot.scatter(x='popularity',y='revenue_adj',figsize=(8,6),grid=False);


# In[30]:


df.plot.scatter(x='runtime',y='revenue_adj',figsize=(8,6),grid=False);


# In[31]:


indep_vs_dep_df = df[['revenue_adj','budget_adj','popularity','runtime']]
indep_vs_dep_df.corr()


# In[32]:


#digram for correlation 
plt.matshow(indep_vs_dep_df.corr())
plt.show()


# Observation <br/>
# <li>budget and revenue has an positive correlation about r=0.646507 </li>
# <li>And it does make sense when revenue increase the popularity increased with r=0.608964 </li>
# <li>but there is the weak correlation between runtime and revenue, the runtime means about 130 minutes <br/>that is means most       successful has long run time than other movies mean of 
#     all movies = 102 minutes otherwise mean of top_50 is 136 min </li>
# 

# ## Question : is there is a certain geners common in the top 50 movies<br/>
# ### we will see which geners most appear in top 50 movies
# 

# In[33]:


geners = years_and_geners_df.columns
popularity_rate_over_years ={}
years_for_pop_geners = {}
for gener in geners:
    popularity_rate_over_years[gener] = df[df['genres'].apply(lambda x :True if gener in x else False )==True].groupby('release_year').mean()['popularity'].tolist()
    years_for_pop_geners[gener] = df[df['genres'].apply(lambda x :True if gener in x else False )==True].groupby('release_year').mean().index


# In[34]:


geners = years_and_geners_df.columns
top_50_geners={}
for gener in geners:
        top_50_geners[gener]=top_50[top_50['genres'].apply(lambda x :True if gener in x else False )==True].count()['id']


# In[35]:


top_50_geners_df = pd.DataFrame({'Frequency':list(top_50_geners.values())},index=top_50_geners.keys())


# In[36]:


top_50_geners_df.plot.bar(figsize=(10,8),title='the most repeated gener');


# <b> observation <br/></b>
# <b> Adventure movies is the most geners in top 50 movies then Action and so on </b>

# ###  Also we will compare budget of top 50 movies with the mean budget for all movies to see if really budget is effect on movie success 

# In[37]:


top_50[top_50['budget_adj']>=df['budget_adj'].mean()].count()


# <b>observation 
# all top 50 movies have budget greater than the mean of all movies what is make sense </b>

# ### Question : Is there is a director or actor make movie which get more revenue ?

# In[38]:


directors_dict = {}     #create an empty dictionary (key is director name and value is the number of movies creaated by him)
for director_list in top_50['director'].tolist():
    if type(director_list)==list:
        for director in director_list:
            if director in directors_dict:
                directors_dict[director] += 1
            else:
                directors_dict[director] =1
    else:
         if director in directors_dict:
                directors_dict[director] += 1
         else:
              directors_dict[director] =1
                


# In[39]:


#create data frame for the frequancies dictionary
top_50_director_df=pd.DataFrame({'Frequency':list(directors_dict.values())},index=directors_dict.keys()) 


# In[40]:


top_50_director_df.plot.bar(figsize=(15,15),title='number of movies for each Drector');


# <h2>Observation:</h2>
# <b> Peter Jackson,Steven Spielberg make 16% from top 50 movies which may be an indicator that director affect on movie revenus</b> 

# In[41]:


actress_dict = {}
for actress_list in top_50['cast'].tolist():
    if type(actress_list)==list:
        for actor in actress_list:
            if actor in actress_dict:
                actress_dict[actor] += 1
            else:
                actress_dict[actor] =1
    else:
         if actor in actress_dict:
                actress_dict[actor] += 1
         else:
                actress_dict[actor] =1
                


# In[42]:


top_50_acctress_df = pd.DataFrame({'Frequency':list(actress_dict.values())},index=actress_dict.keys())


# In[43]:


top_50_acctress_df.plot.bar(figsize=(30,30),title='number of movies for each actor');


# In[44]:


#the name of actress contribures in more than 3 movies 
top_50_acctress_df[top_50_acctress_df['Frequency']>3]


# In[45]:


top_50_acctress_df[top_50_acctress_df['Frequency']>3].sum()


# <h2> Observation :</h2>
# <b>only 9 performars contribute 80% of the successful movies which is a good indicator that actor is an important factor to success the movie </b>

# <a id='conclusions'></a>
# ## conclusions :
# <font color = 'blue'><b> we use expletory data analysis in this project to try to know what is the properties of the success movies:</font><br/>
# 1- Big budget make a good movies and then make more revenue <br/>
# 2- runtime for succsful movies between 136 to 153 minutes <br/>
# 3- the geners for first three movies are [Action, Adventure, Fantasy, Science Fiction] , [Adventure, Action, Science Fiction],[Drama, Romance, Thriller] that is mean the combination of geners make a good movie<br/>
# 4- good director and cast  is a basic factor to make a good movie </b>
# 

# Resorces:<br/>
# 1- Dataquest.io <br/>
# 2-Python documentation <br/>
# 3-stack overflow <br/>
# 4-pandas & matplotlib documentation<br/>
