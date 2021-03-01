import requests
from bs4 import BeautifulSoup
import smtplib
import webbrowser


def get_link(command):
    com = ['flipkart', 'amazon']
    final_link = []
    for it in com:
        res = requests.get("https://google.com/search?q=" + command + str(it))
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")
        links = soup.select('.kCrYT a')
        for li in links[:1]:
            final_link.append('https://google.com/' + li.get('href'))
    return final_link


def scrape_amazon(url):
    headers = {
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'}
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    title = (soup.find(id='productTitle').get_text().strip())
    try:
        price = ((soup.find(id="priceblock_ourprice").get_text().strip())[2:])
    except AttributeError:
        price = ((soup.find(id="priceblock_dealprice").get_text().strip())[2:])
    try:
        price = float(price[0:(price.index(','))] + price[price.index(',') + 1:(len(price) - 3)])
    except ValueError:
        price = float(price[0:(len(price) - 3)])
    return title, price


def scrape_flip(url):
    headers = {
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'}
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")
    title = soup.find('span', {'class': '_35KyD6'}).text
    # try:
    # price = soup.find('div', {'class': '_1vC4OE'}).text
    price = soup.find('div', {'class': '_1vC4OE _3qQ9m1'}).text
    # except:
    #     price = soup.find('div', {'class': '_1vC4OE'}).text
    try:
        price = float(price[1:(price.index(','))] + price[price.index(',') + 1:(len(price))])
    except ValueError:
        price = float(price[1:])
    return title, price


def send_mail(name, link, price):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login('tirthdhara108@gmail.com', 'xjcjbgdomnwwcrcb')
    subject = "HEY HERE IS YOUR SELECTED PRODUCT  " + name
    body = "If you wanna check " + link
    msg = f'Subject:{subject}\n\n body: {subject}\n {body} \n Current price :{price}'
    server.sendmail('tirthdhara108@gmail.com', 'tirth.170410107110@gmail.com', msg)
    server.quit()


if __name__ == '__main__':
    print("please tell us how many items do you want to search for??")
    items = int(input())
    url_in = []
    final = []
    for i in range(items):
        print(
            'Please enter the Keywords (Name,company,model_spec) of your product ' + str(i) + ' you want your price :')
        url_in.extend(get_link(input()))
        print("Total [ " + str(len(url_in)) + " ] links.")
        print(url_in)
    for ind in range(0, len(url_in)):
        if ind % 2 == 0:
            final.append([scrape_flip(url=url_in[ind]), 'FLIPKART'])  # L'OREAL PARIS Total repair 5 Shampoo
        else:                                                         # horlicks classic malt 1kg
            final.append([scrape_amazon(url=url_in[ind]), 'AMAZON'])  # Samsung m31 6gb
    for f in final:
        print(f)
    choice = input("do you want to open the websites ")
    choices = ['yes', 'Y', 'y', 'YES', 'Yes']
    if choice in choices:
        for link in url_in:
            webbrowser.open(link)
    else:
        for link in url_in:
            print(link)
    # https://www.amazon.in/gp/product/B07HGGYWL6?pf_rd_r=E9462YT5VD5FWZH72YQD&pf_rd_p=649eac15-05ce-45c0-86ac-3e413b8ba3d4
    # https://www.amazon.in/Test-Exclusive-553/dp/B0784D7NFQ/ref=pd_di_sccai_4/257-3892071-7423639?_encoding=UTF8&pd_rd_i=B0784D7NFQ&pd_rd_r=6592a879-3e8d-49ad-b82d-8df4ef50e58b&pd_rd_w=63lsr&pd_rd_wg=ve70V&pf_rd_p=a1f3aa5a-f05d-4e2d-b84b-6ef88e21fb7e&pf_rd_r=N8JQCX1P0RZ60GHTR6A6&psc=1&refRID=N8JQCX1P0RZ60GHTR6A6
    # https://www.amazon.in/Redmi-Note-Pro-Storage-Processor/dp/B07X4PKGSN/ref=psdc_1805560031_t3_B0784D7NFQ
    # https://www.amazon.in/Test-Exclusive-749/dp/B07DJ8K2KT/ref=psdc_1805560031_t2_B07DJLVJ5M
