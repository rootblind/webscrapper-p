
# webscrapper-p
This is a webscrapper made in python through BeautifulSoup4 with the intent to display the difference in time between parallel execution and secvential execution of webscrapping.

The algorithm scraps [books.toscrape.com](https://books.toscrape.com/) and stores the title, price and stock availability of the books, together with a link to their page in an excel file format.

An excel [example](https://github.com/rootblind/webscrapper-p/blob/main/books.xlsx) can be found in this repository.
## Requirements:

```bash
  It was made in python 3.12
  Modules to be imported:
-   import requests
-   from bs4 import BeautifulSoup
-   import pandas as pd
-   import multiprocessing as mp
-   import time
-   import json
```
In case of any module that you're missing, use:
```bash
    pip install <module_name>
    as for example:  pip install beautifulsoup4
```
Make sure to download the `config.json` file in the same directory as `webscrapper-p.py`, or create a json file with the contents:
```json
{
    "site": "https://books.toscrape.com/catalogue/page-{}.html"
}
```
## Execution
Open a Terminal inside the directory where `webscrapper-p.py` is located and type:
```bash
python webscrapper-p.py
```
In case of failure to execute, please make sure python3 is installed correctly and the environment system variables are set correctly.

To check if python is installed correctly, use:
```bash
python --version
or
python
or
py
```
Inside your system's terminal.
## Demo

Click the image for a Demo video
[![Watch the video](https://play-lh.googleusercontent.com/Gcbg63BqBVa-0Ki--TjC-o26iaptfP0YgccBCei6jiyS8aRjWtKxNm-5ZwYGi87qXmg=w240-h480-rw)](https://youtu.be/7bg15JeTEkQ)
## Documentation
### Project details:
- Language used: Python3
- Module used to scrape: BeautifulSoup4
- Module used to execute the algorithm in parallel: multiprocessing
- Algorithm: very simple, so special methods were used
- Website scrapped: static website.

The basic idea of how this code works is that an url is given through `config.json`, which is a file inside the same directory as the source. The file is opened for read and its content is converted into a json object in the following lines:
```py
    configFile = open("config.json", "r")
    config = json.loads(configFile.read())
```
inside the main function of the program (hence \__main\_\_).


The variable _config_ is given as parameter to the functions.

Something important is that the object looks like this:
```bash
{
    "site": "https://books.toscrape.com/catalogue/page-{}.html"
}
```
and the " {} " inside the url is used as placeholder for formatting in order for the code to be able to scrape through each page without having to simulate clicking "next page".

And in that way, the code scraps the website and puts the data inside an excel file.
#
 To achieve this, the code uses two def functions:

The first function is __scrape\_one\_page__ which is given two variables: page and config. page represents a specific web page of the website and config represents the json object.

The second one is __scrape\_books__ and its parameters are:
- start: the first page to scrape
- finish: the last page to scrape
- config: the json object

The only difference between scrape\_one\_page and scrape\_books is that the first one does it for one page, while the other does it for a range of pages, so there is no need to explain the same thing twice, but since doing so for a range of pages might be a bit more difficult than doing so for a single one, the former will be analized.

```py
for current_page in range(start, finish):
```
Starting from "start" index and finishing with "finish - 1", since range(1,x) generates a sequence of numbers from 1 to x-1.

```py
print("Current page: ", current_page)
```
The current page that is being scrapped is printed into the terminal.

```py
        url = config["site"].format(current_page)
        page = requests.get(url).text
        doc = BeautifulSoup(page, "html.parser")
```
- config["site"] accesses the json object, the "site" key that has the value the url inside the file.

- config["site"].format(current_page) replaces {} inside the string with the current page that is being scrapped

- requests.get(url) sends a HTTP request to the "url" and returns the response, in our case that being the content of the web page which is converted to a parsable string through ".text" and this value is kept in "page" variable
- doc uses BeautifulSoup method to parse the content of "page" using "html.parser" as the format method. Exactly what we need in order to scrape for content inside the html code of the page.

```py
if doc.title.text != "404 Not Found":
            all_books = doc.find_all("li", class_="col-xs-6 col-sm-4 col-md-3 col-lg-3")
```

doc.title.text means the title object inside the html code, converted as string.
And if its value is "404 Not Found", through tests, this is the title value when a page is not avalible, then the page is skipped, otherwise, filtering and storing the seeked content starts.

What doc.find_all() does is returning an array that stores as elements, everything that matches what's given as parameter.

In our case "li" is a list in html <li> and we know that the content we're looking for is inside a list li.
What we also know is that the classes of what we want to scrap are `col-xs-6 col-sm-4 col-md-3 col-lg-3`.

```py
for book in all_books:
                item = {}
                item['Title'] = book.find("img").attrs["alt"]
                item['Link'] = "https://books.toscrape.com/catalogue/" + book.find("a").attrs["href"]
                item["Price"] = book.find("p", class_="price_color").text[2:]
                item["Stock"] = book.find("p", class_="instock availability").text.strip()
                
                data.append(item)
```
The code iterates through the all_books array in order to access the attributes of each book. We also need an object for each book that has as attributes the information that we want to scrap and store inside an array "data".

The find() method is used to return the first element that is found. attrs() takes as parameter a specific attribute to be returned of what is found.

Therefore, for books.toscrape.com, the title of each book is inside the image's alt text; The link is composed of the catalogue url and the contents of <a> attribute href; The price is formatted to exclude the currency symbol and keep only the numbers; As for the stock availability, the string has a lot of spaces, so strip() is used to remove these spaces.

At the end, each item is appended to the data array.

### The scrapping part of the code is done, the following lines will be about how the code executes it.

The first execution is launching 3 parallel processes, each is given a segment of the 50 pages; from 1 to 16, from 17 to 33 and from 34 to 50.
```py
    p1 = mp.Process(target=scrape_books, args=(1, 17,config,))
    p2 = mp.Process(target=scrape_books, args=(17, 34,config,))
    p3 = mp.Process(target=scrape_books, args=(34, 51,config,))
```
mp.Process takes as arguments a target, which is a defined function, therefore parallelization can not be done without the use of methods; And a touble args where the arguments of the method are given, if any.

A process must be started through the method call of ".start()" and be waited by the main process to finish its execution through the ".join()" method.

The second execution is launching a process for each page.

To do so, I made an array of processes, each calling mp.Process recieving as target "scrape_books" and as for args: their corresponding page and the config object.
```py
    for process in processes:
        process.start()
    
    for process in processes:
        process.join()
```

The third execution is the iterative, one process one, done so by simply calling scrape_books from 1 to 50.
```py
    scrape_books(1, 51,config)
```
And the data is stored into an excel file using the following lines that formats the array of item objects and exports it to an excel file.
```py
df = pd.DataFrame(data)
df.to_excel("books.xlsx")
```

## Execution time
After each execution is finished, the code prints the time passed.

Using the time module and the time() method, we can wrap any portion of the code between two calls of `time.time()` and the difference between the latter and the former is the time it took to execute.

Example in code:
```py
    start = time.time()
    for process in processes:
        process.start()
    
    for process in processes:
        process.join()
    end = time.time()
    print("Execution time 50 parallel processes: ", end-start)
```

Thanks to this the code has the following average results:
Scraping 50 pages from books.toscrape.com.
- Three parallel processes: 23.77 seconds
- Fifty parallel processes: 17.46 seconds
- Secvential execution (one process): 53.69 seconds

Let the secvential execution be the baseline, then we can conclude that, in our code, 3 parallel processes are ~55.72% faster than one and 50 parallel processes are ~73.06% faster. But the speed increase from 3 parallel processes to 50 is only about 26.54%, resulting that the more processes we add, while it gets faster, each process increases the speed by smaller and smaller amounts, therefore consuming more memory and making it inefficient.

As reference, the processor used in running those tests:
![processor](https://i.imgur.com/WFMJcse.png)
## Author

- Me: [@rootblind](https://github.com/rootblind/)

Done as a project for Parallel and Distributed Algorithms.
