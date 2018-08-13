'''
Election_Webscraper.py
Author: Tyler Jubenville
Apr 2 2018

This script uses beatiful soup and the requests module to parse through the election 
results on townhall.com for national election results. The results are then output to
user defined csv files.
'''
#TODO Add functionality to pass elections, years, and states into the funtions as parameters.
def main():
    houseResultsPath = "G:/Projects/Election_Webscraper_Final/Election_Webscraper/Data/HouseResults.csv"
    otherResultsPath = "G:/Projects/Election_Webscraper_Final/Election_Webscraper/Data/ElectionResults.csv"
    houseScraper(houseResultsPath)
    electionScraper(otherResultsPath)

def houseScraper(savepath):
    '''
    This function scrapes election results from townhall.com and outputs them to the csv file defined in savepath.
    savepath should be in the format "Path/filename.csv"

    '''
    import bs4
    import requests
    import pandas as pd
    import numpy as np

    baseUrl = 'https://townhall.com/election/'

    Results = pd.DataFrame(columns= ['Election','Year','State','District','Party','Candidate', 'Votes Received', 'Vote Percentage'])
    District = 'Undeclared'

    Election = ['house']
    Years = ['2004', '2005','2006', '2007', '2008', '2009', '2010', '2012', '2014', '2016']
    States = ['AK', 'AL', 'AR', 'AZ', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'IA', 'ID',
             'IL', 'IN', 'KS', 'KY', 'LA', 'MA', 'MD', 'ME', 'MI', 'MN', 'MO', 'MS', 'MT', 'NC', 'ND', 'NE', 'NH', 'NJ',
            'NM', 'NV', 'NY', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VA', 'VT', 'WA', 'WI', 'WV', 'WY']

    errors = []
    for elec in Election:
        for year in Years:
            for state in States:

                Url = baseUrl + year + '/results/' + state 
                
                res = requests.get(Url)
                res.raise_for_status
                soup = bs4.BeautifulSoup(res.text,"html5lib")
                temp = soup.find_all('tbody')
                data = []
                test = []
                i = 0
           
                for body in temp:
                    j = 0
                    for child in body.children:
                        try:
                            try:
                                val = child.div
                            except:
                                val = None

                            if (val != None):
                                District = val.text
                                CandData = child.find_all('td')
                                k=0
                                for line in CandData:                                
                                    if ' wf' in str(line):
                                        if k == 1:
                                            index = str(line).find(' wf')
                                            Party = str(line)[index-3:index]
                                            Candidate = str(line.text).strip()
                                        elif k == 2:
                                            Votes = str(line.text).strip().replace(',','')
                                        elif k == 3:
                                            VotePercent = str(line.text).strip().replace('%','')
                                    k+=1
                                if Party == 'her':
                                    Party = 'Other'
                                #print('County: {}, Party: {}, Candidate: {}, Votes: {}, VotePercent: {}'.format(District,Party,Candidate,Votes,VotePercent))
                                if "District" in District:
                                    data.append([elec,year,state,District,Party,Candidate,Votes, VotePercent])
                            else:
                                if ' wb' in str(child):
                                    CandData = child.find_all('td')
                                    k=0
                                    for line in CandData:
                                        if ' wb' in str(line):
                                            if k == 0:
                                                index = str(line).find(' wb')
                                                Party = str(line)[index-3:index]
                                                Candidate = str(line.text).strip()
                                            elif k == 1:
                                                Votes = str(line.text).strip().replace(',','')
                                            elif k == 2:
                                                VotePercent = str(line.text).strip().replace('%','')
                                        k+=1
                                    if Party == 'her':
                                        Party = 'Other'
                                    #print('County: {}, Party: {}, Candidate: {}, Votes: {}, VotePercent: {}'.format(District,Party,Candidate,Votes,VotePercent))
                                    if "District" in District:
                                        data.append([elec,year,state,District,Party,Candidate,Votes, VotePercent])
                            j+=1
                        except:
                            errors.append(str(child))
                    i+=1
                CountyDF = pd.DataFrame(data, columns= ['Election','Year','State','District','Party','Candidate', 'Votes Received', 'Vote Percentage'])
                Results = Results.append(CountyDF,ignore_index=True)
    print(errors)
    Results.to_csv(savepath)
def electionScraper(savepath):
    '''
    This function scrapes election results from townhall.com and outputs them to the csv file defined in savepath.
    savepath should be in the format "Path/filename.csv"

    '''
    import bs4
    import requests
    import pandas as pd
    import numpy as np

    baseUrl = 'https://townhall.com/election/'

    Election = 'President'
    Year = '2016'

    Results = pd.DataFrame(columns= ['Election','Year','State','County','Party','Candidate', 'Votes Received', 'Vote Percentage'])
    County = 'Undeclared'

    Election = ['president', 'senate', 'governor']
    Years = ['2004', '2005','2006', '2007', '2008', '2009', '2010', '2012', '2014', '2016']
    States = ['AK', 'AL', 'AR', 'AZ', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'IA', 'ID',
             'IL', 'IN', 'KS', 'KY', 'LA', 'MA', 'MD', 'ME', 'MI', 'MN', 'MO', 'MS', 'MT', 'NC', 'ND', 'NE', 'NH', 'NJ',
            'NM', 'NV', 'NY', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VA', 'VT', 'WA', 'WI', 'WV', 'WY']

    errors = []
    for elec in Election:
        for year in Years:
            for state in States:
                Url = baseUrl + year + '/' + elec + '/' + state +'/county'
                res = requests.get(Url)
                res.raise_for_status
                soup = bs4.BeautifulSoup(res.text,"html5lib")
                temp = soup.find_all('tbody')
                data = []
                test = []
                i = 0
           
                for body in temp:
                    j = 0
                    for child in body.children:
                        try:
                            try:
                                val = child.div
                            except:
                                val = None
                            if (val != None):
                                County = val.text
                                CandData = child.find_all('td')
                                k=0
                                for line in CandData:                                
                                    if ' wf' in str(line):
                                        if k == 1:
                                            index = str(line).find(' wf')
                                            Party = str(line)[index-3:index]
                                            Candidate = str(line.text).strip()
                                        elif k == 2:
                                            Votes = str(line.text).strip().replace(',','')
                                        elif k == 3:
                                            VotePercent = str(line.text).strip().replace('%','')
                                    k+=1
                                data.append([elec,year,state,County,Party,Candidate,Votes, VotePercent])
                            else:
                                if ' wb' in str(child):
                                    CandData = child.find_all('td')
                                    k=0
                                    for line in CandData:
                                        if ' wb' in str(line):
                                            if k == 0:
                                                index = str(line).find(' wb')
                                                Party = str(line)[index-3:index]
                                                Candidate = str(line.text).strip()
                                            elif k == 1:
                                                Votes = str(line.text).strip().replace(',','')
                                            elif k == 2:
                                                VotePercent = str(line.text).strip().replace('%','')
                                        k+=1
                                    #print('County: {}, Party: {}, Candidate: {}, Votes: {}, VotePercent: {}'.format(County,Party,Candidate,Votes,VotePercent))
                                    data.append([elec,year,state,County,Party,Candidate,Votes, VotePercent])
                            j+=1
                        except:
                            errors.append(str(child))
                    i+=1
                CountyDF = pd.DataFrame(data, columns= ['Election','Year','State','County','Party','Candidate', 'Votes Received', 'Vote Percentage'])
                Results = Results.append(CountyDF,ignore_index=True)    
    print(errors)      
    Results.to_csv(savepath)

main()  

