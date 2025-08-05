import pandas as pd
import sqlite3
import numpy as np
from tkinter import messagebox
import os
from pathlib import Path
import logging

def convert_csv_to_sqlite(csv_file, db_file, db_path, table_name):
    """
    Convert CSV data to SQLite database
    
    Args:
        csv_file (str): Path to the CSV file
        db_file (str): Name of the SQLite database file (with .db extension)
        db_path (str): Directory path where the database should be created
        table_name (str): Name of the table to create in the database
    
    Returns:
        bool: True if successful, False otherwise
    """
    conn = None
    cursor = None
    
    try:
        # Validate inputs
        if not csv_file or not db_file or not db_path or not table_name:
            raise ValueError("All parameters (csv_file, db_file, db_path, table_name) must be provided")
        
        # Check if CSV file exists and is readable
        if not os.path.exists(csv_file):
            raise FileNotFoundError(f"CSV file not found: {csv_file}")
        
        if not os.access(csv_file, os.R_OK):
            raise PermissionError(f"Cannot read CSV file: {csv_file}")
        
        # Validate table name (basic SQL injection prevention)
        if not table_name.replace('_', '').replace('-', '').isalnum():
            raise ValueError("Table name can only contain letters, numbers, underscores, and hyphens")
        
        # Validate and create database directory
        try:
            os.makedirs(db_path, exist_ok=True)
        except PermissionError:
            raise PermissionError(f"Cannot create directory: {db_path}")
        
        # Construct full database path
        full_db_path = os.path.join(db_path, db_file)
        
        # Ensure db_file has .db extension
        if not db_file.lower().endswith('.db'):
            full_db_path += '.db'
        
        # Read CSV with error handling
        try:
            df = pd.read_csv(csv_file)
        except pd.errors.EmptyDataError:
            raise ValueError("CSV file is empty")
        except pd.errors.ParserError as e:
            raise ValueError(f"Error parsing CSV file: {e}")
        except UnicodeDecodeError:
            # Try different encodings
            encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
            df = None
            for encoding in encodings:
                try:
                    df = pd.read_csv(csv_file, encoding=encoding)
                    break
                except UnicodeDecodeError:
                    continue
            if df is None:
                raise ValueError("Unable to decode CSV file with common encodings")
        
        # Check if DataFrame is empty
        if df.empty:
            raise ValueError("CSV file contains no data")
        
        # Clean column names (remove special characters that might cause SQL issues)
        df.columns = df.columns.str.replace('[^a-zA-Z0-9_]', '_', regex=True)
        df.columns = df.columns.str.strip()
        
        # Handle duplicate column names
        if df.columns.duplicated().any():
            df.columns = pd.io.common.dedup_names(df.columns, is_potential_multiindex=False)
        
        # Connect to SQLite database
        try:
            conn = sqlite3.connect(full_db_path)
            cursor = conn.cursor()
        except sqlite3.Error as e:
            raise sqlite3.Error(f"Cannot connect to database: {e}")
        
        # Enhanced data type mapping
        dtype_map = {
            'int8': 'INTEGER',
            'int16': 'INTEGER', 
            'int32': 'INTEGER',
            'int64': 'INTEGER',
            'uint8': 'INTEGER',
            'uint16': 'INTEGER',
            'uint32': 'INTEGER', 
            'uint64': 'INTEGER',
            'float16': 'REAL',
            'float32': 'REAL',
            'float64': 'REAL',
            'object': 'TEXT',
            'string': 'TEXT',
            'bool': 'INTEGER',
            'datetime64[ns]': 'TEXT',
            'timedelta64[ns]': 'TEXT',
            'category': 'TEXT'
        }
        
        # Create table schema with proper types
        columns = []
        for col, dtype in df.dtypes.items():
            # Clean column name for SQL
            safe_col = str(col).replace('"', '""')  # Escape quotes
            sqlite_type = dtype_map.get(str(dtype), 'TEXT')
            columns.append(f'"{safe_col}" {sqlite_type}')
        
        # Create table
        create_sql = f'CREATE TABLE IF NOT EXISTS "{table_name}" ({", ".join(columns)})'
        
        try:
            # Drop existing table if it exists
            cursor.execute(f'DROP TABLE IF EXISTS "{table_name}"')
            cursor.execute(create_sql)
            conn.commit()
        except sqlite3.Error as e:
            raise sqlite3.Error(f"Error creating table: {e}")
        
        # Insert data using pandas to_sql for better handling
        try:
            df.to_sql(table_name, conn, if_exists='replace', index=False, method='multi')
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error inserting data: {e}")
        
        # Verify data was inserted
        cursor.execute(f'SELECT COUNT(*) FROM "{table_name}"')
        row_count = cursor.fetchone()[0]
        
        if row_count != len(df):
            raise Exception(f"Data verification failed: Expected {len(df)} rows, found {row_count}")
        
        success_msg = (f"Success! Data has been successfully converted and saved.\n\n"
                      f"Database: {full_db_path}\n"
                      f"Table: {table_name}\n" 
                      f"Rows: {row_count}\n"
                      f"Columns: {len(df.columns)}")
        
        messagebox.showinfo("Conversion Successful", success_msg)
        return True
        
    except FileNotFoundError as e:
        error_msg = f"File Error: {str(e)}"
        messagebox.showerror("File Not Found", error_msg)
        logging.error(error_msg)
        return False
        
    except PermissionError as e:
        error_msg = f"Permission Error: {str(e)}"
        messagebox.showerror("Permission Denied", error_msg)
        logging.error(error_msg)
        return False
        
    except ValueError as e:
        error_msg = f"Data Error: {str(e)}"
        messagebox.showerror("Invalid Data", error_msg)
        logging.error(error_msg)
        return False
        
    except sqlite3.Error as e:
        error_msg = f"Database Error: {str(e)}"
        messagebox.showerror("Database Error", error_msg)
        logging.error(error_msg)
        return False
        
    except Exception as e:
        error_msg = f"Unexpected Error: {str(e)}"
        messagebox.showerror("Error", error_msg)
        logging.error(error_msg)
        return False
        
    finally:
        # Ensure database connection is properly closed
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# Example usage with validation
def safe_convert_csv_to_sqlite(csv_file, db_file, db_path, table_name):
    """
    Wrapper function with additional validation before conversion.
    """
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # Basic parameter validation
    if not all([csv_file, db_file, db_path, table_name]):
        messagebox.showerror("Invalid Input", "All parameters must be provided")
        return False
    
    # Check file extension
    if not csv_file.lower().endswith('.csv'):
        messagebox.showwarning("File Type Warning", "File does not have .csv extension")
    # Call the main conversion function
    return convert_csv_to_sqlite(csv_file, db_file, db_path, table_name)