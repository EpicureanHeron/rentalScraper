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
    # parse the <a> tag
    link = li.find('a', class_= 'hdrlnk')
    # prints the link itself
    print(link['href'])