import time
import datetime
import logging
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_all_articles(driver, load_more_selector, date_limit):
    while True:
        try:
            load_more_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, load_more_selector))
            )
            load_more_button.click()
            logging.info("Clicked 'Load More' button")
            time.sleep(2)  # Adjust sleep time if necessary

            soup = BeautifulSoup(driver.page_source, "html.parser")
            articles = soup.find_all("div", class_="typeAndTime___3oQRN")
            if not articles:
                logging.info("No more articles found.")
                break

            last_article_date_str = articles[-1].text.strip()
            last_article_date_part = " ".join(last_article_date_str.split()[:3])
            last_article_date = datetime.datetime.strptime(last_article_date_part, "%b %d, %Y")

            if last_article_date < date_limit:
                logging.info("Last article date is older than date limit, stopping load")
                break
        except Exception as e:
            logging.error(f"Error clicking 'Load More' button or parsing date: {e}")
            break

def scrape_articles():
    url = "https://news.metal.com/list/industry/aluminium"
    
    # Calculate the date 45 days ago
    end_date = datetime.datetime.now()
    start_date = end_date - datetime.timedelta(days=45)

    # Setup Edge options
    edge_options = Options()
    edge_options.add_argument("--headless")  # Run in headless mode
    edge_options.add_argument("--disable-gpu")
    edge_options.add_argument("--no-sandbox")

    service = Service(executable_path=r"C:\Users\suren\Downloads\edgedriver_win64\msedgedriver.exe")  # Update this path
    driver = webdriver.Edge(service=service, options=edge_options)
    driver.get(url)
    logging.info("Navigated to URL")
   
    load_more_selector = ".footer___PvIjk"  # Update this selector if needed
    load_all_articles(driver, load_more_selector, start_date)
    
    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()
    
    articles = []
    
    for item in soup.find_all("div", class_="newsItem___wZtKx"):
        title_tag = item.find("div", class_="title___1baLV")
        date_tag = item.find("div", class_="typeAndTime___3oQRN")
        summary_tag = item.find("div", class_= "description___z7ktb")  
        
        if title_tag and date_tag:
            title = title_tag.text.strip()
            link = title_tag.parent["href"]
            date_str = date_tag.text.strip()
            
            date_part = " ".join(date_str.split()[:3])
            try:
                date = datetime.datetime.strptime(date_part, "%b %d, %Y")
            except ValueError:
                logging.warning(f"Date parsing error for article: {title}")
                continue
            
            if start_date <= date <= end_date:
                summary = summary_tag.text.strip() if summary_tag else "No summary available"
                articles.append({"title": title, "link": link, "date": date_str, "summary": summary})
    
    return articles

def save_articles_to_csv(articles, filename="articles.csv"):
    fieldnames = ["title", "link", "date", "summary"]
    
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for article in articles:
            writer.writerow(article)
    logging.info(f"Articles saved to {filename}")

if __name__ == "__main__":
    try:
        articles = scrape_articles()
        for article in articles:
            logging.info(f"Title: {article['title']}")
            logging.info(f"Link: {article['link']}")
            logging.info(f"Date: {article['date']}")
            logging.info(f"Summary: {article['summary']}\n")
        
        save_articles_to_csv(articles)
    except Exception as e:
        logging.error(f"An error occurred: {e}")
