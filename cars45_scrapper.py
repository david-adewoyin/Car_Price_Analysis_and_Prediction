import pandas as pd
from utils import intercept_route
from playwright.sync_api import sync_playwright, BrowserContext

DOMAIN = "https://www.cars45.com/"
URL = "https://www.cars45.com/listing?filter_inspection=Inspected"


# fetch car data from is individual listing page
def fetch_car_data(context: BrowserContext, url: str):
    page = context.new_page()

    page.route("**/*", intercept_route)
    page.goto(url, wait_until='domcontentloaded', timeout=10_000)

    car = {}
    details = page.query_selector_all(".car-details .general-info div")
  
    for item in details:
        if item.query_selector('span').inner_text() == 'MAKE':
            car['Brand'] = item.query_selector("p").inner_text()
        elif item.query_selector('span').inner_text() == 'MODEL':
            car['Model'] = item.query_selector("p").inner_text()
        elif item.query_selector('span').inner_text() == 'MILEAGE':
            car['Mileage'] = item.query_selector("p").inner_text()
        elif item.query_selector('span').inner_text() == 'CONDITION':
            car['Condition'] = item.query_selector("p").inner_text()
        elif item.query_selector('span').inner_text() == 'YEAR OF MANUFACTURE':
            car['Year'] = item.query_selector("p").inner_text()
        elif item.query_selector('span').inner_text() == 'COLOUR':
            car['Color'] = item.query_selector("p").inner_text()
        elif item.query_selector('span').inner_text() == 'ENGINE SIZE':
            car['Engine Size'] = item.query_selector("p").inner_text()
        elif item.query_selector('span').inner_text() == 'NUMBER OF CYLINDERS':
            car['Number of Cylinders'] = item.query_selector("p").inner_text()
  
    car['Price'] = page.query_selector(".main-details__name h5").inner_text()
    page.close()
    return car




# scrap cars pages from grid listings page
def scrap_cars_from_page(context: BrowserContext, url: str, is_homepage=False):
    cars = []
    page = context.new_page()

    page.route("**/*", intercept_route)
    page.goto(url, wait_until='domcontentloaded', timeout=50_000)

    cars_list = page.query_selector_all(".cars-grid a")

    count = 0 
    for car_item in cars_list:
        car_url = DOMAIN + car_item.get_attribute("href")
        try:
            car = fetch_car_data(context, car_url)
            cars.append(car)
            if count % 10 == 0:
                print(f'parsed {count} cars from page')
            count =count +1

        except Exception as e:
            print(f"error :{e}")

    if is_homepage:
        total_pages = page.query_selector_all(
            ".b-pagination__item")[-2].query_selector("a").inner_text()
        total_pages_count = int(total_pages.split()[-1])
        current_page_count = 1
        page.close()
        return cars, total_pages_count, current_page_count
    
    page.close()
    return cars


def main():
    # list to store lists of cars
    CARS = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
 
        print("starting web scrapper...........")

        cars, total_pages_count, current_page_count = scrap_cars_from_page(context=context, url=URL, is_homepage=True)
        CARS.extend(cars)
        print(f"Scrapped {len(cars)} cars from page 1")

        # scrap all the remaining pages
        while current_page_count < total_pages_count:
            next = current_page_count + 1
            next_url = f'https://www.cars45.com/listing/page{next}?filter_inspection=Inspected'
            print(f"scrapping page {current_page_count +1}")
            try:
                cars = scrap_cars_from_page(context, next_url)
                print(f"Scrapped {len(cars)} cars from page {current_page_count+1}")
                CARS.extend(cars)
            except Exception as e:
                print("error",e)
            current_page_count = current_page_count + 1
        
        context.close()
        df = pd.DataFrame(CARS)
        df.to_csv("data/cars45.csv")

if __name__ == '__main__':
    main()
