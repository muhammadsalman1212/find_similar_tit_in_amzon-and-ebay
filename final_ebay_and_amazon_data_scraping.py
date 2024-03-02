import csv
import time
from fuzzywuzzy import fuzz
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

delete_old_csv_data = input("[info] Do you want to delete old data from amazon_details.csv file? (yes/no): ")
search_item = input("[info] Enter the product you want to search for: ")
how_many_pages = int(input("[info] How many pages do you want to scrape: "))





def find_matching_titles(title, title_list, threshold=70):
    matching_titles = []

    for amazon_title in title_list:
        similarity_ratio = fuzz.token_sort_ratio(title, amazon_title)
        if similarity_ratio >= threshold:
            matching_titles.append((amazon_title, similarity_ratio))

    return matching_titles

ua = UserAgent()

random_user_agent = ua.random

options = webdriver.ChromeOptions()
options.add_argument(f"user-agent={random_user_agent}")

driver = webdriver.Chrome(options=options)

driver.get("https://ebay.com")
driver.maximize_window()
time.sleep(5)

def delete_old_data():
    with open('amazon_details.csv', 'r') as file:
        first_line = file.readline()
        if not first_line:  # agar first line mein kuch nahi ha to ye ho ga
            print("There's no data in the CSV file.")
            return

    # agar csv mein d ata ho ga to ye ho g run
    if delete_old_csv_data.lower() == 'yes':
        with open('amazon_details.csv', 'w') as file:
            file.truncate()#ye data delete krta ha

        print("All data deleted from the CSV file.")
    else:
        print("No data deleted from the CSV file.")

delete_old_data()

def search_your_product(search_product):
    time.sleep(5)
    search_input = driver.find_element(By.CLASS_NAME, "ui-autocomplete-input")
    search_input.send_keys(search_product)
    search_input.send_keys(Keys.ENTER)
    time.sleep(8)

search_your_product(search_item)

def twoforty_pages():
    pages_button = driver.find_element(By.XPATH, '//*[@id="srp-ipp-menu"]/button')
    time.sleep(5)
    pages_button.click()

    element = driver.find_element(By.XPATH, "//div[@class='srp-ipp']//li[2]//a[1]")

    href_value = element.get_attribute("href")

    print("The href value is:", href_value)
    driver.get(href_value)

    time.sleep(7)

twoforty_pages()


titles_list = []


def pages(how_much_page):
    try:
        for i in range(how_much_page):
            time.sleep(5)
            titles = driver.find_elements(By.CSS_SELECTOR, "div.s-item__title span")
            # Scroll karein
            actions = ActionChains(driver)
            actions.move_to_element(titles[-1]).perform()
            for all_title in titles:
                header = ["amazon_products_titles"]

                with open('all_products_titles.csv', 'a+', encoding='utf-8', newline='') as file:
                    writer = csv.writer(file)

                    # Write header
                    if file.tell() == 0:  # Check if file is empty
                        writer.writerow(header)

                    writer.writerow([all_title])



                titles_list.append(all_title.text)
            time.sleep(6)
            next_page = driver.find_element(By.XPATH, "//a[@aria-label='Go to next search page']")
            next_page.click()


        # now i want to skip 1st title from list
    except:
        pass

pages(how_many_pages)

title_list = titles_list[1:]
print(title_list)

try:
    driver.get("https://amazon.com")
except:
    for i in range(3):
        driver.refresh()
    driver.get("https://amazon.com")

simality_list = []
all_price_list =[]

try:
    for title_or_ebay in titles_list:
        time.sleep(12)
        search_input = driver.find_element(By.ID, "twotabsearchtextbox")
        search_input.send_keys(title_or_ebay)
        search_input.send_keys(Keys.ENTER)
        time.sleep(5)
        amazon_tit_list = []
        # amazon_titles = driver.find_elements(By.CSS_SELECTOR, "h2.a-size-mini a.a-link-normal span.a-size-medium")
        amazon_titles = driver.find_elements(By.CSS_SELECTOR, "h2.a-size-mini a.a-link-normal span")
        for all_amazon_titles in amazon_titles:
            title_text = all_amazon_titles.text
            amazon_tit_list.append(title_text)
            # print(amazon_tit_list)
        matching_titles = find_matching_titles(title_or_ebay, amazon_tit_list)

        simality_list.append(matching_titles)


        try:
            for match in matching_titles:
                print(f"{match[0]}")
                print(f"matching Title: {match[0]}, similarity: {match[1]}%")
                element = driver.find_element(By.XPATH,
                                              f'//a[@class="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal"]//span[text()="{match[0]}"]')
                element.click()
                time.sleep(4)
                price = driver.find_element(By.XPATH, '//span[@class="a-price-whole"]')
                price_text = price.text

                header = ["price", "matching_title"]

                with open('amazon_details.csv', 'a+', encoding='utf-8', newline='') as file:
                    writer = csv.writer(file)

                    # Write header
                    if file.tell() == 0:  # Check if file is empty
                        writer.writerow(header)

                    writer.writerow([price_text, match[0]])



                all_price_list.append(price_text)

                driver.back()
                time.sleep(10)
        except:
            pass



        time.sleep(5)
        delete_input = driver.find_element(By.ID, "twotabsearchtextbox")
        delete_input.send_keys(Keys.CONTROL + "a")
        delete_input.send_keys(Keys.DELETE)
except:
    pass



driver.quit()







