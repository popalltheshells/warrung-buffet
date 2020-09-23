# warung-buffet
Hello All, Ignatius here.
I was bored one day and decided to create a messy code for automation process that aggregates different stock analyst ratings from different sources.

Everything is messy, done in python. I had a plan to polish it and add more resources, but I haven't had the time to do it because of other projects that I have. Decided to make it open source and if there's anyone who wants to contribute, please do let me know. 

Note that there are still some bugs, but other than that, the code can be ran using python
usage: python3 ./warrung-buffet.py

Don't be a sheep and follow these ratings when investing in stocks, this is just gonna give you a better idea of the current state of the stock.


##############################
####### WARUNG-BUFFET ########
#### By: Ignatius Michael ####
##############################
                                                    

This script was made because I was too lazy to do research on stock consensus rating.				  					   
This script automates that and more. Please enjoy. This is called warung buffet because it's another version of "Warren Buffet" that old legend.	   
However, this script does not have the ability to think like he does.						                                           
Pretty much the rip off version of warren = warung (which is what we call an insanely good street-side 'restaurants' in Indonesia)		  	   
###########################################
1. thestockmarketwatch.py is to grab consensus rating from thestockmarketwatch.com but only works for NASDAQ and NYSE
2. warung-buffet.py is the main script to grab information from marketbeat.com (rating, price, gain/loss, how many times it has been analyzed)
3. tipranks.py is to grab the consensus rating from tipranks.com works for any stock exchange
