from tkinter import *
from tkinter import ttk
import nltk
from nltk.corpus import stopwords
from rake_nltk import Rake

import requests
import wikipediaapi

root = Tk()
frm = ttk.Frame(root, padding=10)
frm.grid()
nltk.download('stopwords')



def get_random_wikipedia_article():
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "list": "random",
        "rnlimit": 1,
        "rnnamespace": 0
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    
    if 'query' in data and 'random' in data['query']:
        random_article = data['query']['random'][0]
        title = random_article['title']
        page_id = random_article['id']
        article_url = f"https://en.wikipedia.org/wiki/{title.replace(' ', '_')}"
        
        return title, article_url
    else:
        return None, None


def find_random_wiki():
    title, url = get_random_wikipedia_article()
    if title and url:
        #print(f"Random Article: {title}")
        print(f"URL: {url}")
    else:
        print("Failed to retrieve a random article.")
    
    
    # Create a Wikipedia API object
    wiki_wiki = wikipediaapi.Wikipedia(
        user_agent = 'Practice Agent ', language = 'en', 
        extract_format=wikipediaapi.ExtractFormat.WIKI)

    # Get a random Wikipedia page
    random_page = wiki_wiki.page(title)
    root.destroy()
    level = 0 
   # for s in random_page.sections:
                #print(s.title)
    
    keywords = get_keywords(random_page.summary + random_page.title)
    create_search_term(keywords= keywords)
    
    print_to_file(random_page.title, random_page.summary)


def print_to_file(title,summary):
    file = open(file="Wiki_page.html", mode='r+', encoding= "utf-8")
    file.write(f" {summary}")
    file.close()
    
def get_keywords(title):
    r = Rake(stopwords = stopwords.words('english'))
    r.extract_keywords_from_text(title)
    keywords_with_scores = r.get_ranked_phrases()
    return keywords_with_scores

def create_search_term(keywords):
    for i in range(0,5):
        print(keywords[i])

ttk.Label(frm, text="Hello World!").grid(column=0, row=0)
ttk.Button(frm, text="Quit", command=root.destroy).grid(column=1, row=1)
ttk.Button(frm, text= "Randomize", command = find_random_wiki).grid(column=1, row=0)

root.mainloop()