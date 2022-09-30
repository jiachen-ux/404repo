#!/usr/bin/env python3

import cgi
from http.cookies import SimpleCookie
import os

import secret
from templates import after_login_incorrect, login_page
from templates import secret_page

def parse_cookies(cookie_string):
    cookies = cookie_string.split(";")
    result  = {}
    for cookie in cookies:
        split_cookie = cookie.split("=")
        result[split_cookie[0]] = split_cookie[1]
        
    return result

# cookies = parse_cookies(os.environ["HTTP_COOKIE"])

form = cgi.FieldStorage()

username = form.getfirst("username")
password = form.getfirst("password")

form_ok = username == secret.username and password == secret.password

cookie = SimpleCookie(os.environ["HTTP_COOKIE"])
cookie_username = None
cookie_password = None
if cookie.get("username"):
    cookie_username = cookie.get("username").value
if cookie.get("password"):
    cookie_password = cookie.get("password").value

cookie_ok = cookie_username == secret.username and cookie_password == secret.password

if cookie_ok:
    username = cookie_username
    password = cookie_password
print('Content-Type: text/html')

if form_ok:
    print(f'Set-Cookie: username={username}')
    print(f'Set-Cookie: password={password}')
print()
# if username is not None or ('logged' in cookies and cookies['logged'] == "true"):
if not username and not password:
    print(login_page())
elif username == secret.username and password == secret.password:
    print(secret_page(username, password))
else:
    print(after_login_incorrect())
    
