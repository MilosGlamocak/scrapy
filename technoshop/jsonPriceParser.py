from bs4 import BeautifulSoup
import re

def parse_price(price_html):
    soup = BeautifulSoup(price_html, 'html.parser')
    
    # Try to find the discounted price (new lower price)
    discounted_price_tag = soup.find('div', class_='cprice')
    discounted_price = discounted_price_tag.get_text(strip=True) if discounted_price_tag else None
    
    # Try to find the regular price (old higher price)
    regular_price_tag = soup.find('div', class_='cprice cprice--old')
    regular_price = regular_price_tag.get_text(strip=True) if regular_price_tag else None
    
    # If there is no regular price, use the discounted price as regular
    if not regular_price:
        regular_price = discounted_price
        discounted_price = None

    # Convert prices to float and round to 2 decimal places (removing 'KM' and ',')
    def convert_to_float(price_str):
        if price_str:
            # Remove non-numeric characters except for the decimal point
            price_str = re.sub(r'[^\d.,]', '', price_str)  
            # Replace comma with dot if it's used as a decimal separator
            price_str = price_str.replace(',', '.')  
            try:
                # Convert to float and round to 2 decimal places
                return round(float(price_str), 2)
            except ValueError:
                return None
        return None
    
    return {
        'regular_price': convert_to_float(regular_price),
        'discounted_price': convert_to_float(discounted_price)
    }
