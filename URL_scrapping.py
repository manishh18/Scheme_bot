from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
import csv


# Setup
driver_path = "C:\chromedriver-win64\chromedriver.exe"  # <-- change this
driver = webdriver.Chrome(service=Service(driver_path))
wait = WebDriverWait(driver, 10)
driver.get("https://www.myscheme.gov.in/search")

# Flags for visited pages
visited = [False] * 347  # Index 0 unused
all_links = []

def extract_links():
    # Wait for schemes to load and extract their hrefs
    wait.until(EC.presence_of_all_elements_located((By.XPATH, '//h2/a')))
    links = driver.find_elements(By.XPATH, '//h2/a')
    for link in links:
        href = link.get_attribute("href")
        if href:
            all_links.append(href)

# Start with page 1
visited[1] = True
extract_links()

while not all(visited[1:]):
    time.sleep(2)

    # Get all visible page numbers
    li_elements = driver.find_elements(By.XPATH, '//ul/li[not(contains(., "…"))]')
    
    page_nums = set()  # Use set to avoid duplicates
    for li in li_elements:
        try:
            raw_text = li.text
            numbers = re.findall(r'\d+', raw_text)  # Find all number groups like '1', '346'
            for num in numbers:
                page_nums.add(int(num))
        except:
            continue


    # Find the smallest unvisited page in visible list
    unvisited = [p for p in sorted(page_nums) if not visited[p]]
    if not unvisited:
        print("No new pages visible, pagination might be stuck.")
        break

    next_page = unvisited[0]
    print(f"Clicking page {next_page}")

    try:
        li_to_click = wait.until(EC.element_to_be_clickable(
        (By.XPATH, f'//ul/li[normalize-space(text())="{next_page}"]')
        ))
        driver.execute_script("arguments[0].scrollIntoView();", li_to_click)
        time.sleep(0.5)
        driver.execute_script("window.scrollBy(0, -150);")  # adjust scroll
        time.sleep(0.5)
        driver.execute_script("arguments[0].click();", li_to_click)

        visited[next_page] = True
        extract_links()

    except Exception as e:
        print(f"Error navigating to page {next_page}: {e}")
        break

print(f"\nCollected {len(all_links)} links from all pages.")

# Save links to CSV
with open('myscheme_links.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Link'])  # header
    for link in all_links:
        writer.writerow([link])

print(f"Saved {len(all_links)} links to 'myscheme_links.csv'")

driver.quit()
