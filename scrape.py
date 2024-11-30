import time
from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
AUTH = 'brd-customer-hl_2750264c-zone-ai_webscraper:7206apd2sh0a'
SBR_WEBDRIVER = f'https://{AUTH}@brd.superproxy.io:9515'


def scrape_website(website):
    sbr_connection = ChromiumRemoteConnection(SBR_WEBDRIVER, 'goog', 'chrome')
    with Remote(sbr_connection, options=ChromeOptions()) as driver:
        print('Connected! Navigating...')
        driver.get(website)
        # print('Taking page screenshot to file page.png')
        # driver.get_screenshot_as_file('./page.png')
        # print('Navigated! Scraping page content...')
        html = driver.page_source
        return html


def extract_body_content(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    body_content = soup.body
    if body_content:
        return str(body_content)
    return ""


def clean_body_content(body_content):
    soup = BeautifulSoup(body_content, 'html.parser')
    for script_or_style in soup(['scripts', 'style']):
        script_or_style.extract()

    cleaned_body_content = soup.get_text(separator='\n')
    cleaned_body_content = "\n".join(
        line.strip() for line in cleaned_body_content.splitlines() if line.strip()
    )

    return cleaned_body_content


def split_dom_content(content, max_length=6000):
    return [
        content[i:i+max_length] for i in range(0, len(content), max_length)
    ]
