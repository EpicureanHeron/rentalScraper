import requests, bs4, os, openpyxl, datetime


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


# request the URL
res = requests.get(url)

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
    # requests the posting page
    postingRes = requests.get(postingLink)
    # creates soup for posting page
    postingSoup = bs4.BeautifulSoup(postingRes.text, 'html.parser')
    # grabs attributes
    attrGroup = postingSoup.find_all('p', class_='attrgroup'.split())
    # creates an empty list to store attributes
    attrList = []
    # puts attributes into list
    for attr in attrGroup:
       attrList.append(attr.text)
    # grabs posting description
    description = postingSoup.find(id='postingbody')

    # for all the below we need to take out the '\n' I think...and maybe split it on that? 
    # attrList[0] is both the size, rooms, and availability, may be split on the \n
    # attrList[1] is other things
    # attrList[2:] is a bunch of other things, need to lloki at all that data 
    scrappingResults.append([dataid, repost, postingLink, attrList[0], attrList[1], ','.join(attrList[2:]), description.text])

    resultsExcel(scrappingResults)
