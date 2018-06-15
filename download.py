from requestium import Session
import time

HOME_URL = 'https://www.t66y.com/'
START_URL = HOME_URL + 'thread0806.php?fid=25'
TORRENT_URL = 'http://www.rmdown.com/download.php'
XIAOMI_URL = 'https://d.miwifi.com/d2r'
XIAOMI_ACCOUNT = ''
XIAOMI_PASSWORD = ''
FETCH_INTERVAL = 60 * 60 * 24   # 间隔多久抓取一次1024首页

session = Session(webdriver_path='./chromedriver', browser='chrome', default_timeout=15,
                  webdriver_options={'arguments': ['headless']})
fetched_urls = set()


def start():
    res = session.get(START_URL)
    for item in res.xpath('//td/h3/a/@href'):
        data = item.extract()
        if data not in fetched_urls:
            fetched_urls.add(data)
            torrent_url = fetch_torrent_url(HOME_URL + data)
            download(torrent_url)


# test url: https://www.t66y.com/htm_data/25/1806/3169307.html
def fetch_torrent_url(url):
    print('正在打开' + url)
    res = session.get(url)
    mid_url = res.xpath('//div[@class="tpc_content do_not_catch"]/a/text()').extract_first()
    res = session.get(mid_url)
    reff = res.xpath('//form/input[@name="reff"]/@value').extract_first()
    ref = res.xpath('//form/input[@name="ref"]/@value').extract_first()
    torrent_url = TORRENT_URL + '?reff=' + reff + '&ref=' + ref
    return torrent_url


def xiaomi_login():
    session.driver.get(XIAOMI_URL)
    need_login = session.driver.find_element_by_id('login-download-button')
    if need_login:
        button = session.driver.find_element_by_class_name('clickable')
        button.click()
        time.sleep(2)
        username = session.driver.find_element_by_id('username')
        username.send_keys(XIAOMI_ACCOUNT)
        password = session.driver.find_element_by_id('pwd')
        password.send_keys(XIAOMI_PASSWORD)
        submit = session.driver.find_element_by_id('login-button')
        submit.submit()
        time.sleep(2)
        session.driver.save_screenshot('is_login_success.png')


# test download('https://sm.myapp.com/original/im/QQ9.0.3-9.0.3.23756.exe')
def download(url):
    url_input = session.driver.find_element_by_id('file-raw-url')
    url_input.send_keys(url)
    submit = session.driver.find_element_by_id('download-button')
    submit.click()
    time.sleep(5)


def main():
    while True:
        xiaomi_login()
        start()
        time.sleep(FETCH_INTERVAL)


if __name__ == '__main__':
    main()
