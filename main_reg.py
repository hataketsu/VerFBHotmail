from selenium.webdriver import Chrome

from check_mail import check_for_code

Chrome = Chrome
cookies = open('./data/cookies.txt').readlines()
emails = open('./data/emails.txt').readlines()


def bake(driver, cookie):
    driver.delete_all_cookies()
    for pair in cookie.split(';'):
        print(pair)
        key, value = pair.split('=')
        key = key.strip()
        value = value.strip()
        if key:
            c = {'name': key, 'value': value, 'domain': 'm.facebook.com'}
            driver.add_cookie(c)


driver = Chrome()


def verify(cookie, email):
    email, password = email.split('|')
    driver.get('https://m.facebook.com/')
    bake(driver, cookie)
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
    verify(cookies[6], emails[7])
