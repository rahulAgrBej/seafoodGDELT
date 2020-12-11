# Summarizing and Filtering Article information

## Instructions

## Getting the article tables
1. Open a terminal window on your computer
2. Write `tar -xzvf articleResults.tar.gz`

When completed you should now see a folder named articleResults. This is where all our article information lives.

## Filtering to specific article information

**Get all article information**
In your terminal run the command `python3 summarize.py`
You will now find a file called summary_table.csv with all the information you asked for.

**Getting articles based on criteria**
*Getting articles that relate to ONE countries*

1. Find the country code of the country you are interested in countryLookUp.csv (eg US)
2. Run the command `python3 summarize.py -c [INSERT COUNTRY CODE HERE]`

For example if I was interested in getting a table containing information on all articles that mention the US I would type:
`python3 summarize.py -c US`

You will now find a file called summary_table.csv with all the information you asked for.

*Getting articles that relate to TWO countries*
1. Find the country code of the countries you are interested in countryLookUp.csv (eg US, CH, etc)
2. Run the command `python3 summarize.py -c1 [INSERT FIRST COUNTRY CODE] -c2 [INSERT SECOND COUNTRY CODE]`

NOTE: that if you don't receive results please try to run the command reversing the order of country codes

For example if I was interested in getting a table containing information on all articles that mention the US and China I would type:
`python3 summarize.py -c1 US -c2 CH` OR 
`python3 summarize.py -c1 CH -c2 US`

*Getting articles that were published from a specific source country*
1. Find the country code of the country you are interested in countryLookUp.csv (eg US)
2. Run the command `python3 summarize.py -s [INSERT COUNTRY CODE HERE]`

For example if I was interested in getting a table containing information on all articles that were published my US sources I would type:
`python3 summarize.py -s US`

