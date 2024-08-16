import re
from bs4 import BeautifulSoup

def extractPriceFromHtml(html_snippet):
    if not html_snippet:
        return None

    soup = BeautifulSoup(html_snippet, 'html.parser')
    text = soup.get_text(separator=' ', strip=True)
    pattern = re.compile(r'(\d{1,3}(?:\.\d{3})*(?:,\d{2}|\,-)?)')
    match = pattern.search(text)
    if match:
        return convertPrice(match.group(1))
    return None

def convertPrice(price_str):
    price_str = price_str.replace(',-', ',00')
    return float(price_str.replace('.', '').replace(',', '.'))

def extractPrices(item, ignored_value=None):
    if ignored_value is not None:
        if isinstance(ignored_value, str):
            ignored_value = extractPriceFromHtml(ignored_value)
        elif isinstance(ignored_value, (int, float)):
            ignored_value = float(ignored_value)
        else:
            raise ValueError("ignored_value must be a number or HTML snippet")
    
    pattern = re.compile(r'(\d{1,3}(?:\.\d{3})*(?:,\d{2}|\,-)?)')
    matches = pattern.findall(item)

    if not matches:
        return {"regular": None, "sale": None}

    matches = [convertPrice(price) for price in matches]

    if ignored_value is not None:
        filtered_prices = [price for price in matches if price != ignored_value]
    else:
        filtered_prices = matches

    if not filtered_prices:
        return {"regular": None, "sale": None}

    maxValue = max(filtered_prices)
    minValue = min(filtered_prices)

    if minValue == maxValue:
        minValue = None

    return {"regular": maxValue, "sale": minValue}
