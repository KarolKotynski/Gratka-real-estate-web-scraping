from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uOpen
from urllib.request import Request as uRequest


class PageSearch:
    """
    Result of this class and function get_page is html content of current page
    as arguments gets url of site and number of page (default is 1)
    e.g.
    url_page = "https://gratka.pl/nieruchomosci/mieszkania/gdansk/sprzedaz?page="
    number_page = 0
    return is <html> content </html>
    """
    full_url = ''
    page = ''
    def __init__(self, url, page=1):
        self.url = url
        self.page = page
        PageSearch.full_url = self.url + str(self.url)


    def __str__(self):
        return f"url: {self.url}\npage: {self.page}"

    def get_page(self):
        try:
            page_url = self.url + str(self.page)
            header = {'User-Agent': 'Mozilla/5.0'}
            request = uRequest(page_url, headers=header)
            client = uOpen(request)
            page = soup(client, 'html.parser')
            client.close()
            PageSearch.page = page
            return page
        except:
            raise AttributeError(f"{self.url}{self.page} not found.")


class ContentSearch(PageSearch):
    """
    Result of this class and get_object_list is to return listed object
    As arguments are name of class where listed object exists
    and name of listed objects
    e.g.
    container = 'content__listing'
    list_search = 'article'
    return is content of articles in current page
    """

    def __init__(self, container, list_search):
        self.container = container
        self.list_search = list_search
    
    def __str__(self):
        return f"container name: {self.container}\nsearching list: {self.list_search}\n{self.full_url}"

    def get_object_list(self):
        # page content taken from PageSearch
        container = self.page.find('div', {'class': self.container})
        object_list = container.findAll(self.list_search)

        return object_list