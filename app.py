from bs4 import BeautifulSoup as bSoup
import urllib3


url = "http://localhost:8000/"
our_url = urllib3.PoolManager().request('GET', url).data
soup = bSoup(our_url, "lxml")

#print(soup.find('title').text)
#print(soup.find('body').text)

head_tag = soup.head
#print(str(head_tag) + "\n")
print(head_tag.contents)

for child in head_tag.descendants:
    print(child)
    
#title_tag = head_tag.contents[0]
#print(title_tag.string)


