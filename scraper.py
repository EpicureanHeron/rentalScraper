import requests, bs4, os

cwd = os.getcwd()


#query url
f = open(cwd + "/url.txt", "r+") 
url = f.read()


# request the URL
res = requests.get(url)

# load URL into BS
soup = bs4.BeautifulSoup(res.text, 'html.parser')

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

