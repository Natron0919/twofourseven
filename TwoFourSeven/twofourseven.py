import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv
from lxml import html

# Functions that will be used in recruiting Classes
def save_html(html, path):
    with open(path, 'wb') as f:
        f.write(html)
def open_html(path):
    with open(path, 'rb') as f:
        return f.read()

class Recruit:

    def __init__(self):
        self.session = requests.Session()

    def getClass(self, year, team):
        self.year = year
        self.team = str(team)
        self.team = self.team.replace(' ', '-')
        self.team = self.team.lower()

        res = self.session.get('https://247sports.com/college/' + self.team + '/Season/' + str(self.year) + '-Football/Commits/', headers = {'User-Agent': 'Mozilla/5.0'})
        res.raise_for_status()
        site = html.fromstring(res.content)

        players = site.xpath("//div[@class='recruit']/a/text()")
        pos = site.xpath("//li[@class='ri-page__list-item']/div/div[@class='position']/text()")
        metrics = site.xpath("//li[@class='ri-page__list-item']/div/div[@class='metrics']/text()")
        ht = [x.split('/')[0].strip() for x in metrics]
        wt = [x.split('/')[1].strip() for x in metrics]
        hometown = site.xpath("//div[@class='recruit']/span/text()")
        hometown = [x.strip() for x in hometown if x.strip()]
        score = site.xpath("//div[@class='rating']/div/span[@class='score']/text()")
        nat_rank = site.xpath("//a[@class='natrank']/text()")
        pos_rank = site.xpath("//a[@class='posrank']/text()")
        st_rank = site.xpath("//a[@class='sttrank']/text()")

        di = {
        'Player' : players, 
        'POS' : pos,
        'HT' : ht,
        'WT' : wt,
        'Hometown': hometown,
        'Rating' : score,
        'National_Rank' : nat_rank,
        'Position_Rank' : pos_rank,
        'State_Rank' : st_rank
        }

        df = pd.DataFrame(di)

        return df

class TransferPortal:

    def __init__(self):
        self.session = requests.Session()

    def getData(self, year):
        
        self.year = year
        # Get html from site for appropriate year. 
        res = requests.get('https://247sports.com/Season/' + str(year) + '-Football/TransferPortal/', headers={'User-Agent': 'Mozilla/5.0'})
        res.raise_for_status()
        site = html.fromstring(res.content)

        # Return lists of player names, position, and rating from HS
        players = site.xpath("//div[@class='player']/a/text()")
        positions = site.xpath("//div[@class='position']/text()")
        scores = site.xpath("//span[child::span[text()='(HS)']]/text()")

        # Return initial team and new team for each player
        player_list = site.xpath("//li[@class='portal-list_itm']")
        team1 = [] # Empty list for original team
        team2 = [] # Empty list for new team
        for x in player_list: # For-loop to get all players original team
            try:
                team2.append(x.xpath("div[contains(@class, 'transfer-institution')]/a[2]/img/@alt"))
            except:
                team2.append('NULL')
        for x in player_list: # For-loop to get all players new team
            try:
                team1.append(x.xpath("div[contains(@class, 'transfer-institution')]/a[1]/img/@alt"))
            except:
                team1.append('NULL')

        team1 = [''.join(x) for x in team1] # Turn all entries into strings instead of one length lists
        team2 = [''.join(x) for x in team2] # Turn all entries into strings instead of one length lists

        # Create dictionary from all lists
        di = {'Player' : players, 'POS' : positions, 'Rating' : scores, 'OriginalTeam' : team1, 'NewTeam' : team2}

        # Turn dictionary into DataFrame
        df = pd.DataFrame(di)
        df['Player'] = df['Player'].astype(str)
        df['POS'] = df['POS'].astype(str)
        df['Rating'] = df['Rating'].str.strip()
        df = df.replace('N/A', 'NULL')
        df.insert(0, 'Year', year)

        return df