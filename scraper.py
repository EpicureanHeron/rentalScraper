import requests, bs4, os, openpyxl, datetime
def scrapeZillow(queryURL):

    res = requests.get(queryURL)

    soup = bs4.BeautifulSoup(res.text, 'html.parser')

    print(soup)
    

   # results = soup.find_all('a', class_='list-card-link list-card-img'.split())

    #for article in results:
     #   print(article)

def scrapeCraigslist(queryURL):

    # request the URL
    res = requests.get(queryURL)

    # load URL into BS
    soup = bs4.BeautifulSoup(res.text, 'html.parser')

    print('Gathering listings from %s' % (queryURL))

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

    print("Gathered results")
    resultsExcel(scrappingResults)

def resultsExcel(results):
    print('Writing results to excel sheet')

    
    excelRow = 2
    excelColumn = 1
    wb = openpyxl.Workbook()
    sheet = wb.active
    sheet['A1'] = 'Post ID'
    sheet['B1'] = 'Repost ID'
    sheet['C1'] = 'Direct Link'
    sheet['D1'] = 'Price'
    sheet['E1'] = 'Location'
    sheet['F1'] = 'Bedroom/Bath'
    sheet['G1'] = 'SQ FT'
    sheet['H1'] = 'Description'

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
    print('Done!')

cwd = os.getcwd()

#query url
f = open(cwd + "/craigslisturl.txt", "r+") 
clurl = f.read()

f2 = open(cwd +'/zillowurl.txt', 'r+')
zurl = f2.read()

scrapeCraigslist(clurl)

#scrapeZillow(zurl)

