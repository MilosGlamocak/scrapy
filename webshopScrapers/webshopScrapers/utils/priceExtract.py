import re
from bs4 import BeautifulSoup

# Define the regex pattern globally
PRICE_PATTERN = re.compile(r'(\d{1,3}(?:[\s\.]\d{3})*(?:,\d{2}|\,-)?)')

def extractPriceFromHtml(html_snippet):
    if not html_snippet:
        return None

    soup = BeautifulSoup(html_snippet, 'html.parser')
    text = soup.get_text(separator=' ', strip=True)
    matches = PRICE_PATTERN.findall(text)
    
    # Process each matched price string
    prices = [convertPrice(match) for match in matches]
    return prices[0] if prices else None

def convertPrice(price_str):
    # Remove spaces and replace thousand separators with nothing
    price_str = price_str.replace(' ', '').replace(',-', ',00')
    return float(price_str.replace('.', '').replace(',', '.'))

def extractPrices(item, ignored_value=None):
    if ignored_value is not None:
        if isinstance(ignored_value, str):
            ignored_value = extractPriceFromHtml(ignored_value)
            if isinstance(ignored_value, list):
                ignored_value = ignored_value[0]
        elif isinstance(ignored_value, (int, float)):
            ignored_value = float(ignored_value)
        else:
            raise ValueError("ignored_value must be a number or HTML snippet")
    
    matches = PRICE_PATTERN.findall(item)

    if not matches:
        return {"regular": None, "sale": None}

    # Convert and filter prices
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
