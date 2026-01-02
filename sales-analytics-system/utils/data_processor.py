def parse_transactions(raw_lines):
    """
    Parses raw lines into clean list of dictionaries
    
    Returns: list of dictionaries with 8 keys:
    ['TransactionID', 'Date', 'ProductID', 'ProductName', 
     'Quantity', 'UnitPrice', 'CustomerID', 'Region']
    
    Expected Output Format:
    [
        {
            'TransactionID': 'T001',
            'Date': '2024-12-01',
            'ProductID': 'P101',
            'ProductName': 'Laptop',
            'Quantity': 2,
            'UnitPrice': 45000.0,
            'CustomerID': 'C001',
            'Region': 'North'
        },
        ...
    ]
    
    Requirements:
    - Split by pipe delimiter '|'
    - Handle commas within ProductName (remove or replace)
    - Remove commas from numeric fields and convert to proper types
    - Convert Quantity to int
    - Convert UnitPrice to float
    - Skip rows with incorrect number of fields
    """
    
    transactions = []
    skipped = 0
    
    for line in raw_lines:
        try:
            # Split by pipe delimiter
            fields = line.split('|')
            
            # Check if correct number of fields
            if len(fields) != 8:
                skipped += 1
                continue
            
            # Extract fields
            transaction_id = fields[0].strip()
            date = fields[1].strip()
            product_id = fields[2].strip()
            product_name = fields[3].strip()
            quantity_str = fields[4].strip()
            unit_price_str = fields[5].strip()
            customer_id = fields[6].strip()
            region = fields[7].strip()
            
            # Clean ProductName: remove commas
            product_name = product_name.replace(',', ' ').strip()
            
            # Clean numeric fields: remove commas
            quantity_str = quantity_str.replace(',', '')
            unit_price_str = unit_price_str.replace(',', '')
            
            # Convert to proper types
            quantity = int(quantity_str)
            unit_price = float(unit_price_str)
            
            # Create transaction dictionary
            transaction = {
                'TransactionID': transaction_id,
                'Date': date,
                'ProductID': product_id,
                'ProductName': product_name,
                'Quantity': quantity,
                'UnitPrice': unit_price,
                'CustomerID': customer_id,
                'Region': region
            }
            
            transactions.append(transaction)
        
        except (ValueError, IndexError):
            skipped += 1
            continue
    
    if skipped > 0:
        print(f"⚠ Skipped {skipped} rows due to parsing errors")
    
    print(f"✓ Parsed {len(transactions)} transactions successfully")
    return transactions

def validate_and_filter(transactions, region=None, min_amount=None, max_amount=None):
    """
    Validates transactions and applies optional filters
    
    Parameters:
    - transactions: list of transaction dictionaries
    - region: filter by specific region (optional)
    - min_amount: minimum transaction amount (Quantity * UnitPrice) (optional)
    - max_amount: maximum transaction amount (optional)
    
    Returns: tuple (valid_transactions, invalid_count, filter_summary)
    
    Expected Output Format:
    (
        [list of valid filtered transactions],
        5,  # count of invalid transactions
        {
            'total_input': 100,
            'invalid': 5,
            'filtered_by_region': 20,
            'filtered_by_amount': 10,
            'final_count': 65
        }
    )
    
    Validation Rules:
    - Quantity must be > 0
    - UnitPrice must be > 0
    - All required fields must be present
    - TransactionID must start with 'T'
    - ProductID must start with 'P'
    - CustomerID must start with 'C'
    """
    
    valid_transactions = []
    invalid_count = 0
    
    # Step 1: Validate records
    print("\n" + "="*50)
    print("VALIDATING TRANSACTIONS")
    print("="*50)
    
    for trans in transactions:
        is_valid = True
        
        # Check Quantity > 0
        if trans['Quantity'] <= 0:
            is_valid = False
        
        # Check UnitPrice > 0
        if trans['UnitPrice'] <= 0:
            is_valid = False
        
        # Check required fields
        if not trans.get('CustomerID') or not trans.get('Region'):
            is_valid = False
        
        # Check TransactionID starts with 'T'
        if not trans['TransactionID'].startswith('T'):
            is_valid = False
        
        # Check ProductID starts with 'P'
        if not trans['ProductID'].startswith('P'):
            is_valid = False
        
        # Check CustomerID starts with 'C'
        if not trans['CustomerID'].startswith('C'):
            is_valid = False
        
        if is_valid:
            valid_transactions.append(trans)
        else:
            invalid_count += 1
    
    print(f"✓ Total input: {len(transactions)}")
    print(f"✗ Invalid: {invalid_count}")
    print(f"✓ Valid: {len(valid_transactions)}")
    
    # Step 2: Display available filter options
    print("\n" + "="*50)
    print("FILTER OPTIONS")
    print("="*50)
    
    # Get unique regions
    regions = sorted(set(trans['Region'] for trans in valid_transactions))
    print(f"Available regions: {', '.join(regions)}")
    
    # Calculate amount range
    amounts = [trans['Quantity'] * trans['UnitPrice'] for trans in valid_transactions]
    min_trans_amount = min(amounts) if amounts else 0
    max_trans_amount = max(amounts) if amounts else 0
    print(f"Transaction amount range: ₹{min_trans_amount:,} - ₹{max_trans_amount:,}")
    
    # Step 3: Apply filters
    filtered_transactions = valid_transactions.copy()
    filtered_by_region = 0
    filtered_by_amount = 0
    
    if region:
        filtered_transactions = [t for t in filtered_transactions if t['Region'] == region]
        filtered_by_region = len(valid_transactions) - len(filtered_transactions)
    
    if min_amount or max_amount:
        initial_count = len(filtered_transactions)
        
        filtered_transactions = [
            t for t in filtered_transactions 
            if (min_amount is None or (t['Quantity'] * t['UnitPrice']) >= min_amount) and
               (max_amount is None or (t['Quantity'] * t['UnitPrice']) <= max_amount)
        ]
        
        filtered_by_amount = initial_count - len(filtered_transactions)
    
    # Step 4: Create summary
    filter_summary = {
        'total_input': len(transactions),
        'invalid': invalid_count,
        'valid': len(valid_transactions),
        'filtered_by_region': filtered_by_region,
        'filtered_by_amount': filtered_by_amount,
        'final_count': len(filtered_transactions)
    }
    
    print(f"\n✓ Final count after filtering: {filter_summary['final_count']}")
    
    return (filtered_transactions, invalid_count, filter_summary)

def calculate_total_revenue(transactions):
    """
    Calculates total revenue from all transactions
    
    Returns: float (total revenue)
    
    Expected Output: Single number representing sum of (Quantity * UnitPrice)
    Example: 1545000.50
    """
    total = 0
    for trans in transactions:
        total += trans['Quantity'] * trans['UnitPrice']
    
    return total

def region_wise_sales(transactions):
    """
    Analyzes sales by region
    
    Returns: dictionary with region statistics
    
    Expected Output Format:
    {
        'North': {
            'total_sales': 450000.0,
            'transaction_count': 15,
            'percentage': 29.13
        },
        'South': {...},
        ...
    }
    """
    region_data = {}
    total_revenue = calculate_total_revenue(transactions)
    
    # Group by region
    for trans in transactions:
        region = trans['Region']
        amount = trans['Quantity'] * trans['UnitPrice']
        
        if region not in region_data:
            region_data[region] = {
                'total_sales': 0,
                'transaction_count': 0
            }
        
        region_data[region]['total_sales'] += amount
        region_data[region]['transaction_count'] += 1
    
    # Calculate percentages and sort
    for region in region_data:
        percentage = (region_data[region]['total_sales'] / total_revenue * 100) if total_revenue > 0 else 0
        region_data[region]['percentage'] = round(percentage, 2)
    
    # Sort by total_sales descending
    sorted_regions = dict(sorted(region_data.items(), key=lambda x: x[1]['total_sales'], reverse=True))
    
    return sorted_regions

def top_selling_products(transactions, n=5):
    """
    Finds top n products by total quantity sold
    
    Returns: list of tuples
    [
        ('Laptop', 45, 2250000.0),  # (ProductName, TotalQuantity, TotalRevenue)
        ('Mouse', 38, 19000.0),
        ...
    ]
    """
    product_data = {}
    
    # Aggregate by product
    for trans in transactions:
        product = trans['ProductName']
        quantity = trans['Quantity']
        amount = quantity * trans['UnitPrice']
        
        if product not in product_data:
            product_data[product] = {
                'total_quantity': 0,
                'total_revenue': 0
            }
        
        product_data[product]['total_quantity'] += quantity
        product_data[product]['total_revenue'] += amount
    
    # Convert to list of tuples and sort
    products_list = [
        (name, data['total_quantity'], data['total_revenue'])
        for name, data in product_data.items()
    ]
    
    # Sort by quantity descending
    products_list.sort(key=lambda x: x[1], reverse=True)
    
    return products_list[:n]

def customer_analysis(transactions):
    """
    Analyzes customer purchase patterns
    
    Returns: dictionary of customer statistics
    
    Expected Output Format:
    {
        'C001': {
            'total_spent': 95000.0,
            'purchase_count': 3,
            'avg_order_value': 31666.67,
            'products_bought': ['Laptop', 'Mouse', 'Keyboard']
        },
        'C002': {...},
        ...
    }
    """
    customer_data = {}
    
    # Aggregate by customer
    for trans in transactions:
        customer = trans['CustomerID']
        amount = trans['Quantity'] * trans['UnitPrice']
        product = trans['ProductName']
        
        if customer not in customer_data:
            customer_data[customer] = {
                'total_spent': 0,
                'purchase_count': 0,
                'products': set()
            }
        
        customer_data[customer]['total_spent'] += amount
        customer_data[customer]['purchase_count'] += 1
        customer_data[customer]['products'].add(product)
    
    # Calculate averages and format
    for customer in customer_data:
        data = customer_data[customer]
        data['avg_order_value'] = round(data['total_spent'] / data['purchase_count'], 2)
        data['products_bought'] = sorted(list(data['products']))
        del data['products']  # Remove temporary set
    
    # Sort by total_spent descending
    sorted_customers = dict(sorted(customer_data.items(), key=lambda x: x[1]['total_spent'], reverse=True))
    
    return sorted_customers

def daily_sales_trend(transactions):
    """
    Analyzes sales trends by date
    
    Returns: dictionary sorted by date
    
    Expected Output Format:
    {
        '2024-12-01': {
            'revenue': 125000.0,
            'transaction_count': 8,
            'unique_customers': 6
        },
        '2024-12-02': {...},
        ...
    }
    """
    daily_data = {}
    
    # Group by date
    for trans in transactions:
        date = trans['Date']
        amount = trans['Quantity'] * trans['UnitPrice']
        customer = trans['CustomerID']
        
        if date not in daily_data:
            daily_data[date] = {
                'revenue': 0,
                'transaction_count': 0,
                'customers': set()
            }
        
        daily_data[date]['revenue'] += amount
        daily_data[date]['transaction_count'] += 1
        daily_data[date]['customers'].add(customer)
    
    # Convert set to count and format
    for date in daily_data:
        data = daily_data[date]
        data['unique_customers'] = len(data['customers'])
        del data['customers']  # Remove temporary set
    
    # Sort chronologically
    sorted_daily = dict(sorted(daily_data.items()))
    
    return sorted_daily

from datetime import datetime

def generate_sales_report(transactions, enriched_transactions, output_file='output/sales_report.txt'):
    """
    Generates a comprehensive formatted text report
    
    Parameters:
    - transactions: list of transaction dictionaries
    - enriched_transactions: list of enriched transaction dictionaries
    - output_file: path to save the report
    """
    
    try:
        # 1. HEADER
        report = []
        report.append("=" * 50)
        report.append("SALES ANALYTICS REPORT")
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"Records Processed: {len(transactions)}")
        report.append("=" * 50)
        report.append("")
        
        # 2. OVERALL SUMMARY
        total_revenue = sum(t['Quantity'] * t['UnitPrice'] for t in transactions)
        total_transactions = len(transactions)
        avg_order_value = total_revenue / total_transactions if total_transactions > 0 else 0
        
        # Get date range
        dates = [t['Date'] for t in transactions]
        min_date = min(dates) if dates else "N/A"
        max_date = max(dates) if dates else "N/A"
        
        report.append("OVERALL SUMMARY")
        report.append("-" * 50)
        report.append(f"Total Revenue: ₹{total_revenue:,.2f}")
        report.append(f"Total Transactions: {total_transactions}")
        report.append(f"Average Order Value: ₹{avg_order_value:,.2f}")
        report.append(f"Date Range: {min_date} to {max_date}")
        report.append("")
        
        # 3. REGION-WISE PERFORMANCE
        region_stats = {}
        for t in transactions:
            region = t['Region']
            if region not in region_stats:
                region_stats[region] = {'sales': 0, 'count': 0}
            region_stats[region]['sales'] += t['Quantity'] * t['UnitPrice']
            region_stats[region]['count'] += 1
        
        # Sort by sales descending
        sorted_regions = sorted(region_stats.items(), key=lambda x: x[1]['sales'], reverse=True)
        
        report.append("REGION-WISE PERFORMANCE")
        report.append("-" * 50)
        report.append(f"{'Region':<15} {'Sales':<20} {'% of Total':<15} {'Transactions':<15}")
        report.append("-" * 50)
        
        for region, stats in sorted_regions:
            percentage = (stats['sales'] / total_revenue * 100) if total_revenue > 0 else 0
            report.append(f"{region:<15} ₹{stats['sales']:>15,.2f}  {percentage:>8.2f}%  {stats['count']:>10}")
        
        report.append("")
        
        # 4. TOP 5 PRODUCTS
        product_stats = {}
        for t in transactions:
            product = t['ProductName']
            if product not in product_stats:
                product_stats[product] = {'qty': 0, 'revenue': 0}
            product_stats[product]['qty'] += t['Quantity']
            product_stats[product]['revenue'] += t['Quantity'] * t['UnitPrice']
        
        top_5_products = sorted(product_stats.items(), key=lambda x: x[1]['qty'], reverse=True)[:5]
        
        report.append("TOP 5 PRODUCTS")
        report.append("-" * 50)
        report.append(f"{'Rank':<6} {'Product Name':<25} {'Quantity':<12} {'Revenue':<15}")
        report.append("-" * 50)
        
        for idx, (product, stats) in enumerate(top_5_products, 1):
            report.append(f"{idx:<6} {product:<25} {stats['qty']:<12} ₹{stats['revenue']:>12,.2f}")
        
        report.append("")
        
        # 5. TOP 5 CUSTOMERS
        customer_stats = {}
        for t in transactions:
            cust_id = t['CustomerID']
            if cust_id not in customer_stats:
                customer_stats[cust_id] = {'spent': 0, 'count': 0}
            customer_stats[cust_id]['spent'] += t['Quantity'] * t['UnitPrice']
            customer_stats[cust_id]['count'] += 1
        
        top_5_customers = sorted(customer_stats.items(), key=lambda x: x[1]['spent'], reverse=True)[:5]
        
        report.append("TOP 5 CUSTOMERS")
        report.append("-" * 50)
        report.append(f"{'Rank':<6} {'Customer ID':<15} {'Total Spent':<20} {'Orders':<10}")
        report.append("-" * 50)
        
        for idx, (cust_id, stats) in enumerate(top_5_customers, 1):
            report.append(f"{idx:<6} {cust_id:<15} ₹{stats['spent']:>15,.2f}  {stats['count']:>8}")
        
        report.append("")
        
        # 6. DAILY SALES TREND
        daily_stats = {}
        for t in transactions:
            date = t['Date']
            if date not in daily_stats:
                daily_stats[date] = {'revenue': 0, 'count': 0, 'customers': set()}
            daily_stats[date]['revenue'] += t['Quantity'] * t['UnitPrice']
            daily_stats[date]['count'] += 1
            daily_stats[date]['customers'].add(t['CustomerID'])
        
        sorted_dates = sorted(daily_stats.items())
        
        report.append("DAILY SALES TREND")
        report.append("-" * 50)
        report.append(f"{'Date':<15} {'Revenue':<20} {'Transactions':<15} {'Unique Customers':<15}")
        report.append("-" * 50)
        
        for date, stats in sorted_dates:
            report.append(f"{date:<15} ₹{stats['revenue']:>15,.2f}  {stats['count']:>12}  {len(stats['customers']):>15}")
        
        report.append("")
        
        # 7. PRODUCT PERFORMANCE ANALYSIS
        report.append("PRODUCT PERFORMANCE ANALYSIS")
        report.append("-" * 50)
        
        # Best selling day
        best_day = max(daily_stats.items(), key=lambda x: x[1]['revenue'])
        report.append(f"Best Selling Day: {best_day[0]} (₹{best_day[1]['revenue']:,.2f})")
        
        # Low performing products (threshold = 10)
        low_performers = {p: stats for p, stats in product_stats.items() if stats['qty'] < 10}
        if low_performers:
            report.append("\nLow Performing Products (< 10 units sold):")
            for product, stats in sorted(low_performers.items(), key=lambda x: x[1]['qty']):
                report.append(f"  - {product}: {stats['qty']} units (₹{stats['revenue']:,.2f})")
        else:
            report.append("Low Performing Products: None")
        
        # Average transaction value per region
        report.append("\nAverage Transaction Value per Region:")
        for region, stats in sorted_regions:
            avg = stats['sales'] / stats['count'] if stats['count'] > 0 else 0
            report.append(f"  - {region}: ₹{avg:,.2f}")
        
        report.append("")
        
        # 8. API ENRICHMENT SUMMARY
        enriched_count = sum(1 for t in enriched_transactions if t.get('API_Match', False))
        total_enriched = len(enriched_transactions)
        success_rate = (enriched_count / total_enriched * 100) if total_enriched > 0 else 0
        
        report.append("API ENRICHMENT SUMMARY")
        report.append("-" * 50)
        report.append(f"Total Products Enriched: {enriched_count}/{total_enriched}")
        report.append(f"Success Rate: {success_rate:.2f}%")
        
        # Products that couldn't be enriched
        failed_products = set()
        for t in enriched_transactions:
            if not t.get('API_Match', False):
                failed_products.add(t.get('ProductID', 'Unknown'))
        
        if failed_products:
            report.append(f"Products Not Enriched: {', '.join(sorted(failed_products))}")
        else:
            report.append("Products Not Enriched: None")
        
        report.append("")
        report.append("=" * 50)
        report.append("END OF REPORT")
        report.append("=" * 50)
        
        # Write to file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(report))
        
        print(f"✓ Report saved to: {output_file}")
        return True
        
    except Exception as e:
        print(f"Error generating report: {str(e)}")
        return False

def daily_sales_trend(transactions):
    """
    Analyzes sales trends by date
    
    Returns: dictionary sorted by date
    """
    daily_stats = {}
    for t in transactions:
        date = t['Date']
        if date not in daily_stats:
            daily_stats[date] = {'revenue': 0, 'count': 0, 'customers': set()}
        daily_stats[date]['revenue'] += t['Quantity'] * t['UnitPrice']
        daily_stats[date]['count'] += 1
        daily_stats[date]['customers'].add(t['CustomerID'])
    
    # Convert sets to lists for JSON serialization
    result = {}
    for date in sorted(daily_stats.keys()):
        result[date] = {
            'revenue': daily_stats[date]['revenue'],
            'transaction_count': daily_stats[date]['count'],
            'unique_customers': len(daily_stats[date]['customers'])
        }
    
    return result


def find_peak_sales_day(transactions):
    """
    Identifies the date with highest revenue
    
    Returns: tuple (date, revenue, transaction_count)
    """
    if not transactions:
        return None, 0, 0
    
    daily_stats = {}
    for t in transactions:
        date = t['Date']
        if date not in daily_stats:
            daily_stats[date] = {'revenue': 0, 'count': 0}
        daily_stats[date]['revenue'] += t['Quantity'] * t['UnitPrice']
        daily_stats[date]['count'] += 1
    
    # Find peak day
    peak_date = max(daily_stats.items(), key=lambda x: x[1]['revenue'])
    return (peak_date[0], peak_date[1]['revenue'], peak_date[1]['count'])


def low_performing_products(transactions, threshold=10):
    """
    Identifies products with low sales
    
    Returns: list of tuples (ProductName, TotalQuantity, TotalRevenue)
    """
    product_stats = {}
    for t in transactions:
        product = t['ProductName']
        if product not in product_stats:
            product_stats[product] = {'qty': 0, 'revenue': 0}
        product_stats[product]['qty'] += t['Quantity']
        product_stats[product]['revenue'] += t['Quantity'] * t['UnitPrice']
    
    # Find low performers
    low_performers = [
        (name, stats['qty'], stats['revenue'])
        for name, stats in product_stats.items()
        if stats['qty'] < threshold
    ]
    
    # Sort by quantity ascending
    return sorted(low_performers, key=lambda x: x[1])
