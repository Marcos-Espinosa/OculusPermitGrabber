#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import requests
import os
import re
import time


# In[4]:


def clear():
    # for windows
    if os.name == 'nt':
        _ = os.system('cls')
    
    else:
        _ = os.system('clear')


# In[5]:


def get_facility_csv():
    while True:
        facility_id = input('Enter facility ID: ')
        if not re.match("^(FL.\d{6})",facility_id):
            print("Error please try again. Facility ID should look like FL1234567")
        else:
            break
    csv_url = 'https://prodenv.dep.state.fl.us/DepNexus/public/electronic-documents/{}/export?wildCardMatch=false&page=1'.format(facility_id)

    csv_download = requests.get(csv_url)
    open(facility_id + ' Files.csv','wb').write(csv_download.content)
    file = facility_id + ' Files.csv'

    return file


# In[1]:


def grab_Permits():
    Permits = df[df['DOCUMENT TYPE'] == 'PERMIT - FINAL']
    Permits = Permits.reset_index()
    
    for index,row in df.iterrows():
        if index <= 50:
            if 'permit' in row['SUBJECT'].lower():
                print('Downloaded {} to folder.'.format(row['SUBJECT']))
                response = requests.get(row['FILE PATH'])
                open(row['DOCUMENT DATE'] + '.pdf','wb').write(response.content)
                time.sleep(1)


# In[2]:


def grab_DMRs():
    DMRs = df[df['DOCUMENT TYPE'] == 'DISCHARGE MONITORING REPORTS RELATED']
    DMRs = DMRs.reset_index()
    DMRs['DOCUMENT DATE'] = pd.to_datetime(DMRs['DOCUMENT DATE']).dt.date

    for index,row in DMRs.iterrows():
        if index <= 50:
            #print (index)
            #print(row['SUBJECT'])
            #print(row['FILE PATH'])
            if 'PART B' in row['SUBJECT']:
                print('Downloaded {} to folder.'.format(row['SUBJECT']))
                response = requests.get(row['FILE PATH'])
                open(str(row['DOCUMENT DATE']) + '_' + row['SUBJECT'] + '.pdf','wb').write(response.content)
                time.sleep(1)


# In[15]:


print("Welcome to the Oculus Permit Grabber")
print("This tool will help you download permits and DMRs for WWTF in Florida")
input("Press Enter to Continue")
clear()

while True:
    file = get_facility_csv()
    df = pd.read_csv(file,on_bad_lines='skip')
    print(df.head())
    check = input("Does this look like the right WWTF? Enter Y or N")   
    if check.lower() == 'y':
        input("Perfect! Let's proceed. Press Enter to continue")
        clear()
        break
    elif check.lower() == 'n':
        print("Let's try that again.")
        clear()
        os.remove(file)
        continue


# In[9]:


def still_using():
    selection = input("Would you like to grab different documents from this WWTF? Enter Y or N")

    try:
        if selection.lower() == 'y':
            return True
        elif selection.lower() == 'n':
            print('Thanks for using the Oculus Permit Grabber')
            return False
    except:
        print('Sorry that is not a valid input.')


# In[12]:


using = True

while using:
    
    try:
        choice = input('Would you like to 1. Grab Permits or 2. DMRs for this plant? Enter 1 or 2')
    except:
        print('Sorry that is not a valid choice. Enter 1 or 2')
        
    if int(choice[0]) == 1:
        print("Let's grab those permits!")
        grab_Permits()
        using = still_using()
    if int(choice[0]) == 2:
        print("Let's grab those DMRs!")
        grab_DMRs()
        using = still_using()


# In[ ]:




