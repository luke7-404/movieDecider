from bs4 import BeautifulSoup as bSoup
import requests


class User:
    def __init__(self, year: int, typeOfContent: str):
      self.year = year
      self.type = typeOfContent
      
    def createSoup(self):
        # Provide the request with a User-Agent
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }

        # URL to scrape data from
        url = "https://www.imdb.com/search/title/?title_type=" + self.type + "&release_date=" + str(self.year) + "," + str(self.year)

        # Get the response from the URL using the User-Agent credentials
        response = requests.get(url, headers=headers)

        # return BeautifulSoup's scrapings 
        return bSoup(response.text, "html.parser")

    # Where the data sits
    #/html/body/div[2]/main/div[2]/div[3]/section/section/div/
    #section/section/div[2]/div/section/div[2]/div[2]/ul

    # The iterable at the end of the last path
    #/ul/li[1]

    def findDataLocation(self):
        soup = self.createSoup()
        body_tag = soup.find("body")
        for ul in body_tag.find_all('ul'):
            if str(ul.get('class')[0]) == "ipc-metadata-list":
                return ul
        pass
    
    def collectData(self):
        ul_location = self.findDataLocation()
        dataMatrix = []
        
        for li in ul_location:
            row = []
            row.append(str(li.find('h3').string))
            for spans in range(len(li.find_all("span"))):
                spanItem = li.find_all("span")[spans].text
                if spans > 0 and spans < 5:
                    if "(" in str(spanItem):
                        row.append(str(spanItem[:spanItem.find("(")-1]))
                    else: 
                        row.append(str(spanItem))
            dataMatrix.append(row)         
        return dataMatrix
                    
            
        
        
        
    def scrapeIMDb(self):
        dataMatrix = self.collectData()
        for row in dataMatrix:
            print(" | ".join(row)+"\n")
        
        

            
        
        



# Main
user = User(1980, "feature")
user.scrapeIMDb()
