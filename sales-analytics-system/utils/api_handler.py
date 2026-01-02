import requests

def fetch_all_products():
    """
    Fetches all products from DummyJSON API
    
    Returns: list of product dictionaries
    
    Expected Output:
    [
        {
            'id': 1,
            'title': 'iPhone 9',
            'category': 'smartphones',
            'brand': 'Apple',
            'price': 549,
            'rating': 4.69
        },
        ...
    ]
    """
    try:
        print("\n" + "="*50)
        print("FETCHING PRODUCTS FROM API")
        print("="*50)
        
        url = 'https://dummyjson.com/products?limit=100'
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        products = data.get('products', [])
        
        # Extract only needed fields
        simplified_products = [
            {
                'id': p['id'],
                'title': p['title'],
                'category': p.get('category', 'unknown'),
                'brand': p.get('brand', 'unknown'),
                'price': p.get('price', 0),
                'rating': p.get('rating', 0)
            }
            for p in products
        ]
        
        print(f"✓ Successfully fetched {len(simplified_products)} products")
        return simplified_products
    
    except requests.exceptions.RequestException as e:
        print(f"✗ Error fetching products: {str(e)}")
        return []
    except Exception as e:
        print(f"✗ Unexpected error: {str(e)}")
        return []


def create_product_mapping(api_products):
    """
    Creates a mapping of product IDs to product info
    
    Parameters: api_products from fetch_all_products()
    
    Returns: dictionary mapping product IDs to info
    
    Expected Output:
    {
        1: {'title': 'iPhone 9', 'category': 'smartphones', 
            'brand': 'Apple', 'rating': 4.69},
        2: {'title': 'iPhone X', 'category': 'smartphones', 
            'brand': 'Apple', 'rating': 4.44},
        ...
    }
    """
    product_mapping = {}
    
    for product in api_products:
        product_id = product['id']
        product_mapping[product_id] = {
            'title': product['title'],
            'category': product['category'],
            'brand': product['brand'],
            'rating': product['rating']
        }
    
    print(f"✓ Created mapping for {len(product_mapping)} products")
    return product_mapping


def enrich_sales_data(transactions, product_mapping):
    """
    Enriches transaction data with API product information
    
    Parameters:
    - transactions: list of transaction dictionaries
    - product_mapping: dictionary from create_product_mapping()
    
    Returns: list of enriched transaction dictionaries
    
    Expected Output (each transaction):
    {
        'TransactionID': 'T001',
        'Date': '2024-12-01',
        'ProductID': 'P101',
        'ProductName': 'Laptop',
        'Quantity': 2,
        'UnitPrice': 45000.0,
        'CustomerID': 'C001',
        'Region': 'North',
        # NEW FIELDS FROM API:
        'API_Category': 'laptops',
        'API_Brand': 'Apple',
        'API_Rating': 4.7,
        'API_Match': True
    }
    """
    enriched_transactions = []
    matched = 0
    unmatched = 0
    
    print("\n" + "="*50)
    print("ENRICHING SALES DATA WITH API INFO")
    print("="*50)
    
    for trans in transactions:
        enriched = trans.copy()
        
        try:
            # Extract numeric ID from ProductID (P101 → 101, P5 → 5)
            product_id_str = trans['ProductID'][1:]  # Remove 'P' prefix
            product_id = int(product_id_str)
            
            # Check if product exists in API mapping
            if product_id in product_mapping:
                api_info = product_mapping[product_id]
                enriched['API_Category'] = api_info['category']
                enriched['API_Brand'] = api_info['brand']
                enriched['API_Rating'] = api_info['rating']
                enriched['API_Match'] = True
                matched += 1
            else:
                # Product not found in API
                enriched['API_Category'] = None
                enriched['API_Brand'] = None
                enriched['API_Rating'] = None
                enriched['API_Match'] = False
                unmatched += 1
        
        except (ValueError, IndexError, KeyError):
            # Error extracting ID or processing
            enriched['API_Category'] = None
            enriched['API_Brand'] = None
            enriched['API_Rating'] = None
            enriched['API_Match'] = False
            unmatched += 1
        
        enriched_transactions.append(enriched)
    
    print(f"✓ Enriched {matched} transactions with API data")
    print(f"⚠ {unmatched} transactions without API match")
    
    return enriched_transactions


def save_enriched_data(enriched_transactions, filename='data/enriched_sales_data.txt'):
    """
    Saves enriched transactions back to file
    
    Expected File Format:
    TransactionID|Date|ProductID|ProductName|Quantity|UnitPrice|CustomerID|Region|API_Category|API_Brand|API_Rating|API_Match
    T001|2024-12-01|P101|Laptop|2|45000.0|C001|North|laptops|Apple|4.7|True
    """
    try:
        print("\n" + "="*50)
        print("SAVING ENRICHED DATA")
        print("="*50)
        
        with open(filename, 'w', encoding='utf-8') as f:
            # Write header
            header = 'TransactionID|Date|ProductID|ProductName|Quantity|UnitPrice|CustomerID|Region|API_Category|API_Brand|API_Rating|API_Match\n'
            f.write(header)
            
            # Write data rows
            for trans in enriched_transactions:
                row = f"{trans['TransactionID']}|{trans['Date']}|{trans['ProductID']}|{trans['ProductName']}|{trans['Quantity']}|{trans['UnitPrice']}|{trans['CustomerID']}|{trans['Region']}|{trans.get('API_Category', '')}|{trans.get('API_Brand', '')}|{trans.get('API_Rating', '')}|{trans.get('API_Match', '')}\n"
                f.write(row)
        
        print(f"✓ Saved {len(enriched_transactions)} enriched transactions to {filename}")
        return True
    
    except Exception as e:
        print(f"✗ Error saving enriched data: {str(e)}")
        return False

