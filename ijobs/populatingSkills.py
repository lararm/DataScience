import pandas as pd
import numpy as np
# from UoT_TermProject.ijobs.ds_excel import *

skill_source = pd.read_excel('ds.xlsx', sheet_name='skill')
kw_source = pd.read_excel('ds.xlsx', sheet_name='kw')

# Functions
def find_skill(skill, jobReq ):
    if skill in jobReq:
        return True
    else:
        return False


# a = find_string(' R', 'AAA Python bbbb xptoR a to NumPy uuu R jjj Math pppp')
# print(a)

df_base = pd.DataFrame(dict(Job_ID=['1','2'],
                       JobTitle=['Data Science', 'Java Developer'],
                       CompanyName=['IBM', 'Accenture'],
                       Salary=['70K', '60'],
                       City=['Toronto', 'Vancouver'],
                       Province=['ON', 'BC'],
                       JobRequirements=['AAA Python bbbb xpto Mathematcs a to NumPy uuu x zzz Math pppp', 'AAA Python bbbb xpto a to SQL uuu x BigData Stats pppp']),
                       index=[0, 1])

df_skill_aux = pd.DataFrame(columns=['ID', 'KeyWord', 'Skill_ID'])

z = 0
for index, row in df_base.iterrows():
    k = kw_source.loc[kw_source.JobTitle == row["JobTitle"], ['KeyWord', 'Skill_ID']]
    jobReq = row["JobRequirements"]
    job_ID = row["Job_ID"]

    for idx, skills in k.iterrows():
        skill = ' ' + skills["KeyWord"]
        skill_ID = skills["Skill_ID"]
        func = find_skill(skill, jobReq)
        if func:
            # print(job_ID, skill, skill_ID)
            df_skill_aux.loc[z] = [job_ID, skill, skill_ID]
            z += 1


df_tmp = df_base.merge(df_skill_aux, how='left', left_on='Job_ID', right_on='ID')

print(df_tmp)














