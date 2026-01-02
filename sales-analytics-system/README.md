# Sales Analytics System

A comprehensive Python-based sales data analysis system that processes transaction data, validates records, enriches them with API information, and generates detailed analytics reports.

## Installation

Prerequisites:
- Python 3.7 or higher
- pip (Python package manager)

Setup Steps:

1. Install dependencies
   pip install -r requirements.txt

2. Verify data file exists
   Ensure data/sales_data.txt exists with sales transaction data

## Usage

Running the Application:

python main.py

What the system does:

1. Reads sales data from data/sales_data.txt
2. Parses and cleans the transaction records
3. Allows filtering by region and amount
4. Validates all transactions
5. Performs comprehensive data analysis
6. Fetches product data from DummyJSON API
7. Enriches transaction data with API information
8. Saves enriched data to data/enriched_sales_data.txt
9. Generates comprehensive report in output/sales_report.txt

## Project Structure

sales-analytics-system/
├── main.py                          (Main entry point)
├── README.md                        (This file)
├── requirements.txt                 (Dependencies)
├── data/
│   ├── sales_data.txt              (Input data)
│   └── enriched_sales_data.txt      (Generated output)
├── output/
│   └── sales_report.txt            (Generated report)
└── utils/
    ├── file_handler.py             (File I/O)
    ├── data_processor.py           (Data processing)
    └── api_handler.py              (API integration)

## Features

- Data Handling: Read files with multiple encoding support
- Data Cleaning: Parse and validate transaction records
- Data Filtering: Filter by region and transaction amount
- Data Analysis: Calculate revenue, regional performance, top products, customer analysis
- API Integration: Enrich data with product information from DummyJSON
- Report Generation: Create 8-section comprehensive reports

## Output Files

The system generates two output files:

1. data/enriched_sales_data.txt
   Contains original transactions with added API fields like category, brand, rating

2. output/sales_report.txt
   Comprehensive formatted report with 8 sections:
   - Header (title, timestamp, record count)
   - Overall Summary (revenue, transactions, averages)
   - Regional Performance (sales by region with percentages)
   - Top 5 Products (best sellers)
   - Top 5 Customers (highest spenders)
   - Daily Sales Trend (revenue by date)
   - Product Performance Analysis (best day, low performers)
   - API Enrichment Summary (success rate)

## Technologies Used

- Python 3
- requests (for API calls)
- Standard libraries (pathlib, datetime, etc.)

## Data Validation

Invalid records are removed for:
- Quantity <= 0
- Unit Price <= 0
- Missing required fields
- Transaction ID not starting with T
- Product ID not starting with P
- Customer ID not starting with C

## Status

Complete - Ready for submission

Version: 1.0
Last Updated: January 13, 2026
