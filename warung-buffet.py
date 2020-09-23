#!/bin/python

import requests
import os
import tempfile
import re
import time


stonk = """
                                                                                                           88         
                                                                              ,d                           88         
                                                                              88                           88         
                                                                  ,adPPYba, MM88MMM ,adPPYba,  8b,dPPYba,  88   ,d8   
                                                                  [8[    ""   88   a8"     "8a 88P'   `"8a 88 ,a8"    
                                                                   `"Y8ba,    88   8b       d8 88       88 8888[      
                                                                  aa    ]8I   88,  "8a,   ,a8" 88       88 88`"Yba,   
                                                                  `"YbbdP"'   "Y888 `"YbbdP"'  88       88 88   `Y8a  
                                                                                                                      
                                                                                 by: Ignatius Michael
    

                                         __    __   ____  ____   __ __  ____    ____      ____   __ __  _____  _____   ___  ______ 
                                        |  T__T  T /    T|    \ |  T  T|    \  /    T    |    \ |  T  T|     ||     | /  _]|      T
                                        |  |  |  |Y  o  ||  D  )|  |  ||  _  YY   __j    |  o  )|  |  ||   __j|   __j/  [_ |      |
                                        |  |  |  ||     ||    / |  |  ||  |  ||  T  |    |     T|  |  ||  l_  |  l_ Y    _]l_j  l_j
                                        l  `  '  !|  _  ||    \ |  :  ||  |  ||  l_ |    |  O  ||  :  ||   _] |   _]|   [_   |  |  
                                         \      / |  |  ||  .  Yl     ||  |  ||     |    |     |l     ||  T   |  T  |     T  |  |  
                                          \_/\_/  l__j__jl__j\_j \__,_jl__j__jl___,_j    l_____j \__,_jl__j   l__j  l_____j  l__j  
                                                                                               



"""
class bcolors:
        HEADER = '\033[95m'
        OKBLUE = '\033[94m'
        OKGREEN = '\033[92m'
        WARNING = '\033[93m'
        FAIL = '\033[91m'
        ENDC = '\033[0m'
        BOLD = '\033[1m'
print(bcolors.HEADER+stonk+bcolors.ENDC)
#marketbeat results
se = input(f"{bcolors.BOLD}Which stock exchange (type exit to exit the program): {bcolors.ENDC}")
while se == "":
    se = input("Which stock exchange: ")
symbol = str(input(f"{bcolors.BOLD}Enter stock symbol e.g WMT, AAPL, etc. or MARKET:SYMBOL for a more accurate result: {bcolors.ENDC}"))
while symbol == "":
    symbol = str(input("Enter stock symbol e.g WMT, AAPL, etc. or MARKET:SYMBOL for a more accurate result: "))

#program_reset = int() #keep track if stock symbol or both uncrecognized, change status to 1, else 0
def submitdata(se, symbol):
    global stock_search
    stock_search = se + ":" + symbol #This is the full name to be submitted on search function se = NYSE, symbol = CGX. Becomes NYSE:CGX
    print(bcolors.WARNING+'++++++++++++++++++++++++++++++++++++++++++++++++'+bcolors.ENDC)
    website1 = "https://www.marketbeat.com/pages/search.aspx?"
    parameters = {'query':stock_search}
    r = requests.get('https://www.marketbeat.com/pages/search.aspx?', params = parameters) #Submitting GET request with stock entered by user to marketbeat website
    global results
    results = r.text #read the server response and populate varibale results
    global temp
    temp = tempfile.NamedTemporaryFile(mode="w+")
    temp.write(results) #writing the results to a temporary file
    temp.seek(0)
    global array_loc
    array_loc = 0 #variable set to find in which location the name, price, etc of the stock is within the response
    global current_lg
    current_lg = "" #current loss/gain tracker
    global rating
    rating = int() #rating counter 0 is hold, more than 0 is buy, less than 0 is sell
    global buy_rate
    buy_rate = 0
    global sell_rate
    sell_rate = 0
    global hold_rate
    hold_rate = 0
    global ipo
    ipo = ""
    global current_price
    current_price = ""
    global rating_checker
    rating_checker = int()
    global current_rating
    current_rating = ""
    global price_null
    price_null = int()

def getname(symbol):
    #Parsing the name of the stock a user entered e.g WMT will show "NASDAQ:WMT"
    with open(temp.name, 'r') as filehandle:
        info = filehandle.readlines()
        for i in info:
            if re.match(r""+se+"\:"+symbol, i):
            #if re.match(r".*\(\b[A-Z]{3,}\b\:"+symbol,i): #Finding if there is a match, if user enters the wrong symbol, it will show blank (additional if statement needed to show error)
                global array_loc 
                array_loc = (info.index(i))
                break
    ipo = re.sub(r"\).*\n", '', info[array_loc]) #parsing for name format
    ipo = re.sub(r".*\(", '', ipo) #parsing for name format V2
    filehandle.close()
    #print(info[array_loc])
    print (bcolors.HEADER+"Fetching information for "+stock_search+bcolors.ENDC) #recently changed from +ipo to +symbol -> IPO is full name e.g NSYE:BAM.A, SYMBOL is what the user entered

#Time delay to look fancy
time.sleep(2)

def getprice():
    #Grabbing the latest price for the aforementioned stock
    global program_reset
    program_reset = 0
    with open(temp.name, 'r') as filehandle:
        info = filehandle.readlines()
        for i in info:
            if re.match(r".*As of [0-9]{2}\/[0-9]{1,}\/[0-9]{4}.*",i):
                array_loc = (info.index(i))
                #price_null = 1
                #print(info[array_loc])
                program_reset = 1 
                break
            else:
                program_reset = 1
                array_loc = None

    if array_loc is not None:
        current_price = re.sub(r"<\/strong>.*\n",'',info[array_loc]) #parsing for current price
        current_price = re.sub(r".*strong>",'',current_price) #parsing for current priceV2
        global price_null
        price_null = 1
        print (bcolors.OKGREEN+"Latest price: " +current_price+bcolors.ENDC)
        #program_reset = 1
    elif array_loc is None:
        #look for another website to find current price
        #for now just display the following message
        #price_null = 0
        print(bcolors.FAIL+"No Price available from marketbeat.com"+bcolors.ENDC)
    filehandle.close()
    #return price_null


#this function is to fetch stock ratings from tipranks website (fetches their API)
def tipranksdata(ticker):# buy_rate, sell_rate, hold_rate):
    tipranks = requests.get('https://www.tipranks.com/api/compare/similar/'+ticker)
    tipranks_data = tipranks.json()
    res = list(tipranks_data.keys())[0]
    dt= tipranks_data['similarStocks']
    global tipranks_consensus
    global buy_rate
    global sell_rate
    global hold_rate
    tipranks_consensus = str(dt)
    #Remove these parsers to get the consensus rating from "Best WS Analysts"
    tipranks_consensus = re.sub(r"nextDividendDate.*",'',tipranks_consensus)
    tipranks_consensus = re.sub(r"\'\, \'raw.*",'',tipranks_consensus)
    tipranks_consensus = re.sub(r"\{.*\'",'',tipranks_consensus)
    if tipranks_consensus == "buy":
        #global buy_rate
        buy_rate = buy_rate + 1
        #print("current buy rate tipranks")
        #print(buy_rate)
    elif tipranks_consensus == "sell":
        sell_rate = sell_rate + 1
    elif tipranks_consensus == "neutral":
        hold_rate = hold_rate + 1
    #print("The consensus is " + tipranks_consensus + " with the following rate: " + str(buy_rate) + str(hold_rate) + str(sell_rate))

def getrating(rating_checker, current_rating, ipo, rating): #buy_rate, sell_rate, hold_rate, rating):
    #to find current rating from marketbeat
    global buy_rate
    global sell_rate
    global hold_rate
    with open(temp.name, 'r') as filehandle:
        info = filehandle.readlines()
        #rating_checker = int()
        for i in info:
            if re.match(r".*buy ratings*",i):
                array_loc = (info.index(i))
                current_rating=re.sub(r".* received a consensus ",'',info[array_loc])
                current_rating = re.sub(r"\..*\n",'',current_rating)
                #print(current_rating)
                rating_checker = 0
                #print(current_rating)
                #print (ipo+" has a "+current_rating) #rating from marketbeat
                break
            else:
                rating_checker = 1
        #algorithm to assign value to rating, if marketbeat is "buy" add 1 to rating, if "hold" add none, if "sell" -1
        if rating_checker > 0:
            print(bcolors.FAIL+"No rating available for this stock on marketbeat.com, fetching rating from the remaining sources"+bcolors.ENDC)
            print(bcolors.WARNING+'++++++++++++++++++++++++++++++++++++++++++++++++'+bcolors.ENDC)
            #print(bcolors.FAIL+"Perhaps you entered the wrong stock exchange/stock symbol"+bcolors.ENDC)

        elif rating_checker == 0:
            if current_rating == "rating of Buy":
                rating = 3
                global buy_rate
                buy_rate = buy_rate + 1
            elif current_rating == "rating of Hold":
                rating = 2
                global hold_rate
                hold_rate = hold_rate + 1
            elif current_rating == "rating of Sell":
                rating = 1
                global sell_rate
                sell_rate = sell_rate + 1
            else:
                rating = str('NULL')
        #print("current buy rate marketbeat")
        #print(buy_rate)

def getratingresult(buy_rate, sell_rate, hold_rate, rating, ipo):
    #this is to check overall rating value after other websites are taken account from
    #in the future check if overall buy_rate > sell_rate & hold_rate then = buy, etc. Majority wins
    #print("buy rate result")
    #print(buy_rate)
    #print(buy_rate)
    #print(sell_rate)
    #print(hold_rate)
    if buy_rate >= hold_rate and buy_rate > sell_rate:
        print(bcolors.OKGREEN+"Current rating for "+ipo+" is buy"+bcolors.ENDC)
    elif hold_rate > sell_rate and hold_rate > buy_rate:
        print(bcolors.WARNING+"Current rating for "+ipo+" is hold"+bcolors.ENDC)
    elif buy_rate == sell_rate and hold_rate < buy_rate:
        print(bcolors.WARNING+"Current rating for "+ipo+" is hold"+bcolors.ENDC)
    elif sell_rate >= hold_rate and sell_rate > buy_rate:
        print(bcolors.FAIL+"Current rating for "+ipo+" is sell"+bcolors.ENDC)
    elif sell_rate == 0 and buy_rate == 0 and hold_rate == 0:
        print(bcolors.FAIL+"No rating available for this organization/or the developer just can't figure out how to fetch rating data from the other source"+bcolors.ENDC)
    elif rating == 'NULL':
        buy_rate = buy_rate + 0
        sell_rate = sell_rate + 0
        hold_rate = hold_rate + 0
        print("No current rating for "+ipo+ "on marketbeat.com")

def getlossgain(current_lg, price_null):
    with open(temp.name, 'r') as filehandle:
        info = filehandle.readlines()
        if price_null == 1:
            for i in info:
                if re.match(r".*As of [0-9]{2}\/[0-9]{1,}\/[0-9]{4}.*",i):
                    array_loc = (info.index(i))
                    #print(info[array_loc])
                    break
            current_lg = re.sub(r".*\&nbsp;",'',info[array_loc]) #parsing for current price
            current_lg = re.sub(r"\<.*\n",'',current_lg) #parsing for current priceV2
            print (bcolors.OKGREEN+"Current loss/gain " +current_lg+bcolors.ENDC)
            filehandle.close()
        elif price_null == 0:
            #print(price_null)
            filehandle.close()

def getinterest():
    #global interest
    global array_loc
    #counter = 0
    with open(temp.name, 'r') as filehandle:
        info = filehandle.readlines()
        for i in info:
            title_search = re.search('Amount of Analyst Coverage.*[0-9]{1,} days', i, re.IGNORECASE)
            if title_search:
                array_loc = (info.index(i))
                #print (info[array_loc])
                interest = re.sub(r".*\>Amount of Analyst Coverage</a></h4><p>",'',info[array_loc]) #researched amount
                interest = re.sub(r"days.*\n",'days.',interest) #parsing for current researched amount
                print (bcolors.OKBLUE+interest+bcolors.ENDC)
                counter = 0
                break
            elif i is not title_search:
                counter = 1
    if counter == 1:
        print(bcolors.WARNING+"Not enough data to show how many researches have been done for this organization --> dev needs a new source"+bcolors.ENDC)
    #interest = re.sub(r".*\>Amount of Analyst Coverage</a></h4><p>",'',info[array_loc]) #researched amount
    #interest = re.sub(r"days.*\n",'days.',interest) #parsing for current researched amount
    #print (bcolors.OKBLUE+interest+bcolors.ENDC)
    filehandle.close()

submitdata(se,symbol)
getname(symbol) #calling function to get stock name
getprice() #get latest price function
getlossgain(current_lg, price_null)
getrating(rating_checker, current_rating, symbol, rating)#buy_rate, sell_rate, hold_rate, rating) #get the most current rating
tipranksdata(symbol)#, buy_rate, sell_rate, hold_rate)
getratingresult(buy_rate, sell_rate, hold_rate, rating, symbol)
#print(buy_rate)

print(bcolors.WARNING+'++++++++++++++++++++++++++++++++++++++++++++++++'+bcolors.ENDC)
print('################################################')
print(bcolors.WARNING+'++++++++++++++++++++++++++++++++++++++++++++++++'+bcolors.ENDC)
getinterest()
print('################################################')
print(bcolors.WARNING+'++++++++++++++++++++++++++++++++++++++++++++++++'+bcolors.ENDC)
#This section is to check if user entered the wrong stock symbol/exchange and asks to re-enter
while program_reset == 1:
    if program_reset == 1:
        se = input("Which stock exchange (type exit to exit the program): ")
        if se == "exit":
            program_reset = 0
            break
        else:
            symbol = str(input("Enter stock symbol e.g WMT, AAPL, etc. or MARKET:SYMBOL for a more accurate result: "))
            submitdata(se,symbol)
            getname(symbol) #calling function to get stock name
            getprice() #get latest price function
            getlossgain(current_lg, price_null)
            getrating(rating_checker, current_rating, symbol, rating)#buy_rate, sell_rate, hold_rate, rating) #get the most current rating
            tipranksdata(symbol)#, buy_rate, sell_rate, hold_rate)
            getratingresult(buy_rate, hold_rate, sell_rate, rating, symbol)
            print(bcolors.WARNING+'++++++++++++++++++++++++++++++++++++++++++++++++'+bcolors.ENDC)
            print('################################################')
            print(bcolors.WARNING+'++++++++++++++++++++++++++++++++++++++++++++++++'+bcolors.ENDC)
            getinterest()
            print('################################################')
            print(bcolors.WARNING+'++++++++++++++++++++++++++++++++++++++++++++++++'+bcolors.ENDC)
        #print('Perhaps you misstyped the stock exchange/stock symbol? Try again')
        #print('++++++++++++++++++++++++++++++++++++++++++++++++')
    #else:
    #    break
