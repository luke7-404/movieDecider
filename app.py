from bs4 import BeautifulSoup as bSoup
import requests
import datetime as date
import imdb


class Scraper(object):
    def __init__(self, year: int, typeOfContent: str):
      self.year = year
      self.type = typeOfContent
      self.url = "https://www.imdb.com/search/title/?title_type=" + self.type + "&release_date=" + str(self.year) + "," + str(self.year)
      
    def createSoup(self):
        # Provide the request with a User-Agent
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }

        # URL to scrape data from

        # Get the response from the URL using the User-Agent credentials
        response = requests.get(self.url, headers=headers)

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
            
        return dataMatrix
    
    def firstLink(self, URL, name):
        self.url = URL
        soup = self.createSoup()
        a_tags = soup.find_all('a')
        for a in a_tags:
            if a.string == name:
                a_tags = a   
                return str(a['href'])
        pass
        
        
class User(object):
    
    def menuSelecton(self):
        selection = ["year", "content"]
        entertainmentType = ["feature","tv_special","podcast_episode",
                             "tv_series","tv_short","short","video_game",
                             "tv_episode","video","tv_miniseries","tv_movie", "music_video"]
        print("What type of content would you like to see? Please choose from the list below: ")
        for i in range(len(entertainmentType)):            
            print(f'{i+1}. {entertainmentType[i].replace('_', ' ').title()}') 
            
        while not (selection[1].isdigit()):
            selection[1] = input("Choose the type of content by entering its number: ")
            if selection[1].isdigit() and (int(selection[1])-1 < len(entertainmentType)): 
                selection[1] = entertainmentType[int(selection[1])-1]
                break
            else:
                print("Selection not answered correctly try again")
                selection[1] = "b"
        
        while not (selection[0].isdigit()):
            selection[0] = input("Please enter in the year that the content was made in: ")
            if selection[0].isdigit() and (int(selection[0]) <= int(date.datetime.now().year) or int(selection[0]) >= 1900): 
                break
            else:
                print("Selection not answered correctly try again")
                selection[0] = "b"
        
        formattedSelection = selection[1].replace('_', ' ').title()
            
        if not (formattedSelection.endswith('s')):
            formattedSelection += 's'
            
        print(f"Thanks for your inputs! here are the top 50 {formattedSelection} from the year {selection[0]}: \n")
        scraper = Scraper(selection[0], selection[1])
        data = scraper.scrapeIMDb()
        
        lookupIndex = input("If you would like to see the IMDb page for a specific title, enter its number. If you wouldn't, enter anything else: ") + ". "
        
        try:
            int(lookupIndex)
            int(lookupIndex) > 0 and int(lookupIndex) <= 50
        except:
            print("Thank you for using Movie Decider")
            return 0
        nameOfContent = ""
            
        for i in range(len(data)):
            if lookupIndex in data[i][0][::]:
                nameOfContent = data[i][0].strip(lookupIndex)
                break    

        link = scraper.firstLink(f"http://www.imdb.com/find?q={nameOfContent.replace(' ', '%20')}&s=all", nameOfContent)
        print(f'The URL: http://www.imdb.com{link}')
        return 1
        
        

# Main
user = User()
user.menuSelecton()
