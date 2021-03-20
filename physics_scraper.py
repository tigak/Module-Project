import requests
from bs4 import BeautifulSoup
import pandas as pd

#URL for physics modules
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
    lambda row: get_pre_reqs(row['Links'])[0], axis=1)
physics_modules['Co-requisites'] = physics_modules.apply(
    lambda row: get_pre_reqs(row['Links'])[1], axis=1)

# Export scraped data to a csv file
physics_modules.to_csv('physics.csv')
