def read_sales_data(filename):
    """
    Reads sales data from file handling encoding issues
    
    Returns: list of raw lines (strings)
    
    Expected Output Format:
    ['T001|2024-12-01|P101|Laptop|2|45000|C001|North', ...]
    
    Requirements:
    - Use 'with' statement
    - Handle different encodings (try 'utf-8', 'latin-1', 'cp1252')
    - Handle FileNotFoundError with appropriate error message
    - Skip the header row
    - Remove empty lines
    """
    
    try:
        # Try different encodings
        encodings = ['utf-8', 'latin-1', 'cp1252']
        
        for encoding in encodings:
            try:
                with open(filename, 'r', encoding=encoding) as file:
                    lines = file.readlines()
                
                # Remove empty lines and strip whitespace
                lines = [line.strip() for line in lines if line.strip()]
                
                # Skip header row (first line)
                if len(lines) > 0:
                    lines = lines[1:]
                
                print(f"✓ Successfully read {len(lines)} transactions from {filename}")
                return lines
                
            except UnicodeDecodeError:
                continue
        
        print("Could not read file with any encoding")
        return []
    
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found!")
        return []
