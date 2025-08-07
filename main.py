import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import openpyxl

def get_all_links(domain):
    try:
        response = requests.get(domain, timeout=5)
    except Exception as e:
        print(f"Ошибка при подключении к сайту: {e}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    links = set()
    for a_tag in soup.find_all('a', href=True):
        full_url = urljoin(domain, a_tag['href'])
        if urlparse(full_url).netloc == urlparse(domain).netloc:
            links.add(full_url.split('#')[0])  
    return list(links)

def check_link_status(url):
    try:
        response = requests.get(url, timeout=5)
        return response.status_code
    except requests.RequestException:
        return 'ERROR'

def write_to_excel(results):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(['URL', 'Status Code', 'Status'])
    for url, code in results:
        status = 'OK' if str(code).startswith('2') else 'ERROR'
        ws.append([url, code, status])
    wb.save('report.xlsx')
    print("✅ Отчет сохранен как report.xlsx")

if __name__ == "__main__":
    domain = input("Введите URL сайта: ").strip()
    if not domain.startswith("http"):
        domain = "https://" + domain

    print("🔍 Поиск ссылок...")
    links = get_all_links(domain)
    print(f"🔗 Найдено ссылок: {len(links)}")

    results = []
    for i, link in enumerate(links, 1):
        code = check_link_status(link)
        print(f"[{i}/{len(links)}] {link} --> {code}")
        results.append((link, code))

    write_to_excel(results)

# Testing URLS:
# https://books.toscrape.com/
# https://reqres.in/