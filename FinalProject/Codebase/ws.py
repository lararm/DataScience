
# coding: utf-8

# # Data Science Jobs Analyze
# 

# Group:
# * Anchal
# * Angela
# * Larissa
# * Fabio
# * Felipe

# This program extracts data from Indeed.ca website to analyze main caracteristics 
# of Data Science Job opportunities in Toronto

# In[1]:


# Importing Libraries 
import numpy as np
import pandas as pd
import re 
import requests
import datetime
from bs4 import BeautifulSoup
import seaborn as sns


# In[2]:


# Defining some search Arguments
input_job = "Data Scientist"
# Add quotation marks("") to your input_job
input_quote = False 
# leave empty if input_city is not specified
input_city = "" 
input_state = "Canada"
sign = "+"
base_url_indeed =  'https://ca.indeed.com/' 


# In[3]:


# Functions
# Function for Transform searching keywords 
def transform(input,sign, quote = False):
    syntax = input.replace(" ", sign)
    if quote == True:
        syntax = ''.join(['"', syntax, '"'])
    return(syntax)

# Funtion to verify a specific Skill(KeyWord) int the Job Requirement attribute ("big String")        
def find_skill(skill, jobReq ):
    if skill in jobReq:
        return True
    else:
        return False

# Web Scraping Attributes
# Scraping the Salary
def Salary(soup):
    try:
        source = soup.find( attrs = {'class' : 'jobsearch-JobMetadataHeader-item'}).text
        source_first_letter = source[0:1]
        if source_first_letter == '$':
            salary = source
            return salary
        else:
            salary = 'Not Informed'
            return salary
    except:
        salary = 'Not Informed'
        return salary

# Scraping the Job Type    
def Job_Type(soup):
    try:
        source = soup.find( attrs = {'class' : 'jobsearch-JobMetadataHeader-item'}).text
        source_first_letter = source[0:1]
        if source_first_letter != '$':
            job_type = source
            return job_type
        else:
            job_type = 'Not Informed'
            return job_type
    except:
        job_type = 'Not Informed'
        return job_type

# Scraping the City    
def City(soup):
    try:
        position = soup.find( attrs = {'class' : 'icl-u-xs-mb--xs icl-u-xs-mt--none jobsearch-JobInfoHeader-title'})
        title_count = len(position.text)
        location_2 = soup.find('title')
        final = location_2.text.find('Indeed')
        city = location_2.text[title_count+3: final-3].split(',')[0]
        return city
    except:
        city = 'Not Informed'
        return city

# Scraping the Province    
def Province(soup):
    try:
        position = soup.find( attrs = {'class' : 'icl-u-xs-mb--xs icl-u-xs-mt--none jobsearch-JobInfoHeader-title'})
        title_count = len(position.text)
        location_2 = soup.find('title')
        final = location_2.text.find('Indeed')
        province = location_2.text[title_count+3: final-3].split(', ')[1]
        return province
    except:
        province = 'Not Informed'
        return province
    
# Scraping the Position    
def Position(soup):
    try:
        position_1 = soup_html.find(attrs = {'class' : 'icl-u-xs-mb--xs icl-u-xs-mt--none jobsearch-JobInfoHeader-title'})
        position = position_1.text
        return position
    except:
        position = 'Not Informed'
        return position
        
# Scraping the Job Requirement    
def Job_requirements (soup):
    try:
        general_1 = soup.find( attrs = {'class' : 'jobsearch-JobComponent-description icl-u-xs-mt--md'})
        general = general_1.text
        return general
    except:
        general = 'Not Informed' 
        return general

# Scraping the Company Name    
def Company_Name(soup):
    try:
        company_name_1 = soup.find( attrs = {'class' : 'icl-u-lg-mr--sm icl-u-xs-mr--xs'})
        company_name = company_name_1.text
        return company_name
    except:
        company_name = 'Not Informed'
        return company_name       


# In[4]:


# Generating Base Indeed URL
url_indeed_list = [ base_url_indeed, '/jobs?q=', transform(input_job, sign, input_quote), '&l=', input_state]
url_indeed = ''.join(url_indeed_list)


# In[5]:


# Get the HTML code from the URL
rawcode_indeed = requests.get(url_indeed)
# Choose "lxml" as parser
soup_indeed = BeautifulSoup(rawcode_indeed.text, "lxml")


# In[6]:


# Total number of results
num_total_indeed = soup_indeed.find(id = 'searchCount').contents[0].split()[-2]
# Remove non-numeric characters in the string
num_total_indeed = re.sub("[^0-9]","", num_total_indeed) 
num_total_indeed = int(num_total_indeed)
# Total number of pages
num_pages_indeed = int(np.ceil(num_total_indeed/11.0))
# Current date
now = datetime.datetime.now()
now_str = now.strftime("%m/%d/%Y")
now_str_name=now.strftime('%m%d%Y')


# In[7]:


# Looping all pages
# create an empty dataframe
df_base = pd.DataFrame()
for i in range(1, num_pages_indeed+1):
    # Generating the URL
    url = ''.join([url_indeed, '&start=', str(i*10)])
    # Getting the LXML
    rawcode = requests.get(url)
    soup_lxml = BeautifulSoup(rawcode.text, "lxml")
    # Pick out all the "div" with "class="job-row"
    divs = soup_lxml.findAll("div")
    job_divs = [jp for jp in divs if not jp.get('class') is None
                    and 'row' in jp.get('class')]
    # Looping all jobs for a specific page
    for job in job_divs:
        try:
            # Attribute Job Id
            id = job.get('data-jk', None)
            # Attribute Link related to job id
            link = base_url_indeed + '/viewjob'+ '?jk=' + id
            # Parsing the HTML
            r = requests.get(link)
            soup_html = BeautifulSoup(r.text, "html.parser")
            # Attribute Job Requirement
            jobrequirements = Job_requirements(soup_html)
            # Attribute Company Name 
            company = Company_Name(soup_html)           
            # Atribute City
            city = City(soup_html)
            # Atribute Province
            province = Province(soup_html)
            # Atribute Salary
            salary = Salary(soup_html)
            # Attribute Job Type
            jobtype = Job_Type(soup_html)
            # Attribute Position
            position = Position(soup_html)
        except:
            continue
        # Populating the base data frame    
        df_base = df_base.append({'Job_ID': id,
                                  'JobTitle': input_job,
                                  'JobType':jobtype,
                                  'CompanyName': company,
                                  'Salary' : salary,
                                  'Position':position,
                                  'City': city,
                                  'Province': province,
                                  'JobRequirements': jobrequirements,
                                  'Date': now_str,
                                  'From':"Indeed",
                                  'JobLink': link},
                                   ignore_index=True)


# In[8]:


# Correlating information from the base data frame and keyword table
# Reading the data sources skill and kewWord
skill_source = pd.read_excel('datasource/ds.xlsx', sheet_name='skill')
kw = pd.read_excel('datasource/ds_kw.xlsx')
# Defining a auxiliary data frame skill
df_skill_aux = pd.DataFrame(columns=['Job_ID', 'KeyWord', 'Skill_ID'])
# Lopping into the base data frame and checking all KeyWords related to the job requiremnt attribute ("Big String")
z = 0
for index, row in df_base.iterrows():
    k = kw.loc[kw.JobTitle == row["JobTitle"], ['KeyWord', 'Skill_ID']]
    jobReq = row["JobRequirements"]
    job_ID = row["Job_ID"]
    for idx, skills in k.iterrows():
        skill = ' ' + skills["KeyWord"]
        skill_ID = skills["Skill_ID"]
        func = find_skill(skill, jobReq)
        if func:
            df_skill_aux.loc[z] = [job_ID, skill, skill_ID]
            z += 1


# In[9]:


# Transforming and Cleaning the df_tmp to prepare the main data frame.
# Creating df_tmp
df_tmp = pd.DataFrame()
# Merging the Base Data Frame and Skill table
df_tmp = df_base.merge(df_skill_aux, how='left', left_on='Job_ID', right_on='Job_ID')
# Treating null values
values = {'Skill_ID': '-1', 'KeyWord': "Not found"}
df_tmp = df_tmp.fillna(value=values)
# Defing the Skill Id attribute as an Tnteger type
df_tmp['Skill_ID'] = df_tmp['Skill_ID'].astype(int)
# Dropping the Job Requirements colum. This column will not be used for analysis
df_tmp.drop(columns=['JobRequirements'])
# Preparing the main data frame: Meging the df_tmp and skill source table
df_jobs = df_tmp.merge(skill_source, left_on='Skill_ID', right_on='Skill_ID', how='left')
# Removing duplicated rows from the main data frame
df_jobs = df_jobs.drop_duplicates(subset={'Job_ID','Skill_ID'}, keep='first', inplace=False)
# Resetting the data frame index
df_jobs = df_jobs.reset_index(drop=True)
# df_jobs.head()
df_jobs = df_jobs[['Province', 'City', 'Job_ID', 'JobTitle_x', 'Position',  'CompanyName', 'JobType', 'Salary', 'KeyWord', 'Skill', 'Category']]


# In[10]:


# Exporting files
df_base.to_excel('output/out.xlsx')
df_jobs.to_excel('output/final_out.xlsx')


# In[11]:


# # Exporting the df_jobs to Sqlite DB (jobs table) 
# import sqlite3
# sqlite_file = '/Users/fabio.maia/Downloads/chinook/chinook.db'
# conn = sqlite3.connect(sqlite_file)
# df_b = df_base[['Province', 'City', 'Job_ID', 'Position',  'CompanyName', 'JobType', 'Salary', 'JobLink']]
# df = df_jobs[['Province', 'City', 'Job_ID', 'JobTitle_x', 'Position',  'CompanyName', 'JobType', 'Salary', 'KeyWord', 'Skill', 'Category']]
# df_b.to_sql("jobs_base", conn, if_exists='replace')
# df.to_sql("jobs", conn, if_exists='replace')
# conn.close()

