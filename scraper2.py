import requests
import re
from bs4 import BeautifulSoup
import pandas as pd

PHYSICS = 'https://newton.ex.ac.uk/handbook/modules/'

page = requests.get(PHYSICS).text

soup = BeautifulSoup(page, 'lxml')
title = soup.h3.text
names = []
urls = []
code = []
for li in soup.find_all('li'):
    module = li.a.text
    link = 'https://newton.ex.ac.uk/handbook/modules/' + module + '.html'
    name = li.text
    names.append(name)
    code.append(module)
    urls.append(link)
filt_names = []
for name in names:
    name = name[8:]
    filt_names.append(name)


def get_descriptor(link):
    page = requests.get(link).text
    soup = BeautifulSoup(page, 'lxml')
    description = soup.body.p.text
    return description


def get_pre_reqs(link):
    requisites = []
    page = requests.get(link).text
    soup = BeautifulSoup(page, 'lxml')
    table = soup.body.find_all('table')[3]
    for reqs in table.find_all('td'):
        requisites.append(reqs.text)
    pre_req = requisites[0]
    co_req = requisites[1]
    return pre_req, co_req


physics_modules = pd.DataFrame(code, columns=['Module Code'], index=None)
physics_modules['Links'] = urls
physics_modules['Module_Name'] = filt_names
physics_modules = physics_modules.drop(index=[0])

physics_modules['Descriptors'] = physics_modules.apply(
    lambda row: get_descriptor(row['Links']), axis=1)
physics_modules['Pre-requisites'] = physics_modules.apply(
    lambda row: get_pre_reqs(row['Links']), axis=1)
# descriptors = []
# for row in physics_modules:
#     get_descriptor(physics_modules['Links'])


# year1 = []
# year2 = []
# year3 = []
# for row in physics_modules['Module_Name']:
#     if row.startswith('PHY1'):
#         year1.append(row)
#     elif row.startswith('PHY2'):
#         year2.append(row)
#     elif row.startswith('PHY3'):
#         year3.append(row)


print(physics_modules.head())
