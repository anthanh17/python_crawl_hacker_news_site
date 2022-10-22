import requests, bs4, csv
from typing import Optional

def download_page(url: str, param: dict) -> Optional[str]: # url can None => Optional
    res = requests.get(url, param)
    if res.status_code != requests.codes.ok:
        print(f'Cannot get page, eror: {res.status_code}')
        return
    return res.text

if __name__ == '__main__':
    with open('hackernews.csv', 'w', newline = '') as file_output:
        headers = ['id', 'title', 'url', 'point', 'comments']
        writer = csv.DictWriter(file_output, delimiter = ',', lineterminator = '\n', fieldnames = headers)
        writer.writeheader()

        for count in range(10):
            param = {"p": count+1}
            html = download_page('https://news.ycombinator.com/news', param)
            if html is None: 
                print(f"Cannot get page {count+1}.") 
                continue
            
            bs_obj = bs4.BeautifulSoup(html, 'html.parser')

            id = bs_obj.find_all('span', class_ = "rank")
            title_and_link = bs_obj.find_all('span', class_ = "titleline")
            score = bs_obj.find_all('span', class_ = "score")
            comment = bs_obj.find_all('span', class_ = "subline")

            for idx in range(len(id)):
                if idx < len(score) and idx < len(comment):
                    writer.writerow({
                        headers[0]:id[idx].contents[0][:-1],
                        headers[1]:title_and_link[idx].find('a').contents[0],
                        headers[2]:title_and_link[idx].find('a').attrs['href'],
                        headers[3]:score[idx].contents[0],
                        headers[4]:comment[idx].find_all('a')[3].contents[0][:-8]
                    })
                elif idx >= len(score) and idx < len(comment):
                    writer.writerow({
                        headers[0]:id[idx].contents[0][:-1],
                        headers[1]:title_and_link[idx].find('a').contents[0],
                        headers[2]:title_and_link[idx].find('a').attrs['href'],
                        headers[3]:"",
                        headers[4]:comment[idx].find_all('a')[3].contents[0][:-8]
                    })
                elif idx < len(score) and idx >= len(comment):
                    writer.writerow({
                        headers[0]:id[idx].contents[0][:-1],
                        headers[1]:title_and_link[idx].find('a').contents[0],
                        headers[2]:title_and_link[idx].find('a').attrs['href'],
                        headers[3]:score[idx].contents[0],
                        headers[4]:""
                    })