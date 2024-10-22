import base64
import csv
import tkinter
import sys
import pyodbc as odbc
import os
import selenium
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

import getpass
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from tkinter import messagebox


USERNAME = getpass.getuser()
CHROME= 'C:/Users/alejandro.palacio/chromedriver.exe'

FILE_PATH = f'C:/Users/{USERNAME}/Desktop'
OPTIONS = Options()
OPTIONS.add_argument("--disable-popup-blocking")
DRIVER = selenium.webdriver.Chrome(options=OPTIONS)


def create_file():
    with open(f'{FILE_PATH}/output.csv', 'w') as file_1:
        writer = csv.writer(file_1)
        data = [['server', 'results']]
        for row in data:
            writer.writerow(row)


def write_to_file(server, result):
    with open(f'{FILE_PATH}/output.csv', 'a') as file_1:
        writer = csv.writer(file_1)
        data = [server, result]
        writer.writerow(data)


def remove_file():
    if os.path.isfile(f'{FILE_PATH}/output.csv'):
        os.remove(f'{FILE_PATH}/output.csv')


def run_sql(env):
    character = 'D'
    if character in env:
        env += '%'
        print(env)
        sql_query =  f"""SELECT server_name
         FROM inv.server with (NOLOCK)
         WHERE 1 = 1
         and pod+site+client_code like '{env}'
         AND inventory_status_id = 1
         and server_function = 'Web Server'
         and product = 'Ultipro'
         and server_name not like '%98%'
         and server_name not like '%99%'"""
    else:
        sql_query = f"""SELECT server_name
         FROM inv.server with (NOLOCK)
         WHERE 1 = 1
         and pod+site+client_code = '{env}'
         AND inventory_status_id = 1
         and server_function = 'Web Server'
         and product = 'Ultipro'
         and server_name not like '%98%'
         and server_name not like '%99%'"""

    conn_results = []
    connection_string = (
        r'DRIVER={ODBC Driver 13 for SQL Server};'
        f'SERVER=E0IDWHDB01;'
        r'DATABASE={InfraWH};'
        r'Trusted_Connection=yes;'
    )
    conn = odbc.connect(connection_string)
    cursor_1 = conn.cursor()
    cursor_1.execute(sql_query)
    conn_results=(cursor_1.fetchall())
    return conn_results


def remove_spec_characters(server):
    s = server
    filtered_s = ''.join(c for c in s if c.isalnum())
    return(filtered_s)

def screenshot(x):
    DRIVER.save_screenshot(f'{FILE_PATH}/screenshot{x}.png')

def check_web_server_login (name, app):
    name = name.lower()
    if name.startswith('t') :
        site = f'https://{name}:9090/login.aspx'
    elif name.startswith('g'):
        sys.exit(1)
    else:
        site = f'https://{name}:9090/login.aspx'

    try:
        DRIVER.get(site)
    except exception:
        write_to_file(name, "fail, unable to hit Site")
        screenshot(1)


    DRIVER.find_element(By.ID,"details-button").click()
    DRIVER.find_element(By.ID, "proceed-link").click()

    try:
        login = DRIVER.find_element(webdriver.common.by.By.ID, "ctl00_Content_Login1_UserName")
        login.send_keys(f'{entry_user.get()}')
    except NoSuchElementException:
        write_to_file(name, "fail, no such element at ctl00_Content_Login1_UserName")
        screenshot(2)


    try:
        pw = DRIVER.find_element(webdriver.common.by.By.ID, "ctl00_Content_Login1_Password")
        pw.send_keys(f'{entry_pw.get()}')
    except NoSuchElementException:
        write_to_file(name, "fail, no such element ctl00_Content_Login1_Password")
        screenshot(3)

    try:
        DRIVER.find_element(By.NAME, "ctl00$Content$Login1$LoginButton").click()
    except NoSuchElementException:
        write_to_file(name, "fail, no such element ctl00$Content$Login1$LoginButton")
        screenshot(4)

    try:
        DRIVER.find_element(webdriver.common.by.By.ID, "ctl00_Content_warnMsg")
        write_to_file(name, "fail, Bad username/password combo")
        messagebox.showinfo('information', 'finished check csv file')
        screenshot(5)
        sys.exit(1)
    except NoSuchElementException:
        try:
            DRIVER.find_element(By.ID, "nav-menu-button").click()
        except NoSuchElementException:
            if login_test(name):
                pass
            else:
                write_to_file(name, "fail, no such element nav-menu-button")
                screenshot(6)
        if app == 'BI':
            Bi_test(name)
        elif app == 'UTM':
            Utm_test(name)
        elif app == 'WFR':
            pass
            #Wfr_test(name)
        elif app == 'UTA':
            Uta_test(name)
        elif app == 'ONB':
            pass
            #Onb_test(name)
        elif app == 'REC':
            pass
            #Rec_test(name)
        else:
            login_test(name)


def login_test(name):
    try:
        DRIVER.find_element(By.ID, "link_home")
        write_to_file(name, "pass")
        return True
    except NoSuchElementException:
        write_to_file(name, "fail")
        screenshot(7)
        return False


def Bi_test(name):
    try:
        time.sleep(5)
        DRIVER.find_element(By.ID, "menu_admin").click()
    except NoSuchElementException:
        write_to_file(name, "fail, no such element menu_admin")
        screenshot(8)

    try:
        DRIVER.find_element(By.XPATH, '//*[@id="2137"]/div/ukg-nav-item').click()
        time.sleep(10)
    except NoSuchElementException:
        write_to_file(name, 'fail, no such element Business Intelligence, //*[@id="2137"]/div/ukg-nav-item')
        screenshot(9)

    try:
        element = DRIVER.find_element(By.CSS_SELECTOR, "[data-id='1932']")
        element.send_keys(Keys.Control + Keys.RETURN)
    except NoSuchElementException:
        write_to_file(name, 'fail, no such element Business Intelligence, //*[@id="1932"]')
        screenshot(10)
#BI test isnt working perfectly at the moment , its not opening the popup and im not quite sure why, might be something
# with this being selenium and us having anti automation stuff on our front end not an actual person clicking through

def Utm_test(name):
    try:
        time.sleep(5)
        DRIVER.find_element(By.ID, "menu_myself").click()

    except NoSuchElementException:
        write_to_file(name, "fail, no such element menu_my_team")
        screenshot(11)

    try:
        DRIVER.find_element(By.XPATH, '//*[@id="2148"]').click()
        time.sleep(20)
    except NoSuchElementException:
        write_to_file(name, 'fail, no such element UTM, //*[@id="2148"]')
        screenshot(12)


def Uta_test(name):
    try:
        time.sleep(5)
        DRIVER.find_element(By.ID, "menu_my_team").click()
        #write_to_file(name, "pass")
    except NoSuchElementException:
        write_to_file(name, "fail, no such element menu_my_team")
        screenshot(13)

    try:
        DRIVER.find_element(By.XPATH, '//*[@id="1411"]').click()
        time.sleep(20)
    except NoSuchElementException:
        write_to_file(name, 'fail, no such element UTA, //*[@id="1411"]')
        screenshot(14)

    DRIVER.switch_to.window(DRIVER.window_handles[1])

    try:
        DRIVER.find_element(By.XPATH, '//*[@id="wfmHeaderMenuBarTicker"]/li[2]/a')
        write_to_file(name, "Uta pass")

    except NoSuchElementException:
        write_to_file(name, "Uta fail")
        screenshot(15)

    DRIVER.close()
    DRIVER.switch_to.window(DRIVER.window_handles[0])





def run_gui(app, web_list):
    x= len(web_list)
    i = 0
    for server in (web_list):
        name = server
        name = remove_spec_characters(name)
        check_web_server_login(name, app)
        i+= 1
    if i == x:
        messagebox.showinfo('information','finished check csv file')
        sys.exit()



def initial_steps():
    remove_file()
    entry_1 = entry.get()
    pw_1 = entry_pw.get()
    syn_user = entry_user.get()
    env = entry_1.strip()
    web_server_list = run_sql(env)
    web_server_list = list(web_server_list)
    create_file()
    return web_server_list


def login_only():
    web_server_list = initial_steps()
    run_gui(app='login', web_list= web_server_list)

def Bi():
    web_server_list = initial_steps()
    run_gui(app='bi', web_list= web_server_list)

def UTM():
    web_server_list = initial_steps()
    run_gui(app='UTM', web_list= web_server_list)

def WFR():
    web_server_list = initial_steps()
    run_gui(app='WFR', web_list= web_server_list)

def UTA():
    web_server_list = initial_steps()
    run_gui(app='UTA', web_list= web_server_list)


root = tkinter.Tk()
root.title("Web server Health check")
root.config(width=100, height=100 , padx=10, pady=10)

Environment_title = tkinter.Label(root, text= 'Environment')
Environment_title.grid(row=0, column =0 , padx=2 ,pady=2)
entry =tkinter.Entry(root)
entry.grid(row=0, column =1 , padx=2 ,pady=2)

label_2 = tkinter.Label(root, text= 'Username')
label_2.grid(row=1, column =0 , padx=2 ,pady=2)
entry_user =tkinter.Entry(root)
entry_user.insert(0,string='Amores')
entry_user.grid(row=1, column =1 , padx=2 ,pady=2)

Label_3 = tkinter.Label(root, text= 'Password')
Label_3.grid(row=3, column =0 , padx=2 ,pady=2)
entry_pw =tkinter.Entry(root)
entry_pw.insert(0,string='Password')
entry_pw.config(show="*")
entry_pw.grid(row=3, column =1 , padx=2 ,pady=2)

button = tkinter.Button(root, text='Login only',command=login_only)
button.grid(row=4, column =0 , padx=2 ,pady=2)

cognos = tkinter.Button(root, text='BI (cognos)', command=Bi)
cognos.grid(row=4, column=1 , padx= 2, pady=2 )

uta = tkinter.Button(root, text='UTA', command=UTA)
uta.grid(row=4, column=2 , padx= 2, pady=2 )

wfd = tkinter.Button(root, text='WFD/WFR', command=WFR)
wfd.grid(row=5, column=1 , padx= 2, pady=2 )

utm = tkinter.Button(root, text='UTM', command=UTM)
utm.grid(row=5, column=0 , padx= 2, pady=2 )

label_4 = tkinter.Label(root, text='Please use this app on a Admin box')
label_4.grid(row=6, column =1 , padx=2 ,pady=2)

root.mainloop()








