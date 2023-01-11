import pandas as pd
from utils import intercept_route
from playwright.sync_api import sync_playwright, BrowserContext

DOMAIN = "https://autochek.africa"
URL = "https://autochek.africa/ng/cars-for-sale"


# fetch car data from is individual listing page
def fetch_car_data(context: BrowserContext, url: str, model: str,year:str):
    page = context.new_page()

    page.route("**/*", intercept_route)
    page.goto(url, wait_until='domcontentloaded', timeout=30_000)

    title_card = page.query_selector(
        '.tw-w-full').inner_text().strip().split()
    subtitle_card = page.query_selector_all(
        ".details-item-container .text")
    desc_card = page.query_selector_all(".description-items div")

    brand = title_card[0]
    mileage = subtitle_card[0].inner_text().split()[0]
    condition = subtitle_card[2].inner_text()
    price = page.query_selector(".price").inner_text()
    price = page.query_selector(".price").inner_text()
    engine_type = desc_card[0].query_selector(".value").inner_text()
    engine_capacity = desc_card[1].query_selector(".value").inner_text()
    exterior_color = desc_card[-3].query_selector(".value").inner_text()
    ratings = None
    if condition.lower() != "new":
        ratings = page.query_selector(".tw-w-full span").inner_text()

    car = {
        "Brand": brand,
        "Model": model,
        "Year": year,
        "Mileage": mileage,
        "Condition": condition,
        "Price": price,
        "Engine Type": engine_type,
        "Engine Capacity": engine_capacity,
        "Exterior Color": exterior_color,
        "Ratings":  ratings
    }
    page.close()
    return car


# scrap cars pages from grid listings page
def scrap_cars_from_page(context: BrowserContext, url: str, is_homepage=False):
    cars = []
    page = context.new_page()

    page.route("**/*", intercept_route)
    page.goto(url, wait_until='domcontentloaded', timeout=30_000)
    page.wait_for_selector(".car-grid-container")
    page.mouse.wheel(0, 500)
    cars_container = page.query_selector(".car-grid-container")
    cars_list = cars_container.query_selector_all(".car-item")

    l = len(cars_list)
    # number of card on initial load is 8 ;f
    while l == 8:
        page.mouse.wheel(0,500)
        cars_container = page.query_selector(".car-grid-container")
        cars_list = cars_container.query_selector_all(".car-item")


    
    count = 0
    for car_item in cars_list:
        car_url = DOMAIN + car_item.query_selector("a").get_attribute("href")
        model = car_item.query_selector(".name").inner_text()
        year = car_item.query_selector(".year").inner_text()
        try:
            car = fetch_car_data(context, car_url, model,year)
            cars.append(car)
            if count % 10 == 0:
                print(f'parsed {count} cars from page')
            count =count +1
        except Exception as e:
            print(f"{e}")

    # if is_home_page get the total number of pages available to parse
    if is_homepage:
        total_pages = page.query_selector(
            "p.jsx-2193466571").inner_text().strip()
        total_pages_count = int(total_pages.split()[-1])
        current_page_count = 1
        page.close()
        return cars, total_pages_count, current_page_count

    page.close()
    return cars


def main():
    CARS = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()

        print("starting web scrapper...........")

        cars, total_pages_count, current_page_count = scrap_cars_from_page(
            context=context, url=URL, is_homepage=True)
        CARS.extend(cars)
        print(f"Scrapped {len(cars)} cars from page 1")
       
        # scrap all the remaining pages
        while current_page_count < total_pages_count:

            next_url = f'https://autochek.africa/ng/cars-for-sale?page_number={current_page_count + 1}'
            print(f"scrapping page {current_page_count +1}")
            try:
                cars = scrap_cars_from_page(context, next_url)
                print(f"Scrapped {len(cars)} cars from page {current_page_count+1}")
                CARS.extend(cars)
            except Exception as e:
                print(e)
            current_page_count = current_page_count + 1
        

        context.close()
        df = pd.DataFrame(CARS)
        df.to_csv("data/autochek.csv")

if __name__ == '__main__':
    main()
