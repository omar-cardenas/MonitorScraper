import pandas as pd
import sqlite3 as sqlite
from bs4 import BeautifulSoup
import requests
from datetime import datetime


def create_dataframe() -> pd.DataFrame:
    # initialize or connect to DB
    db_connection = sqlite.connect('monitors.db')
    
    sql = "SELECT * FROM monitors;"
    result_cursor = db_connection.execute(sql)

    frame_columns = ["product_id", "product_name", "resolution", "panel_type", "brand", "price", "url", "image_src"]

    dataframe = pd.DataFrame(columns=frame_columns)

    for row in result_cursor:
        product_data = [row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]]
        length = len(dataframe)
        dataframe.loc[length] = product_data

    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_colwidth', None)
    
    db_connection.close()

    return dataframe

def export_dataframe_to_csv(dataframe : pd.DataFrame) -> None:
    full_path = r'/Users/omarcardenas/Desktop/Monitor_data.csv'
    dataframe.to_csv(full_path, index = False)


def db_print_table():
    # initialize or connect to DB
    db_connection = sqlite.connect('monitors.db')
    
    sql = "SELECT * FROM monitors;"
    c = db_connection.execute(sql)
    print(f"TABLE CONTENTS FOR 'monitors': ({get_table_size()} entries) ")
    for row in c:
        db_entry = f"product_id: {row[0]}, Name:{row[1]}, Resolution: {row[2]}, Panel type: {row[3]}, Brand: {row[4]}, Price: {row[5]}"
        print(db_entry)

    db_connection.close()


def product_in_db(product_id) -> bool:
    # initialize or connect to DB
    db_connection = sqlite.connect('monitors.db')

    #select 1 from monitors <where clause>, returns 1 if a record matches the clause
    #returns 1 if entry exists or 0 otherwise
    sql = f"SELECT EXISTS(SELECT 1 FROM monitors WHERE PRODUCT_ID = {product_id});"
    c = db_connection.execute(sql)
    answer = c.fetchone()[0]
    db_connection.close()

    if answer == 1:
        return True
    return False

def insert_to_db(product_data):
    # initialize or connect to DB
    db_connection = sqlite.connect('monitors.db')
    
    product_id = product_data[0]
    name = product_data[1]
    resolution = product_data[2]
    panel_type = product_data[3]
    brand = product_data[4]
    price = product_data[5]
    product_url = product_data[6]
    image_src = product_data[7]

    cursor = db_connection.cursor()
    sql = f"INSERT INTO monitors (PRODUCT_ID, NAME, RESOLUTION, PANEL_TYPE, BRAND, PRICE, PRODUCT_URL, IMAGE_SRC) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
    cursor.execute(sql, (product_id, name, resolution, panel_type, brand, price, product_url, image_src))
    db_connection.commit()
    db_connection.close()

    print("insertion successful")

def get_product_price(product_id) -> float:
    # initialize or connect to DB
    db_connection = sqlite.connect('monitors.db')
    sql = f"SELECT PRICE FROM monitors WHERE PRODUCT_ID = {product_id};"
    result_cursor = db_connection.execute(sql)
    price = result_cursor.fetchone()[0]
    db_connection.close()
    return price

def update_product_price(product_id, price):
    # initialize or connect to DB
    db_connection = sqlite.connect('monitors.db')
    
    sql = f"UPDATE monitors SET PRICE = {price} WHERE PRODUCT_ID = {product_id};"
    db_connection.execute(sql)
    db_connection.commit()
    db_connection.close()
    print("price updated")

def get_table_size() -> int:
    # initialize or connect to DB
    db_connection = sqlite.connect('monitors.db')

    sql = "SELECT COUNT(*) FROM monitors;"
    cursor = db_connection.execute(sql)
    size = cursor.fetchone()[0]
    db_connection.close()

    return size

def create_table():
    #initialize or connect to DB
    db_connection = sqlite.connect('monitors.db')
    #product_id INTEGER PRIMARY KEY AUTOINCREMENT
    sql = """
        CREATE TABLE IF NOT EXISTS monitors 
        (PRODUCT_ID INTEGER PRIMARY KEY, 
        NAME TEXT NOT NULL,
        RESOLUTION TEXT,
        PANEL_TYPE TEXT,
        BRAND TEXT NOT NULL, 
        PRICE REAL, 
        PRODUCT_URL TEXT, 
        IMAGE_SRC TEXT);"""

    db_connection.execute(sql)
    db_connection.commit()
    db_connection.close()

def drop_table():
    #initialize or connect to DB
    db_connection = sqlite.connect('monitors.db')

    sql = "DROP TABLE IF EXISTS monitors;"
    db_connection.execute(sql)
    db_connection.commit()
    db_connection.close()


def find_resolution(description: str) -> str:
    if "1080" in description:
        return "1080"
    elif "1440" in description:
        return "1440"
    elif "2160" in description:
        return "2160"

    return "not found"

def find_panel(description: str) -> str:
    if "OLED" in description:
        return "OLED"
    return "LCD"

def scrape():


    webpage = "https://www.microcenter.com"
    #url by pages for all monitors
    page_url = "https://www.microcenter.com/search/search_results.aspx?N=4294966896+4294819462&NTK=all&page=1&cat=Gaming-:-MicroCenter"
    #find how many pages there are for monitors
    page = requests.get(page_url)
    soup = BeautifulSoup(page.content, 'html.parser')
    ul_tag = soup.find('ul', {"class": 'pages inline'})
    list_items = ul_tag.find_all('li')
    # subtract 2 to not take into account the 2 <li>s showing the current page number and class
    number_of_pages = len(list_items) - 2
    #print(f"Number of pages: {number_of_pages}")

    page_number = 1
    while page_number <= number_of_pages:
        page_url = f"https://www.microcenter.com/search/search_results.aspx?N=4294966896+4294819462&NTK=all&page={page_number}&cat=Gaming-:-MicroCenter"
        print(f"scraping page: {page_number}")
        page = requests.get(page_url)

        soup = BeautifulSoup(page.content, 'html.parser')

        #these divs are holding the data for each product
        products = soup.findAll('div', { "class" : 'result_left'})
        #print(products)

        for product in products:
            #retrieve the tag holding the product information (the first <a> tag in each result_left div)
            a_tag = product.find('a')
            #retrieve specific attributes of a html element with get()
            product_id =a_tag.get('data-id')
            name = a_tag.get('data-name')
            #find out what resolution the monitor is
            resolution = find_resolution(name)
            panel_type = find_panel(name)
            brand = a_tag.get('data-brand')
            price = float(a_tag.get('data-price'))
            
            #error check, incase attribute names are changed in website
            if product_id is None or name is None or brand is None or price is None:
                print("webpage elements have been changed, inspect website")
                break

            # check if product_id already in DB and price the same, if so skip
            if product_in_db(product_id):
                if price == get_product_price(product_id) :
                    continue
                else:
                    update_product_price(product_id, price)
                    continue


            #get product webpage url and image from the next <a> tag in the result_left div
            second_a_tag = product.find_all('a')[1]
            product_url = webpage + second_a_tag.get('href')
            image_src = second_a_tag.find('img').get('src')

            product_data = [product_id, name, resolution, panel_type, brand, price, product_url, image_src]
            insert_to_db(product_data)


        page_number += 1
        

if __name__ == '__main__':

    current_time = datetime.now()
    # Convert to string
    datetime_string = current_time.strftime('%m-%d-%y %H:%M')
    print(f"Scraping starting on: {datetime_string}")
   
    # will only create table if it doesn't exist
    create_table()
    scrape()
    
    #OPTIONS TO DISPLAY DATA
    # db_print_table()
    # df = create_dataframe()
    # print(df)
    # export_dataframe_to_csv(df)

    print("Scraping complete")
