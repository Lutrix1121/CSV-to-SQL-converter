import sqlite3
import tkinter as tk
import os
from tkinter import messagebox, simpledialog, ttk
import globals


# Custom Dialog Classes for better UX
class CustomStringDialog(simpledialog.Dialog):
    """Custom string input dialog with size control"""
    
    def __init__(self, parent, title, prompt, initialvalue="", width=450, height=200):
        self.prompt = prompt
        self.initialvalue = initialvalue
        self.width = width
        self.height = height
        self.result = None
        super().__init__(parent, title)
    
    def body(self, master):
        """Create dialog body"""
        # Set window size
        self.geometry(f"{self.width}x{self.height}")
        self.resizable(True, True)
        
        # Create main frame
        main_frame = tk.Frame(master, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Add prompt label
        prompt_label = tk.Label(main_frame, text=self.prompt, 
                               font=("Arial", 10), wraplength=self.width-60,
                               justify=tk.LEFT)
        prompt_label.pack(anchor=tk.W, pady=(0, 10))
        
        # Add entry widget
        self.entry = tk.Entry(main_frame, font=("Arial", 12), width=40)
        self.entry.pack(fill=tk.X, pady=(0, 20))
        
        if self.initialvalue:
            self.entry.insert(0, self.initialvalue)
            self.entry.select_range(0, tk.END)
        
        return self.entry  # Initial focus
    
    def apply(self):
        """Process the result"""
        self.result = self.entry.get()


class CustomOptionDialog(simpledialog.Dialog):
    """Custom dialog with list selection"""
    
    def __init__(self, parent, title, prompt, options, width=500, height=350):
        self.prompt = prompt
        self.options = options
        self.width = width
        self.height = height
        self.result = None
        super().__init__(parent, title)
    
    def body(self, master):
        """Create dialog body"""
        # Set window size
        self.geometry(f"{self.width}x{self.height}")
        self.resizable(True, True)
        
        # Create main frame
        main_frame = tk.Frame(master, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Add prompt label
        prompt_label = tk.Label(main_frame, text=self.prompt, 
                               font=("Arial", 10), wraplength=self.width-60,
                               justify=tk.LEFT)
        prompt_label.pack(anchor=tk.W, pady=(0, 10))
        
        # Create listbox with scrollbar
        list_frame = tk.Frame(main_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        self.listbox = tk.Listbox(list_frame, font=("Arial", 11), selectmode=tk.SINGLE)
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.listbox.yview)
        self.listbox.configure(yscrollcommand=scrollbar.set)
        
        # Add options to listbox
        for option in self.options:
            self.listbox.insert(tk.END, option)
        
        if self.options:
            self.listbox.select_set(0)  # Select first item by default
        
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Double-click to select
        self.listbox.bind('<Double-1>', lambda e: self.ok())
        
        return self.listbox  # Initial focus
    
    def apply(self):
        """Process the result"""
        selection = self.listbox.curselection()
        if selection:
            self.result = self.options[selection[0]]


# Helper functions
def askstring_custom(title, prompt, initialvalue="", width=450, height=200, parent=None):
    """Custom askstring with size control"""
    if parent is None:
        parent = tk._default_root
    
    dialog = CustomStringDialog(parent, title, prompt, initialvalue, width, height)
    return dialog.result


def askoption_custom(title, prompt, options, width=500, height=350, parent=None):
    """Custom dialog for selecting from options"""
    if parent is None:
        parent = tk._default_root
    
    dialog = CustomOptionDialog(parent, title, prompt, options, width, height)
    return dialog.result


class editsql:
    @staticmethod
    def get_database_connection():
        """Get database connection using global DB_PATH and DB_NAME"""
        if not globals.DB_PATH:
            messagebox.showerror("Database Error", "No database path specified in globals.")
            return None
        
        if not globals.DB_NAME:
            messagebox.showerror("Database Error", "No database name specified in globals.")
            return None
        
        try:
            # Construct full database path
            db_file = globals.DB_NAME
            if not db_file.lower().endswith('.db'):
                db_file += '.db'
            
            full_db_path = os.path.join(globals.DB_PATH, db_file)
            
            # Check if database file exists
            if not os.path.exists(full_db_path):
                messagebox.showerror("Database Error", f"Database file not found: {full_db_path}")
                return None
            
            conn = sqlite3.connect(full_db_path)
            return conn
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to connect to database: {str(e)}")
            return None

    @staticmethod
    def view_database():
        """View database contents in a new window"""
        conn = editsql.get_database_connection()
        if not conn:
            return
        
        view_window = None
        try:
            cursor = conn.cursor()
            
            # Get all table names
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()
            
            if not tables:
                messagebox.showinfo("Database Viewer", "Database is empty (no tables found)")
                conn.close()
                return
            
            # Create new window for database view
            # Get the root window to use as parent
            root = None
            for widget in tk._default_root.winfo_children():
                if isinstance(widget, tk.Toplevel):
                    root = widget
                    break
            if not root:
                root = tk._default_root
            
            view_window = tk.Toplevel(root)
            view_window.title("Database Viewer")
            view_window.geometry("900x700")
            view_window.configure(bg='white')
            
            # Make window stay on top initially and grab focus
            view_window.lift()
            view_window.focus_force()
            view_window.grab_set()
            
            # Create main frame
            main_frame = tk.Frame(view_window, bg='white')
            main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            # Title label
            title_label = tk.Label(main_frame, text="Database Viewer", 
                                 font=("Arial", 16, "bold"), bg='white', fg='navy')
            title_label.pack(pady=(0, 10))
            
            # Create notebook for tabs
            notebook = ttk.Notebook(main_frame)
            notebook.pack(fill=tk.BOTH, expand=True)
            
            # Create tab for each table
            for table in tables:
                table_name = table[0]
                
                # Create frame for this table
                table_frame = ttk.Frame(notebook)
                notebook.add(table_frame, text=table_name)
                
                # Create main container
                container = tk.Frame(table_frame, bg='white')
                container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
                
                # Create treeview for table data
                tree_frame = tk.Frame(container)
                tree_frame.pack(fill=tk.BOTH, expand=True)
                
                tree = ttk.Treeview(tree_frame)
                
                # Get column information
                cursor.execute(f"PRAGMA table_info([{table_name}])")
                columns_info = cursor.fetchall()
                column_names = [col[1] for col in columns_info]
                
                # Configure treeview columns
                tree['columns'] = column_names
                tree['show'] = 'headings'
                
                for col in column_names:
                    tree.heading(col, text=col)
                    tree.column(col, width=120, minwidth=80)
                
                # Get table data - properly quote table name
                cursor.execute(f"SELECT * FROM [{table_name}]")
                rows = cursor.fetchall()
                
                # Insert data into treeview
                for i, row in enumerate(rows):
                    tree.insert('', 'end', values=row, tags=(f'row{i%2}',))
                
                # Configure alternating row colors
                tree.tag_configure('row0', background='white')
                tree.tag_configure('row1', background='#f0f0f0')
                
                # Add scrollbars
                v_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=tree.yview)
                h_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL, command=tree.xview)
                tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
                
                # Pack treeview and scrollbars
                tree.grid(row=0, column=0, sticky='nsew')
                v_scrollbar.grid(row=0, column=1, sticky='ns')
                h_scrollbar.grid(row=1, column=0, sticky='ew')
                
                tree_frame.grid_columnconfigure(0, weight=1)
                tree_frame.grid_rowconfigure(0, weight=1)
                
                # Add info label
                info_label = tk.Label(container, 
                    text=f"Table: {table_name} | Rows: {len(rows)} | Columns: {len(column_names)}", 
                    font=("Arial", 10), bg='white', fg='gray')
                info_label.pack(pady=(5, 0))
            
            # Add close button
            button_frame = tk.Frame(main_frame, bg='white')
            button_frame.pack(pady=10)
            
            close_button = tk.Button(button_frame, text="Close", 
                                   command=lambda: editsql._close_view_window(view_window, conn),
                                   font=("Arial", 12), width=15, height=2,
                                   bg='lightgray', cursor='hand2')
            close_button.pack()
            
            # Handle window closing properly
            view_window.protocol("WM_DELETE_WINDOW", 
                               lambda: editsql._close_view_window(view_window, conn))
            
            # Release grab after a short delay to prevent window from disappearing
            view_window.after(100, lambda: view_window.grab_release())
            
        except sqlite3.Error as e:
            if view_window:
                view_window.destroy()
            messagebox.showerror("Database Error", f"Failed to view database: {str(e)}")
            if conn:
                conn.close()
        except Exception as e:
            if view_window:
                view_window.destroy()
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")
            if conn:
                conn.close()
    
    @staticmethod
    def _close_view_window(window, conn):
        """Helper method to properly close the view window"""
        try:
            if conn:
                conn.close()
        except:
            pass
        try:
            window.destroy()
        except:
            pass

    @staticmethod
    def add_table():
        """Add a new table to the database"""
        conn = editsql.get_database_connection()
        if not conn:
            return
        
        try:
            # Get table name
            table_name = askstring_custom("Add Table", 
                "Enter the name for the new table:\n\nTable names should start with a letter or underscore and\ncontain only letters, numbers, and underscores.", 
                width=500, height=250)
            if not table_name:
                conn.close()
                return
            
            # Get column definitions
            columns = []
            while True:
                col_name = simpledialog.askstring("Add Column", 
                    f"Enter column name for table '{table_name}' (or click Cancel to finish):")
                if not col_name:
                    break
                
                col_type = simpledialog.askstring("Column Type", 
                    f"Enter data type for column '{col_name}' (TEXT, INTEGER, REAL, BLOB):")
                if not col_type:
                    col_type = "TEXT"
                
                # Ask if column should be PRIMARY KEY
                is_primary = messagebox.askyesno("Primary Key", 
                    f"Should column '{col_name}' be the primary key?")
                
                col_def = f"{col_name} {col_type.upper()}"
                if is_primary:
                    col_def += " PRIMARY KEY"
                
                columns.append(col_def)
            
            if not columns:
                messagebox.showwarning("No Columns", "Cannot create table without columns")
                conn.close()
                return
            
            # Create table - properly quote table name
            columns_sql = ", ".join(columns)
            cursor = conn.cursor()
            cursor.execute(f"CREATE TABLE [{table_name}] ({columns_sql})")
            conn.commit()
            
            messagebox.showinfo("Success", f"Table '{table_name}' created successfully!")
            
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to create table: {str(e)}")
        finally:
            conn.close()

    @staticmethod
    def delete_table():
        """Delete a table from the database"""
        conn = editsql.get_database_connection()
        if not conn:
            return
        
        try:
            cursor = conn.cursor()
            
            # Get all table names
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()
            
            if not tables:
                messagebox.showinfo("No Tables", "No tables found in database")
                conn.close()
                return
            
            # Create selection dialog
            table_names = [table[0] for table in tables]
            
            # Use custom option dialog for better UX
            table_name = askoption_custom("Delete Table", 
                "Select the table you want to delete:\n\n⚠️ Warning: This action cannot be undone!", 
                table_names, width=500, height=400)
            
            if not table_name or table_name not in table_names:
                conn.close()
                return
            
            # Confirm deletion
            if not messagebox.askyesno("Confirm Deletion", 
                f"Are you sure you want to delete table '{table_name}'?\nThis action cannot be undone."):
                conn.close()
                return
            
            # Delete table - properly quote table name
            cursor.execute(f"DROP TABLE [{table_name}]")
            conn.commit()
            
            messagebox.showinfo("Success", f"Table '{table_name}' deleted successfully!")
            
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to delete table: {str(e)}")
        finally:
            conn.close()

    @staticmethod
    def add_record():
        """Add a new record, allowing user to choose columns and cancel at any time"""
        conn = editsql.get_database_connection()
        if not conn:
            return
        
        try:
            cursor = conn.cursor()
            
            # Get table names
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()
            if not tables:
                messagebox.showinfo("No Tables", "No tables found in database")
                conn.close()
                return
            
            table_names = [table[0] for table in tables]
            table_name = askoption_custom("Select Table",
                "Select the table you want to add a record to:",
                table_names, width=500, height=350)
            if not table_name:
                conn.close()
                return
            
            # Get column info
            cursor.execute(f"PRAGMA table_info([{table_name}])")
            columns_info = cursor.fetchall()
            column_names = [col[1] for col in columns_info]
            column_types = [col[2] for col in columns_info]
            
            # Let user choose columns to fill
            chosen_columns = []
            while True:
                remaining_columns = [c for c in column_names if c not in chosen_columns]
                if not remaining_columns:
                    break
                
                col_choice = askoption_custom("Choose Column",
                    "Select a column to add a value for (Cancel to finish selecting):",
                    remaining_columns, width=500, height=350)
                if not col_choice:
                    break
                chosen_columns.append(col_choice)
            
            if not chosen_columns:
                messagebox.showinfo("No Columns Selected", "No columns chosen. Operation cancelled.")
                conn.close()
                return
            
            # Get values for chosen columns
            values_dict = {}
            for col in chosen_columns:
                col_type = column_types[column_names.index(col)]
                val = askstring_custom("Enter Value",
                    f"Enter value for column '{col}' ({col_type}):\nLeave blank for NULL",
                    width=500, height=300)
                if val is None:  # Cancel pressed
                    messagebox.showinfo("Cancelled", "Operation cancelled.")
                    conn.close()
                    return
                if val == "":
                    values_dict[col] = None
                else:
                    if col_type.upper() in ['INTEGER', 'INT']:
                        try:
                            values_dict[col] = int(val)
                        except ValueError:
                            values_dict[col] = val
                    elif col_type.upper() in ['REAL', 'FLOAT', 'DOUBLE']:
                        try:
                            values_dict[col] = float(val)
                        except ValueError:
                            values_dict[col] = val
                    else:
                        values_dict[col] = val
            
            # Build insert query only for chosen columns
            cols_sql = ", ".join(f"[{c}]" for c in values_dict.keys())
            placeholders = ", ".join("?" for _ in values_dict)
            cursor.execute(f"INSERT INTO [{table_name}] ({cols_sql}) VALUES ({placeholders})",
                        list(values_dict.values()))
            conn.commit()
            
            messagebox.showinfo("Success", f"Record added to '{table_name}' successfully!")
        
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to add record: {str(e)}")
        finally:
            conn.close()


    @staticmethod
    def delete_record():
        """Delete a record from a table using one or more columns as filters"""
        conn = editsql.get_database_connection()
        if not conn:
            return
        
        try:
            cursor = conn.cursor()
            
            # Get all table names
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()
            if not tables:
                messagebox.showinfo("No Tables", "No tables found in database")
                conn.close()
                return
            
            table_names = [table[0] for table in tables]
            table_name = askoption_custom("Delete Record", 
                "Select the table to delete records from:", 
                table_names, width=500, height=350)
            if not table_name:
                conn.close()
                return
            
            # Get column information
            cursor.execute(f"PRAGMA table_info([{table_name}])")
            columns_info = cursor.fetchall()
            column_names = [col[1] for col in columns_info]
            column_types = [col[2] for col in columns_info]
            
            # Let user select columns for filtering
            chosen_columns = []
            while True:
                remaining_columns = [c for c in column_names if c not in chosen_columns]
                if not remaining_columns:
                    break
                
                col_choice = askoption_custom("Choose Filter Column",
                    "Select a column to filter by (Cancel to finish selecting):",
                    remaining_columns, width=500, height=350)
                if not col_choice:
                    break
                chosen_columns.append(col_choice)
            
            if not chosen_columns:
                messagebox.showinfo("No Filters", "No columns chosen. Operation cancelled.")
                conn.close()
                return
            
            # Get filter values
            conditions = []
            params = []
            for col in chosen_columns:
                col_type = column_types[column_names.index(col)]
                val = askstring_custom("Filter Value",
                    f"Enter value for column '{col}' ({col_type}):\nOnly records matching this will be deleted.",
                    width=500, height=300)
                if val is None:  # Cancel pressed
                    messagebox.showinfo("Cancelled", "Operation cancelled.")
                    conn.close()
                    return
                conditions.append(f"[{col}] = ?")
                params.append(val)
            
            where_clause = " AND ".join(conditions)
            
            # Preview matching records
            cursor.execute(f"SELECT * FROM [{table_name}] WHERE {where_clause}", params)
            records = cursor.fetchall()
            if not records:
                messagebox.showinfo("No Records", "No records match the given criteria.")
                conn.close()
                return
            
            # Confirm deletion
            if not messagebox.askyesno("Confirm Deletion", 
                f"Found {len(records)} record(s) matching your filters.\nAre you sure you want to delete them?"):
                conn.close()
                return
            
            # Delete records
            cursor.execute(f"DELETE FROM [{table_name}] WHERE {where_clause}", params)
            conn.commit()
            
            messagebox.showinfo("Success", f"Deleted {cursor.rowcount} record(s) from '{table_name}'.")
        
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to delete record: {str(e)}")
        finally:
            conn.close()


    @staticmethod
    def add_column():
        """Add a new column to a table"""
        conn = editsql.get_database_connection()
        if not conn:
            return
        
        try:
            cursor = conn.cursor()
            
            # Get all table names
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()
            
            if not tables:
                messagebox.showinfo("No Tables", "No tables found in database")
                conn.close()
                return
            
            table_names = [table[0] for table in tables]
            table_name = askoption_custom("Add Column", 
                "Select the table to add a column to:", 
                table_names, width=500, height=350)
            
            if not table_name or table_name not in table_names:
                conn.close()
                return
            
            # Get column details
            column_name = askstring_custom("Column Name", 
                "Enter the name for the new column:\n\nColumn names should start with a letter or underscore\nand contain only letters, numbers, and underscores.", 
                width=500, height=250)
            if not column_name:
                conn.close()
                return
            
            # Get column type with options
            column_types = ["TEXT", "INTEGER", "REAL", "BLOB"]
            column_type = askoption_custom("Column Type", 
                "Select the data type for the new column:", 
                column_types, width=400, height=300)
            if not column_type:
                column_type = "TEXT"
            
            default_value = askstring_custom("Default Value", 
                f"Enter a default value for existing records (optional):\n\nThis value will be assigned to the '{column_name}' column\nfor all existing records in the table.\n\nLeave blank for NULL.", 
                width=500, height=300)
            
            # Add column - properly quote table and column names
            sql = f"ALTER TABLE [{table_name}] ADD COLUMN [{column_name}] {column_type.upper()}"
            if default_value:
                sql += f" DEFAULT '{default_value}'"
            
            cursor.execute(sql)
            conn.commit()
            
            messagebox.showinfo("Success", f"Column '{column_name}' added to table '{table_name}' successfully!")
            
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to add column: {str(e)}")
        finally:
            conn.close()

    @staticmethod
    def delete_column():
        """Delete a column from a table (SQLite limitation workaround)"""
        conn = editsql.get_database_connection()
        if not conn:
            return
        
        try:
            cursor = conn.cursor()
            
            # Get all table names
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()
            
            if not tables:
                messagebox.showinfo("No Tables", "No tables found in database")
                conn.close()
                return
            
            table_names = [table[0] for table in tables]
            table_name = askoption_custom("Delete Column", 
                "Select the table to delete a column from:", 
                table_names, width=500, height=350)
            
            if not table_name or table_name not in table_names:
                conn.close()
                return
            
            # Get column information - properly quote table name
            cursor.execute(f"PRAGMA table_info([{table_name}])")
            columns_info = cursor.fetchall()
            column_names = [col[1] for col in columns_info]
            
            column_to_delete = askoption_custom("Delete Column", 
                f"Select the column to delete from table '{table_name}':\n\n⚠️ Warning: This will recreate the table without this column.\nThis action cannot be undone!", 
                column_names, width=500, height=400)
            
            if not column_to_delete or column_to_delete not in column_names:
                conn.close()
                return
            
            # Confirm deletion
            if not messagebox.askyesno("Confirm Deletion", 
                f"Are you sure you want to delete column '{column_to_delete}' from table '{table_name}'?\n"
                "This will recreate the table without this column."):
                conn.close()
                return
            
            # SQLite doesn't support DROP COLUMN directly, so we need to recreate the table
            remaining_columns = [col for col in column_names if col != column_to_delete]
            
            if not remaining_columns:
                messagebox.showerror("Error", "Cannot delete the last column from a table")
                conn.close()
                return
            
            # Create new table without the column
            temp_table = f"{table_name}_temp"
            columns_sql = ", ".join([f"[{col}]" for col in remaining_columns])  # Quote column names
            
            # Create temporary table with remaining columns - properly quote all names
            cursor.execute(f"CREATE TABLE [{temp_table}] AS SELECT {columns_sql} FROM [{table_name}]")
            
            # Drop original table - properly quote table name
            cursor.execute(f"DROP TABLE [{table_name}]")
            
            # Rename temporary table - properly quote table names
            cursor.execute(f"ALTER TABLE [{temp_table}] RENAME TO [{table_name}]")
            
            conn.commit()
            
            messagebox.showinfo("Success", f"Column '{column_to_delete}' deleted from table '{table_name}' successfully!")
            
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to delete column: {str(e)}")
        finally:
            conn.close()

    @staticmethod
    def edit_record():
        """Edit an existing record in a table"""
        conn = editsql.get_database_connection()
        if not conn:
            return
        
        try:
            cursor = conn.cursor()
            
            # Get all table names
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()
            
            if not tables:
                messagebox.showinfo("No Tables", "No tables found in database")
                conn.close()
                return
            
            table_names = [table[0] for table in tables]
            table_name = askoption_custom("Edit Record", 
                "Select the table containing the record to edit:", 
                table_names, width=500, height=350)
            
            if not table_name or table_name not in table_names:
                conn.close()
                return
            
            # Get column information - properly quote table name
            cursor.execute(f"PRAGMA table_info([{table_name}])")
            columns_info = cursor.fetchall()
            column_names = [col[1] for col in columns_info]
            
            # Get WHERE condition to identify record
            where_column = askoption_custom("Identify Record", 
                f"Select the column to use for identifying the record to edit:\n\nChoose a column that uniquely identifies the record you want to modify.", 
                column_names, width=500, height=400)
            
            if not where_column or where_column not in column_names:
                conn.close()
                return
            
            where_value = askstring_custom("Record Value", 
                f"Enter the current value in column '{where_column}' to identify the record:\n\nThis will be used to find the specific record you want to edit.", 
                width=500, height=300)
            
            if where_value is None:
                conn.close()
                return
            
            # Show current record - properly quote table and column names
            cursor.execute(f"SELECT * FROM [{table_name}] WHERE [{where_column}] = ?", (where_value,))
            records = cursor.fetchall()
            
            if not records:
                messagebox.showinfo("No Records", f"No records found with {where_column} = '{where_value}'")
                conn.close()
                return
            
            if len(records) > 1:
                messagebox.showwarning("Multiple Records", 
                    f"Found {len(records)} records. Only the first one will be edited.")
            
            # Get column to edit
            edit_column = askoption_custom("Edit Column", 
                f"Select the column you want to edit:\n\nCurrent record values will be shown after selection.", 
                column_names, width=500, height=400)
            
            if not edit_column or edit_column not in column_names:
                conn.close()
                return
            
            # Get new value
            current_record = records[0]
            current_index = column_names.index(edit_column)
            current_value = current_record[current_index]
            
            new_value = askstring_custom("New Value", 
                f"Column: {edit_column}\nCurrent value: {current_value}\n\nEnter the new value for this column:\n(Leave blank to set to NULL)", 
                initialvalue=str(current_value) if current_value is not None else "", 
                width=500, height=350)
            
            if new_value is None:  # User clicked Cancel
                conn.close()
                return
            
            if new_value == "":
                new_value = None
            
            # Update record - properly quote table and column names
            cursor.execute(f"UPDATE [{table_name}] SET [{edit_column}] = ? WHERE [{where_column}] = ?", 
                         (new_value, where_value))
            conn.commit()
            
            messagebox.showinfo("Success", f"Record updated successfully in table '{table_name}'!")
            
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to edit record: {str(e)}")
        finally:
            conn.close()
               

            