import tkinter as tk
from tkinter import filedialog, messagebox
from converter import convert_csv_to_sqlite
import os
import globals

class SetupPathsWindow:
    """Window for setting up file paths and configurations"""
    
    def __init__(self, parent):
        self.parent = parent
        
        # Initialize theme
        self.current_theme = {
            'bg': 'white',
            'text': 'black'
        }
        
        # Create window
        self.window = tk.Toplevel(parent)
        self.window.title("Conversion of the CSV file to SQL database")
        self.window.geometry("1300x700")
        self.window.configure(bg='white')
        self.window.resizable(width=False, height=False)
        
        self.window.transient(parent)
        self.window.grab_set()
        self.window.focus_set()
        
        # Initialize variables
        self.csv_selected = False
        self.path_selected = False
        self.db_name_set = False
        self.table_name_set = False
        
        try:
            self.setup_ui()
        except Exception as e:
            messagebox.showerror("UI Setup Error", f"Failed to create interface: {str(e)}")
            self.window.destroy()
    
    def setup_ui(self):
        """Setup the user interface"""
        # Title
        title_label = tk.Label(
            self.window, 
            text="Configure Data File, save location and database name",
            font=("Arial", 16, "bold"), 
            bg='white', 
            fg='black'
        )
        title_label.pack(pady=20)
        
        self.create_CSV_section()
        self.create_dbname_section()
        self.create_save_path_section()
        self.create_control_buttons()

    def create_CSV_section(self):
        '''Create CSV file selection section'''
        csv_frame = tk.Frame(self.window, bg=self.current_theme['bg'])
        csv_frame.pack(pady=20, padx=20, fill='x')
        
        file_section_label = tk.Label(
            csv_frame, 
            text="1. Select CSV File",
            font=("Arial", 12, "bold"), 
            bg=self.current_theme['bg'], 
            fg=self.current_theme['text']
        )
        file_section_label.pack(anchor='w', pady=(0, 10))
        
        file_button = tk.Button(
            csv_frame, 
            text="Browse for Data File",
            command=self.select_file,
            font=("Arial", 12), 
            width=20, 
            height=2, 
            bg='lightblue',
            cursor='hand2'
        )
        file_button.pack(pady=5)
        
        self.file_status_label = tk.Label(
            csv_frame, 
            text="No file selected",
            font=("Arial", 10), 
            bg='white', 
            fg='red'
        )
        self.file_status_label.pack(pady=5)
    
    def create_dbname_section(self):
        """Create database name and table name input section"""
        dbname_frame = tk.Frame(self.window, bg='white')
        dbname_frame.pack(pady=20, padx=20, fill='x')
        
        # Database name section
        db_section = tk.Frame(dbname_frame, bg='white')
        db_section.pack(fill='x', pady=(0, 10))
        
        dbname_label = tk.Label(
            db_section, 
            text="2. Database name:",
            font=("Arial", 12, "bold"), 
            bg='white', 
            fg='black'
        )
        dbname_label.pack(side='left', padx=(0, 10))
        
        self.dbname_entry = tk.Entry(db_section, font=("Arial", 12), width=30)
        self.dbname_entry.pack(side='left', padx=(0, 10))
        self.dbname_entry.bind("<KeyRelease>", self.validate_db_name)
        self.dbname_entry.bind("<Return>", self.set_db_name)
        
        # Database name status
        self.db_status_label = tk.Label(
            db_section,
            text="Enter database name",
            font=("Arial", 10),
            bg='white',
            fg='orange'
        )
        self.db_status_label.pack(side='left', padx=(10, 0))
        
        # Table name section
        table_section = tk.Frame(dbname_frame, bg='white')
        table_section.pack(fill='x')
        
        tablename_label = tk.Label(
            table_section,
            text='3. Table name:',
            font=("Arial", 12, "bold"),
            bg='white',
            fg='black'
        )
        tablename_label.pack(side='left', padx=(0, 10))
        
        self.tablename_entry = tk.Entry(table_section, font=("Arial", 12), width=30)
        self.tablename_entry.pack(side='left', padx=(0, 10))
        self.tablename_entry.bind("<KeyRelease>", self.validate_table_name)
        self.tablename_entry.bind("<Return>", self.set_table_name)
        
        # Table name status
        self.table_status_label = tk.Label(
            table_section,
            text="Enter table name",
            font=("Arial", 10),
            bg='white',
            fg='orange'
        )
        self.table_status_label.pack(side='left', padx=(10, 0))
    
    def validate_db_name(self, event=None):
        """Validate database name input"""
        db_name = self.dbname_entry.get().strip()
        if not db_name:
            self.db_status_label.config(text="Database name required", fg='red')
            self.db_name_set = False
        elif not self.is_valid_filename(db_name):
            self.db_status_label.config(text="Invalid characters in name", fg='red')
            self.db_name_set = False
        else:
            self.db_status_label.config(text="✓ Valid database name", fg='green')
            self.db_name_set = True
            globals.DB_NAME = db_name
    
    def validate_table_name(self, event=None):
        """Validate table name input"""
        table_name = self.tablename_entry.get().strip()
        if not table_name:
            self.table_status_label.config(text="Table name required", fg='red')
            self.table_name_set = False
        elif not self.is_valid_sql_name(table_name):
            self.table_status_label.config(text="Invalid SQL table name", fg='red')
            self.table_name_set = False
        else:
            self.table_status_label.config(text="✓ Valid table name", fg='green')
            self.table_name_set = True
            globals.TABLE_NAME = table_name
    
    def is_valid_filename(self, filename):
        """Check if filename is valid for the operating system"""
        invalid_chars = '<>:"/\\|?*'
        if any(char in filename for char in invalid_chars):
            return False
        if filename.lower() in ['con', 'prn', 'aux', 'nul'] or filename.lower().startswith('com') or filename.lower().startswith('lpt'):
            return False
        return True
    
    def is_valid_sql_name(self, name):
        """Check if name is valid for SQL table/column"""
        if not name:
            return False
        # Must start with letter or underscore
        if not (name[0].isalpha() or name[0] == '_'):
            return False
        # Can only contain letters, numbers, and underscores
        return all(c.isalnum() or c == '_' for c in name)
    
    def set_db_name(self, event=None):
        """Set database name"""
        self.validate_db_name()
    
    def set_table_name(self, event=None):
        """Set table name"""
        self.validate_table_name()
    
    def create_save_path_section(self):
        """Create save path selection section"""
        path_frame = tk.Frame(self.window, bg='white')
        path_frame.pack(pady=20, padx=20, fill='x')
        
        path_section_label = tk.Label(
            path_frame, 
            text="4. Select Save Location",
            font=("Arial", 12, "bold"), 
            bg='white', 
            fg='black'
        )
        path_section_label.pack(anchor='w', pady=(0, 10))
        
        path_button = tk.Button(
            path_frame, 
            text="Browse for Save Location",
            command=self.select_save_path,
            font=("Arial", 12), 
            width=20, 
            height=2, 
            bg='lightblue',
            cursor='hand2'
        )
        path_button.pack(pady=5)
        
        self.path_status_label = tk.Label(
            path_frame, 
            text="No save path selected",
            font=("Arial", 10), 
            bg='white', 
            fg='red'
        )
        self.path_status_label.pack(pady=5)

    def create_control_buttons(self):
        """Create control buttons"""
        button_frame = tk.Frame(self.window, bg=self.current_theme['bg'])
        button_frame.pack(pady=30)
        
        # Convert button
        self.convert_button = tk.Button(
            button_frame, 
            text="Convert CSV to SQLite",
            command=self.perform_conversion,
            font=("Arial", 12, "bold"), 
            width=20, 
            height=2, 
            bg='lightgreen',
            cursor='hand2',
            state='disabled'  # Initially disabled
        )
        self.convert_button.pack(side='left', padx=10)
        
        # Done button (close window)
        done_button = tk.Button(
            button_frame, 
            text="Close",
            command=self.close_setup,
            font=("Arial", 12), 
            width=15, 
            height=2, 
            bg='lightgray',
            cursor='hand2'
        )
        done_button.pack(side='left', padx=10)
        
        # Cancel button
        cancel_button = tk.Button(
            button_frame, 
            text="Cancel",
            command=self.cancel_operation,
            font=("Arial", 12), 
            width=15, 
            height=2, 
            bg='lightcoral',
            cursor='hand2'
        )
        cancel_button.pack(side='left', padx=10)
    
    def check_conversion_ready(self):
        """Check if all requirements are met for conversion"""
        ready = (self.csv_selected and 
                self.path_selected and 
                self.db_name_set and 
                self.table_name_set)
        
        if ready:
            self.convert_button.config(state='normal', bg='lightgreen')
        else:
            self.convert_button.config(state='disabled', bg='lightgray')
        
        return ready
    
    def perform_conversion(self):
        """Perform the CSV to SQLite conversion"""
        if not self.check_conversion_ready():
            messagebox.showerror("Conversion Error", 
                               "Please ensure all fields are properly filled:\n"
                               "- CSV file selected\n"
                               "- Valid database name\n"
                               "- Valid table name\n"
                               "- Save location selected")
            return
        
        try:
            # Disable button during conversion
            self.convert_button.config(state='disabled', text='Converting...')
            self.window.update()
            
            # Perform conversion
            success = convert_csv_to_sqlite(
                csv_file=globals.CSV_PATH,
                db_file=globals.DB_NAME,
                db_path=globals.DB_PATH,
                table_name=globals.TABLE_NAME
            )
            
            if success:
                # Optionally close window after successful conversion
                response = messagebox.askyesno("Conversion Complete", 
                                             "Conversion completed successfully!\n\n"
                                             "Would you like to close this window?")
                if response:
                    self.close_setup()
            
        except Exception as e:
            messagebox.showerror("Conversion Error", f"An error occurred during conversion:\n{str(e)}")
        
        finally:
            # Re-enable button
            self.convert_button.config(state='normal', text='Convert CSV to SQLite')

    def select_file(self):
        """Handle file selection with error handling"""
        try:
            filename = filedialog.askopenfilename(
                title="Select CSV Data File",
                filetypes=[
                    ("CSV files", "*.csv"),
                    ("Text files", "*.txt"),
                    ("All files", "*.*")
                ],
                initialdir=os.path.expanduser("~")
            )
            
            if filename:
                # Validate file
                if not os.path.exists(filename):
                    messagebox.showerror("File Error", "Selected file does not exist.")
                    return
                
                if not os.access(filename, os.R_OK):
                    messagebox.showerror("File Error", "Cannot read the selected file. Check permissions.")
                    return
                
                # Check file size (warn if very large)
                file_size = os.path.getsize(filename)
                if file_size > 100 * 1024 * 1024:  # 100MB
                    response = messagebox.askyesno("Large File Warning", 
                                                 f"The selected file is {file_size / (1024*1024):.1f} MB. "
                                                 "This may take a while to process. Continue?")
                    if not response:
                        return
                
                # Set global variables
                globals.CSV_PATH = filename
                self.csv_selected = True
                
                # Update UI
                filename_display = os.path.basename(filename)
                if len(filename_display) > 50:
                    filename_display = filename_display[:47] + "..."
                
                self.file_status_label.config(
                    text=f"✓ Selected: {filename_display}", 
                    fg='green'
                )
                
                self.check_conversion_ready()
                
        except Exception as e:
            messagebox.showerror("File Selection Error", f"Error selecting file:\n{str(e)}")
    
    def select_save_path(self):
        """Handle save path selection with error handling"""
        try:
            savepath = filedialog.askdirectory(
                title="Select Save Location for Database",
                initialdir=os.path.expanduser("~")
            )
            
            if savepath:
                # Test write permissions
                test_file = os.path.join(savepath, "test_write_permission.tmp")
                try:
                    with open(test_file, 'w') as f:
                        f.write("test")
                    os.remove(test_file)
                except (PermissionError, OSError):
                    messagebox.showerror("Permission Error", 
                                       "Cannot write to the selected directory. Please choose another location.")
                    return
                
                # Set global variables
                globals.DB_PATH = savepath
                self.path_selected = True
                
                # Update UI
                path_display = savepath
                if len(path_display) > 60:
                    path_display = "..." + path_display[-57:]
                
                self.path_status_label.config(
                    text=f"✓ Save to: {path_display}", 
                    fg='green'
                )
                
                self.check_conversion_ready()
                
        except Exception as e:
            messagebox.showerror("Path Selection Error", f"Error selecting save path:\n{str(e)}")
    
    def cancel_operation(self):
        """Cancel the operation with confirmation"""
        response = messagebox.askyesno("Cancel Operation", 
                                     "Are you sure you want to cancel?\n"
                                     "All current settings will be lost.")
        if response:
            self.window.destroy()

    def close_setup(self):
        """Close the setup window"""
        try:
            self.window.destroy()
        except Exception as e:
            print(f"Error closing window: {e}")

# Example usage
if __name__ == "__main__":
    # Create main window for testing
    root = tk.Tk()
    root.withdraw()  # Hide main window
    
    # Create setup window
    setup = SetupPathsWindow(root)
    
    # Start GUI loop
    root.mainloop()
