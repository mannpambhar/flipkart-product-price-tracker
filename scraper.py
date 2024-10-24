import requests
from bs4 import BeautifulSoup

def fetch_product_details(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0",
        "Referer": "https://www.flipkart.com/",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Connection": "keep-alive"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Ensure request was successful
    except requests.exceptions.RequestException as e:
        print(f"Error fetching product details: {e}")
        return None

    soup = BeautifulSoup(response.content, 'html.parser')

    try:
        title = soup.find("span", {"class": "VU-ZEz"}).text.strip()
    except AttributeError:
        title = "Title not found"

    try:
        current_price = soup.find("div", {"class": "Nx9bqj CxhGGd"}).text.strip()
    except AttributeError:
        current_price = "Price not found"

    try:
        description = soup.find("div", {"class": "yN+eNk"}).text.strip()
    except AttributeError:
        description = "Description not found"

    try:
        rating = soup.find("div", {"class": "ipqd2A"}).text.strip()
    except AttributeError:
        rating = "Rating not found"

    try:
        reviews = soup.find("div", {"class": "review-class-name"}).text.strip()  # Update with actual class name
    except AttributeError:
        reviews = "Reviews not found"

    try:
        total_purchases = soup.find("div", {"class": "purchase-class-name"}).text.strip()  # Update with actual class name
    except AttributeError:
        total_purchases = "Total Purchases not found"

    return {
        "title": title,
        "current_price": current_price,
        "description": description,
        "rating": rating,
        "reviews": reviews,
        "total_purchases": total_purchases,
    }
