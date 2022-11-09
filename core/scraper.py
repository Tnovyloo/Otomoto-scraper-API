import requests
import bs4 as bs
from multiprocessing.dummy import Pool as ThreadPool


def check_type_of_url(url):
    # print(url)
    temp_list = url.split('/')

    if indexExists(temp_list, 5) is False:
        # return print("True '?' - no url[5]") #TODO - Add this descriptions in Program logs
        return True
    else:
        if indexExists(temp_list, 6):
            # return print("False '&' - search in url[6]")
            return False
    if indexExists(temp_list, 5):
        if temp_list[5].__contains__("search"):
            # return print("False '&' - url[5] contains search")
            return False
        else:
            if indexExists(temp_list, 6):
                if temp_list[6].__contains__("search"):
                    # return print("False '&' - url[6] contains search")
                    return False
                else:
                    # return print("True '?' - url[6] no contains search")
                    return True
            # return print("True '?' - url no contains 'search'")
            return True

def indexExists(list, index):
    try:
        list[index]
        return True
    except IndexError:
        return False

class DownloadPage:
    def __init__(self, url):
        self.url = url # URL from user
        self.response = requests.get(self.url).text # Response
        self.soup = bs.BeautifulSoup(self.response, 'html.parser') # Creating BS object
        self.price_cars_list = [] # List of prices of cars
        self.link_cars_list = [] # List of URLs of cars
        self.page_list = [] # List of pages from URL

    def find_data(self, url):
        """Finding price of cars in page"""
        response = requests.get(url).text
        inner_soup = bs.BeautifulSoup(response, 'html5lib')
        cars_price = inner_soup.findAll('span',
                                        class_='ooa-epvm6 e1b25f6f8')  # Sometimes the class of 'span' on te web-page is changed
        for price in cars_price:
            self.price_cars_list.append(str(price.text).strip('PLN '))  # Appending price to list

        cars_links = inner_soup.findAll('h2',
                                        class_='e1b25f6f6 e1b25f6f19 ooa-10p8u4x er34gjf0')  # Sometimes the class of 'h2' on te web-page is changed
        for link in cars_links:
            link = link.find('a', href=True)
            self.link_cars_list.append(link['href'])  # Appending URL to list

    def find_page(self, site):
        """Finding amount of pages"""
        # webpages = self.soup.findAll('span', class_="page")
        response = requests.get(site).text
        soup = bs.BeautifulSoup(response, 'html5lib')

        webpages = soup.findAll('a',
                                class_='ooa-g4wbjr ekxs86z0')  # Sometimes the class of 'a' on te web-page is changed
        if len(webpages) == 0:  # Check if there is problem with finding amount of pages
            self.page_list = ['0']
        else:
            self.page_list = [page.text for page in webpages]  # Appending numbers of pages

        print(f'Amount of pages: {self.page_list[-1]}')
        return self.page_list

    def start(self):
        count_pages = int(self.find_page(self.url)[-1])  # Last index from page_list is amount of pages

        if check_type_of_url(self.url) is True:
            func_url = (self.url[:] + f"?page=0")  # Append '?page=0' to URL which is used on next steps
        else:
            func_url = (self.url[:] + f"&page=0")  # Append '$page=0' to URL which is used on next steps

        url_pages = [func_url[:-1] + f'{page}' for page in range(count_pages + 1)]

        pool = ThreadPool(4)
        results = pool.map(lambda x: self.find_data(x), url_pages)

        pool.close()
        pool.join()

        cars = zip(self.price_cars_list, self.link_cars_list)

        return cars

class ScrapMoreData:
    def __init__(self, car_dict:dict):
        self.car_info = car_dict

    def find_more_data(self, url):
        html = requests.get(url).text
        soup = BeautifulSoup(html, 'html.parser')

        li_data = soup.findAll('li', class_='offer-params__item')
        # print(li_data)

        labels = []
        for label in li_data:
            label = label.find('span', class_='offer-params__label')
            labels.append(label.text)

        data = []
        for info in li_data:
            info = info.find('div', class_='offer-params__value')
            data.append(str(info.text).strip())

        car_data = zip(labels, data)
        return car_data

    def get_more_data(self, data, url, price):
        result = {'URL': f'{url}',
                'cena': f'{price}',
                'Marka pojazdu' : '',
                'Model pojazdu' : '',
                'Rok produkcji' : '',
                'Wersja' : '',
                'Moc' : '',
                'Liczba drzwi' : '',
                'Rodzaj paliwa' : '',
                'Pojemność skokowa' : '',
                'Skrzynia biegów' : '',
                'Typ nadwozia' : '',
                'Kolor' : ''}

        for element, answer in list(data):
            if element in result:
                result[element] = answer

        return result

    def start(self, url, price):
        # for price, url in self.car_info.items():
        #     result_of_finding = self.find_more_data(url)
        #     result = self.get_more_data(result_of_finding, url, price)
        #     print(result)
        result_of_finding = self.find_more_data(url)
        result = self.get_more_data(result_of_finding, url, price)
        return result