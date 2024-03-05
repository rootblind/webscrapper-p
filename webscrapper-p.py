import requests
from bs4 import BeautifulSoup
import pandas as pd
import multiprocessing as mp
import time
import math

# scraping books to scrape
# the iterative program

data = []

def scrape_one_page(page):
    print("Current page: ", page)
    url = f"https://books.toscrape.com/catalogue/page-{page}.html"
    page = requests.get(url).text
    doc = BeautifulSoup(page, "html.parser")

    if doc.title.text != "404 Not Found":
        all_books = doc.find_all("li", class_="col-xs-6 col-sm-4 col-md-3 col-lg-3")

        for book in all_books:
            item = {}
            item['Title'] = book.find("img").attrs["alt"]
            item['Link'] = "https://books.toscrape.com/catalogue/" + book.find("a").attrs["href"]
            item["Price"] = book.find("p", class_="price_color").text[2:]
            item["Stock"] = book.find("p", class_="instock availability").text.strip()
                
            data.append(item)

def scrape_books(start, finish):
    for current_page in range(start, finish):
        print("Current page: ", current_page)
        url = f"https://books.toscrape.com/catalogue/page-{current_page}.html"
        page = requests.get(url).text
        doc = BeautifulSoup(page, "html.parser")

        if doc.title.text != "404 Not Found":
            all_books = doc.find_all("li", class_="col-xs-6 col-sm-4 col-md-3 col-lg-3")

            for book in all_books:
                item = {}
                item['Title'] = book.find("img").attrs["alt"]
                item['Link'] = "https://books.toscrape.com/catalogue/" + book.find("a").attrs["href"]
                item["Price"] = book.find("p", class_="price_color").text[2:]
                item["Stock"] = book.find("p", class_="instock availability").text.strip()
                
                data.append(item)

if __name__ == "__main__":
    
    
    
    # the 3 parallel processes
    
    p1 = mp.Process(target=scrape_books, args=(1, 17,))
    p2 = mp.Process(target=scrape_books, args=(17, 34,))
    p3 = mp.Process(target=scrape_books, args=(34, 51,))
    start = time.time()
    p1.start()
    p2.start()
    p3.start()
    p1.join()
    p2.join()
    p3.join()
    end = time.time()
    print("Execution time 3 parallel processes: ", end-start)

    # a process for each page
    processes = [mp.Process(target=scrape_one_page, args=(i,)) for i in range(1, 51)]
    start = time.time()
    for process in processes:
        process.start()
    
    for process in processes:
        process.join()
    end = time.time()
    print("Execution time 50 parallel processes: ", end-start)
    # iterative program
    start = time.time()
    scrape_books(1, 51)
    end = time.time()
    print("Execution time iterative: ", end-start)

# storing the data scraped into an excel
df = pd.DataFrame(data)
df.to_excel("books.xlsx")