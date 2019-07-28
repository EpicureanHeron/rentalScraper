import requests, bs4, os, openpyxl, datetime

def zillowAPI(api):

    # sample api call:
    #   http://www.zillow.com/webservice/GetSearchResults.htm?zws-id=<ZWSID>&address=2114+Bigelow+Ave&citystatezip=Seattle%2C+WA
    # documents: https://www.zillow.com/howto/api/GetSearchResults.htm
    url = 'http://www.zillow.com/webservice/GetSearchResults.htm?zws-id=' + api
    # zip paramenter
    url += '&citystatezip=55372'

    url+= '&rentzestimate=True'

    res = requests.get(url)

    print(res.text)
    # it doesn't look like the API will allow a search. aYou must know the location itself

    # probably will scrape instead: https://www.zillow.com/savage-mn/rentals/2-_beds/?searchQueryState={%22pagination%22:{},%22mapBounds%22:{%22west%22:-93.4254929523214,%22east%22:-93.3034760476786,%22south%22:44.74174617796238,%22north%22:44.76695555723581},%22usersSearchTerm%22:%22savage%20%22,%22regionSelection%22:[{%22regionId%22:50554,%22regionType%22:6}],%22isMapVisible%22:true,%22mapZoom%22:13,%22filterState%22:{%22price%22:{%22min%22:430854,%22max%22:592424},%22monthlyPayment%22:{%22min%22:1600,%22max%22:2200},%22beds%22:{%22min%22:2},%22sortSelection%22:{%22value%22:%22days%22},%22isForSaleByAgent%22:{%22value%22:false},%22isForSaleByOwner%22:{%22value%22:false},%22isNewConstruction%22:{%22value%22:false},%22isForSaleForeclosure%22:{%22value%22:false},%22isComingSoon%22:{%22value%22:false},%22isAuction%22:{%22value%22:false},%22isPreMarketForeclosure%22:{%22value%22:false},%22isPreMarketPreForeclosure%22:{%22value%22:false},%22isMakeMeMove%22:{%22value%22:false},%22isForRent%22:{%22value%22:true}},%22isListVisible%22:true}

    

def scrapeCraigslist(queryURL):

    # request the URL
    res = requests.get(queryURL)

    # load URL into BS
    soup = bs4.BeautifulSoup(res.text, 'html.parser')

    scrappingResults = []

    # select all results
    liArray = soup.find_all("li", class_="result-row".split())

    # iterate through the results
    for li in liArray:
        # get the ID of the post
        dataid = li['data-pid']
        # check to see if it is a repost and grab repost id
        if li.has_attr('data-repost-of'):
            repost = li['data-repost-of']
        else:
            repost = 'None'

        # parse the <a> tag
        a = li.find('a', class_= 'hdrlnk')
        # grabs the URL from HREF of the a tag
        postingLink = a['href']
        try:
            price = li.find('span', class_='result-price').text
        except:
            price = 'None Found'

        try:
            hood = li.find('span', class_='result-hood').text
        except:
            hood = 'None Found'
        # requests the posting page
        postingRes = requests.get(postingLink)
        # creates soup for posting page
        postingSoup = bs4.BeautifulSoup(postingRes.text, 'html.parser')
        # grabs attributes
       # attrGroup = postingSoup.find_all('p', class_='attrgroup'.split())
        spanGroup = postingSoup.find_all('span', class_='shared-line-bubble'.split())

        # creates an empty list to store attributes
       # attrList = []
        spanList = []
        # puts attributes into list
        for span in spanGroup:
            spanList.append(span.text)
            # grabs posting description
        description = postingSoup.find(id='postingbody')

            # for all the below we need to take out the '\n' I think...and maybe split it on that? 
            # attrList[0] is both the size, rooms, and availability, may be split on the \n
            # attrList[1] is other things
            # attrList[2:] is a bunch of other things, need to lloki at all that data 
        try:
            scrappingResults.append([dataid, repost, postingLink, price, hood, spanList[0], spanList[1], description.text])

           # scrappingResults.append([dataid, repost, postingLink, ','.join(spanList[0:2]), ','.join(attrList[2:]), description.text])
        except:
          #   print(postingLink)
             print(spanList)
             break
        resultsExcel(scrappingResults)

def resultsExcel(results):
    excelRow = 1
    excelColumn = 1
    wb = openpyxl.Workbook()
    sheet = wb.active
    for posting in results:
        for data in posting:
            sheet[openpyxl.utils.get_column_letter(excelColumn) + str(excelRow)] = data

            excelColumn += 1
        #iterates to the next row
        excelRow += 1
        #resets the column counter when a new row is written
        excelColumn = 1
    fileName =  ' Results ' + str(datetime.datetime.now().date()) + '.xlsx'
    wb.save(fileName)

cwd = os.getcwd()

#query url
f = open(cwd + "/url.txt", "r+") 
url = f.read()

f2 = open(cwd +'/api.txt', 'r+')
apiKey = f2.read()

#scrapeCraigslist(url)

zillowAPI(apiKey)