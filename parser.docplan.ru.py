import requests
from bs4 import BeautifulSoup
from pprint import pprint as pp
import xlsxwriter


class Scraper():
    """ Сбор нормативки с сайта docplan.ru"""

    def __init__(self) -> None:
        pass

    def get_soup(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        return soup

    def get_url_type(self, url):
        soup = self.get_soup(url)
        rows = soup.find_all('tr', class_='m2')
        links = []
        for row in rows:
            cell = row.find(align='left')
            ntd_name = (cell.text)
            ntd_link = 'https://docplan.ru/' + cell.find('a').get('href')
            # print(f'{ntd_name}\t {ntd_link}')
            links.append((ntd_name, ntd_link))
        return links

    def get_ntd_list(self, url):
        soup = self.get_soup(url)
        ntd_rows = soup.find_all('tr', class_='m3')
        links = []
        for row in ntd_rows:
            row = row.find_all('td')
            cells = row[0].find_all('a')
            for cell in cells:
                if cell.text != '':
                    ntd_name = cell.text
                    link = cell.get('href')
                    ntd_link = 'https://docplan.ru/' + link[3:]
                    links.append((ntd_name, ntd_link))
        return links

    def get_ntd_pages(self, url):
        """ Получаем список листов """
        urls = [url]
        num_page = 2
        print(f'1: {url}')
        soup = self.get_soup(url)
        while True:
            pages = soup.find('span', class_='pagebox')
            try:
                link = pages.find('a', text=str(num_page)).get("href")
                link = 'https://docplan.ru/' + link[3:]
                print(f'{str(num_page)}: {link}')
                urls.append(link)
                soup = scrap.get_soup(link)
                num_page += 1
            except:
                break
        return urls

    def get_ntd(self, url):
        soup = self.get_soup(url)
        tab = soup.find('table', class_='doctab2')
        rows = tab.find_all('tr')
        ntd_info = {
            'number': '',
            'name': '',
            'status': '',
            'new': [],
            'old': [],
        }
        for row in rows:
            row_right = row.find('td', align="right")
            if row_right != None:
                row_left = row_right.parent.find('td', align="left")
                if row_right.text == 'Обозначение:':
                    try:
                        ntd_number = row_left.find(
                            'a', target='_blank').get('title')
                        ntd_info['number'] = ntd_number
                    except:
                        ntd_number = row_left.text
                        ntd_info['number'] = ntd_number
                elif row_right.text == 'Статус:':
                    ntd_status = row_left.text
                    ntd_info['status'] = ntd_status
                elif row_right.text == 'Название рус.:':
                    ntd_name = row_left.text
                    ntd_info['name'] = ntd_name
                elif row_right.text == 'Заменяющий:':
                    for txt in row_left.find_all('a'):
                        ntd_info['new'].append(txt.text)
                elif row_right.text == 'Взамен:':
                    for txt in row_left.find_all('a'):
                        ntd_info['old'].append(txt.text)
        return ntd_info


if __name__ in '__main__':
    scrap = Scraper()
    wb = xlsxwriter.Workbook('ntd_sup.xlsx')
    ws = wb.add_worksheet('test')
    ws.write(0, 0, 'ntd_short')
    ws.write(0, 1, 'ntd_full')
    ws.write(0, 2, 'status')
    ws.write(0, 3, 'new')
    ws.write(0, 4, 'old')

    url = 'https://docplan.ru/list2.htm'
    url_type = scrap.get_url_type(url)

    num_row = 1
    for ntd_name, ntd_link in url_type:
        print(f'\n{ntd_name}: {ntd_link}')
        ntd_pages = scrap.get_ntd_pages(ntd_link)
        for page_link in ntd_pages:
            tb_rows = scrap.get_ntd_list(page_link)
            for tb_name, tb_link in tb_rows:
                ntd_info = scrap.get_ntd(tb_link)
                print(f"{ntd_info['number']} {ntd_info['name']}")
                ws.write(num_row, 0, ntd_info['number'])
                ws.write(
                    num_row, 1, f"{ntd_info['number']} {ntd_info['name']}")
                ws.write(num_row, 2, ntd_info['status'])
                ws.write(num_row, 3, '; '.join(ntd_info['new']))
                ws.write(num_row, 4, '; '.join(ntd_info['old']))
                num_row += 1
                print(f"---------------------------------------")
    wb.close()
