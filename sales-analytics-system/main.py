from utils.file_handler import read_sales_data

# Test Task 1.1: Read Sales Data Function
print("\n" + "="*50)
print("TESTING: read_sales_data()")
print("="*50)

raw_lines = read_sales_data('data/sales_data.txt')

print(f"\nTotal lines read: {len(raw_lines)}")
if raw_lines:
    print(f"\nFirst 3 lines:")
    for i, line in enumerate(raw_lines[:3]):
        print(f"  {i+1}. {line}")
    
    print(f"\nLast line:")
    print(f"  {raw_lines[-1]}")
from utils.data_processor import parse_transactions


# Test Task 1.2: Parse and Clean Data
print("\n" + "="*50)
print("TESTING: parse_transactions()")
print("="*50)

parsed_data = parse_transactions(raw_lines)

print(f"\nTotal parsed: {len(parsed_data)}")
if parsed_data:
    print(f"\nFirst transaction:")
    print(parsed_data[0])
    
    print(f"\nExample of cleaned comma data:")
    # Find a transaction with comma in number
    for trans in parsed_data:
        if ',' in trans['ProductName'] or trans['UnitPrice'] > 1000:
            print(trans)
            break

from utils.data_processor import validate_and_filter

# Test Task 1.3: Validate and Filter
print("\n" + "="*50)
print("TESTING: validate_and_filter()")
print("="*50)

valid_trans, invalid_count, summary = validate_and_filter(parsed_data)

print(f"\nFilter Summary:")
for key, value in summary.items():
    print(f"  {key}: {value}")

from utils.data_processor import (
    calculate_total_revenue,
    region_wise_sales,
    top_selling_products,
    customer_analysis,
    daily_sales_trend
)

# Test Question 3: Data Processing Functions
print("\n" + "="*50)
print("QUESTION 3: DATA PROCESSING FUNCTIONS")
print("="*50)

# Test 1: Total Revenue
print("\n1. Calculate Total Revenue")
total_revenue = calculate_total_revenue(valid_trans)
print(f"   Total Revenue: ₹{total_revenue:,.2f}")

# Test 2: Region-wise Sales
print("\n2. Region-wise Sales Analysis")
regions = region_wise_sales(valid_trans)
for region, data in list(regions.items())[:3]:
    print(f"   {region}: ₹{data['total_sales']:,.2f} ({data['percentage']:.2f}%) - {data['transaction_count']} txns")

# Test 3: Top Selling Products
print("\n3. Top 5 Products")
top_products = top_selling_products(valid_trans, n=5)
for i, (product, qty, revenue) in enumerate(top_products, 1):
    print(f"   {i}. {product}: {qty} units, ₹{revenue:,.2f}")

# Test 4: Customer Analysis
print("\n4. Top 3 Customers")
customers = customer_analysis(valid_trans)
for i, (cust_id, data) in enumerate(list(customers.items())[:3], 1):
    print(f"   {i}. {cust_id}: Spent ₹{data['total_spent']:,.2f} ({data['purchase_count']} purchases)")

# Test 5: Daily Sales Trend
print("\n5. Daily Sales Trend (First 3 days)")
daily = daily_sales_trend(valid_trans)
for date, data in list(daily.items())[:3]:
    print(f"   {date}: ₹{data['revenue']:,.2f} ({data['transaction_count']} txns, {data['unique_customers']} customers)")

print("\n✓ All Question 3 functions tested!")

from utils.api_handler import fetch_all_products, create_product_mapping, enrich_sales_data, save_enriched_data

# Test Question 4: API Integration
print("\n" + "="*50)
print("QUESTION 4: API INTEGRATION")
print("="*50)

# Fetch products
api_products = fetch_all_products()

if api_products:
    # Create mapping
    product_mapping = create_product_mapping(api_products)
    
    # Enrich sales data
    enriched_trans = enrich_sales_data(valid_trans, product_mapping)
    
    # Save enriched data
    save_enriched_data(enriched_trans)
    
    # Show sample
    print(f"\nSample enriched transaction:")
    if enriched_trans:
        sample = enriched_trans[0]
        print(f"  TransactionID: {sample['TransactionID']}")
        print(f"  ProductName: {sample['ProductName']}")
        print(f"  API_Brand: {sample.get('API_Brand', 'N/A')}")
        print(f"  API_Match: {sample.get('API_Match', 'N/A')}")
else:
    print("✗ Failed to fetch products from API")

print("\n✓ Question 4 complete!")

#!/usr/bin/env python3
"""
Sales Analytics System - Main Application
Complete workflow for sales data processing, analysis, and reporting
"""

import sys
from pathlib import Path

# Add utils to path
sys.path.insert(0, str(Path(__file__).parent))

from utils.file_handler import read_sales_data
from utils.data_processor import (
    parse_transactions,
    validate_and_filter,
    calculate_total_revenue,
    region_wise_sales,
    top_selling_products,
    customer_analysis,
    daily_sales_trend,
    find_peak_sales_day,
    low_performing_products,
    generate_sales_report
)
from utils.api_handler import fetch_all_products, create_product_mapping, enrich_sales_data, save_enriched_data


def main():
    """
    Main execution function
    
    Workflow:
    1. Print welcome message
    2. Read sales data file (handle encoding)
    3. Parse and clean transactions
    4. Display filter options to user
    5. If yes, ask for filter criteria and apply
    6. Validate transactions
    7. Display validation summary
    8. Perform all data analyses
    9. Fetch products from API
    10. Enrich sales data with API info
    11. Save enriched data to file
    12. Generate comprehensive report
    13. Print success message with file locations
    """
    
    try:
        # Welcome message
        print("=" * 50)
        print("SALES ANALYTICS SYSTEM")
        print("=" * 50)
        print()
        
        # Step 1: Read sales data
        print("[1/10] Reading sales data...")
        raw_lines = read_sales_data('data/sales_data.txt')
        print(f"✓ Successfully read {len(raw_lines)} transactions")
        print()
        
        # Step 2: Parse and clean data
        print("[2/10] Parsing and cleaning data...")
        transactions = parse_transactions(raw_lines)
        print(f"✓ Parsed {len(transactions)} records")
        print()
        
        # Step 3: Display filter options
        print("[3/10] Filter Options Available:")
        
        # Get regions
        regions = sorted(set(t['Region'] for t in transactions))
        print(f"Regions: {', '.join(regions)}")
        
        # Get amount range
        amounts = [t['Quantity'] * t['UnitPrice'] for t in transactions]
        min_amount = min(amounts) if amounts else 0
        max_amount = max(amounts) if amounts else 0
        print(f"Amount Range: ₹{min_amount:,.0f} - ₹{max_amount:,.0f}")
        print()
        
        # Ask if user wants to filter
        filter_choice = input("Do you want to filter data? (y/n): ").strip().lower()
        
        # Step 4: Apply filters if needed
        if filter_choice == 'y':
            print()
            print("Filter Options:")
            print(f"1. By Region ({', '.join(regions)})")
            print("2. By Amount Range")
            print("3. Both")
            print()
            
            filtered_transactions = transactions.copy()
            
            filter_type = input("Choose filter type (1/2/3): ").strip()
            
            if filter_type in ['1', '3']:
                region_input = input(f"Enter region ({', '.join(regions)}): ").strip()
                if region_input in regions:
                    filtered_transactions = [t for t in filtered_transactions if t['Region'] == region_input]
            
            if filter_type in ['2', '3']:
                try:
                    min_val = float(input(f"Enter minimum amount (₹{min_amount:,.0f}): ").strip() or min_amount)
                    max_val = float(input(f"Enter maximum amount (₹{max_amount:,.0f}): ").strip() or max_amount)
                    filtered_transactions = [
                        t for t in filtered_transactions 
                        if min_val <= t['Quantity'] * t['UnitPrice'] <= max_val
                    ]
                except ValueError:
                    print("Invalid amount entered. Using all data.")
            
            transactions = filtered_transactions
            print(f"✓ Filtered to {len(transactions)} records")
        
        print()
        
        # Step 5: Validate transactions
        print("[4/10] Validating transactions...")
        valid_transactions, invalid_count, filter_summary = validate_and_filter(transactions)
        print(f"✓ Valid: {len(valid_transactions)} | Invalid: {invalid_count}")
        print()
        
        # Step 6: Perform data analyses
        print("[5/10] Analyzing sales data...")
        
        # Calculate total revenue
        total_revenue = calculate_total_revenue(valid_transactions)
        
        # Region-wise sales
        region_sales = region_wise_sales(valid_transactions)
        
        # Top products
        top_5_products = top_selling_products(valid_transactions, n=5)
        
        # Customer analysis
        customer_stats = customer_analysis(valid_transactions)
        
        # Daily trends
        daily_trend = daily_sales_trend(valid_transactions)
        peak_day = find_peak_sales_day(valid_transactions)
        
        # Low performing products
        low_performers = low_performing_products(valid_transactions, threshold=10)
        
        print(f"✓ Analysis complete")
        print()
        
        # Step 7: Fetch products from API
        print("[6/10] Fetching product data from API...")
        api_products = fetch_all_products()
        if api_products:
            print(f"✓ Fetched {len(api_products)} products")
        else:
            print("✗ Failed to fetch products from API")
            api_products = []
        print()
        
        # Step 8: Create product mapping and enrich data
        print("[7/10] Enriching sales data...")
        product_mapping = create_product_mapping(api_products)
        enriched_transactions = enrich_sales_data(valid_transactions, product_mapping)
        
        # Count enriched transactions
        enriched_count = sum(1 for t in enriched_transactions if t.get('API_Match', False))
        success_rate = (enriched_count / len(enriched_transactions) * 100) if enriched_transactions else 0
        print(f"✓ Enriched {enriched_count}/{len(enriched_transactions)} transactions ({success_rate:.1f}%)")
        print()
        
        # Step 9: Save enriched data
        print("[8/10] Saving enriched data...")
        save_enriched_data(enriched_transactions, 'data/enriched_sales_data.txt')
        print(f"✓ Saved to: data/enriched_sales_data.txt")
        print()
        
        # Step 10: Generate report
        print("[9/10] Generating report...")
        generate_sales_report(valid_transactions, enriched_transactions, 'output/sales_report.txt')
        print(f"✓ Report saved to: output/sales_report.txt")
        print()
        
        # Success message
        print("[10/10] Process Complete!")
        print("=" * 50)
        print("✓ All tasks completed successfully!")
        print()
        print("Generated Files:")
        print("  - data/enriched_sales_data.txt (Enriched transaction data)")
        print("  - output/sales_report.txt (Comprehensive sales report)")
        print("=" * 50)
        
    except FileNotFoundError as e:
        print(f"\n✗ Error: File not found - {str(e)}")
        print("Please ensure sales_data.txt exists in the data/ folder")
        
    except Exception as e:
        print(f"\n✗ Error: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
