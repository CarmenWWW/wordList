#https://www.vocabulary.com/lists/n6qhcqws/words-to-help-you-win-at-wordle/explore

import sys
import requests # get URL
from  bs4 import BeautifulSoup # analyze website
import re # regular expression
import xlwt # excel
import sqlite3 # sqlite
import random



wordList = []
defList = []


def main():

    urlList = [
        "https://www.vocabulary.com/lists/8266895",
        "https://www.vocabulary.com/lists/8266838",
        "https://www.vocabulary.com/lists/8266845",
        "https://www.vocabulary.com/lists/8266851",
        "https://www.vocabulary.com/lists/8266856",
        "https://www.vocabulary.com/lists/8266860",
        "https://www.vocabulary.com/lists/8266817"
    ]

    for url in urlList:
        # get info list
        getData(url)
    
    #print(len(wordList) == len(defList))
    resultList = getTogether()
    #write(resultList, output)
    saveData(resultList)
    
    # separate info into words
    # print (wordDict(dataList))

findWord = re.compile(r'<a class="word dynamictext" href="/dictionary/(.*?)"') # word rules                 
findDef = re.compile(r'<div class="definition">(.*?)</div>') # word definition


def getData(url):
    # 1 get source code file

    html = askURL(url)
    # 2 analyze source code file
    soup = BeautifulSoup(html, "html.parser")
    for item in soup.find_all('div', class_ = "definition"): 
        # find different strings and form list
        item = str(item)
        # regular expression
        definition = re.findall(findDef, item)
        defList.append(definition[0])

    for item in soup.find_all('a', class_ = "word dynamictext"): 
        # find different strings and form list
        item = str(item)
        word = ""
        # print(item)
        word = re.findall(findWord, item)
        wordList.append(word[0])
    return

def askURL(url):
    #im a human, not a spider!
    head = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
        }
    html = ""
    try:
        response = requests.get(url, headers = head)
        response.encoding = "utf-8"
        html = response.content.decode()
        print (f'note {url} scraped successfully!')
        return html
    except:
        print (f'something went wrong in {url}')
        pass

def getTogether():
    resultList = []
    for i in range(len(wordList)):
        resultList.append((wordList[i], defList[i]))
    return resultList

def saveData(resultList):
    workbook = xlwt.Workbook(encoding = "utf-8")
    worksheet = workbook.add_sheet("sheet1")
    row = 0
    col = 0
    count = 0
    for (word, definition) in resultList:
        count += 1
        #addSQL(movie, rating, count)
        worksheet.write(row, col, word)
        worksheet.write(row, col+1, definition)
        row += 1
        if row == 20:
            row = 0
            col += 2
    workbook.save("word_definition_wordle.xls")


def addSQL(word, definition, id):
    conn = sqlite3.connect("movie.db")
    print ("Opened database successfully")
    c = conn.cursor()
    sql = '''
    create table resultList
        (id int primary key not null,
        name text not null,
        rating float not null);
    '''

    sql = '''
    insert into resultList(word, definition, id)
    values(word, definition, id)
    ''' 

    c.execute(sql)
    conn.commit()
    conn.close()


main()