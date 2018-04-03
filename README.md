# ElectionWebscraper
This simple script scrapes townhall.com and outputs the election results to csv, so it may be used for analysis.


The results are output to two csv files with the format below:

House results = ['Election','Year','State','District','Party','Candidate', 'Votes Received', 'Vote Percentage']
Other election results = ['Election','Year','State','County','Party','Candidate', 'Votes Received', 'Vote Percentage']

I am using this for some R projects and joining the data there. I may add that functionality back to this script,
as well as adding the census FIPS codes for the associated districts, but there is no guarantee I will get to that.

I have also not validated the results yet. 
