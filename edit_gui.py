import tkinter as tk
from tkinter import messagebox
from GUI_tooltip import ToolTip
from edit_sql import editsql


class editgui:
    def __init__(self, parent):
        self.parent = parent
        
        # Initialize theme
        self.current_theme = {
            'bg': 'white',
            'text': 'black'
        }
        
        # Create window
        self.window = tk.Toplevel(parent)
        self.window.title("Edit database")
        self.window.geometry("1300x800")
        self.window.configure(bg='white')
        self.window.resizable(width=False, height=False)
        
        self.window.transient(parent)
        self.window.grab_set()
        self.window.focus_set()
        
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
            text="Created database editing tools",
            font=("Arial", 16, "bold"), 
            bg='white', 
            fg='black'
        )
        title_label.pack(pady=20)
        
        self.view_db_section()
        self.add_delete_table_section()
        self.add_delete_record_section()
        self.edit_record_section()
        self.add_delete_column_section()
        self.create_control_buttons()

    def view_db_section(self):
        """Section to view the database"""
        view_frame = tk.Frame(self.window, bg=self.current_theme['bg'])
        view_frame.pack(pady=10, padx=20, fill='x')
        
        view_label = tk.Label(view_frame, text="View Database", font=("Arial", 14), bg='white', fg='black')
        view_label.pack(padx=10, pady=5)
        
        # Placeholder for database viewing functionality
        view_button = tk.Button(view_frame, text="View Database", command=editsql.view_database)
        view_button.pack(pady=5)
        ToolTip(view_button, "Click to view the database contents in a new window")

    def add_delete_table_section(self):
        """Section to add or delete tables"""
        table_frame = tk.Frame(self.window, bg=self.current_theme['bg'])
        table_frame.pack(pady=10, padx=20, fill='x')
        
        table_label = tk.Label(table_frame, text="Add/Delete Table", font=("Arial", 14), bg='white', fg='black')
        table_label.pack(anchor='center')

        table_entry = tk.Entry(table_frame, width=20)
        table_entry.pack(padx=5, pady=5)
        ToolTip(table_entry, "Enter the name of table you want to add or delete")
        
        add_table_button = tk.Button(table_frame, text="Add Table", command=editsql.add_table)
        add_table_button.pack(padx=5, pady=5)
        
        delete_table_button = tk.Button(table_frame, text="Delete Table", command=editsql.delete_table)
        delete_table_button.pack(padx=5, pady=5)

    def add_delete_record_section(self):
        """Section to add or delete records"""
        record_frame = tk.Frame(self.window, bg=self.current_theme['bg'])
        record_frame.pack(pady=10, padx=20, fill='x')
        
        record_label = tk.Label(record_frame, text="Add/Delete Record", font=("Arial", 14), bg='white', fg='black')
        record_label.pack(padx=5, pady=5)

        record_entry = tk.Entry(record_frame, width=20)
        record_entry.pack(padx=5, pady=5)
        ToolTip(record_entry, "Enter the record details you want to add or delete (table name and record data)")
        
        add_record_button = tk.Button(record_frame, text="Add Record", command=editsql.add_record)
        add_record_button.pack(padx=5, pady=5)
        
        delete_record_button = tk.Button(record_frame, text="Delete Record", command=editsql.delete_record)
        delete_record_button.pack(padx=5, pady=5)

    def add_delete_column_section(self):
        """Section to add or delete columns"""
        column_frame = tk.Frame(self.window, bg=self.current_theme['bg'])
        column_frame.pack(pady=10, padx=20, fill='x')
        
        column_label = tk.Label(column_frame, text="Add/Delete Column", font=("Arial", 14), bg='white', fg='black')
        column_label.pack(anchor='center')

        column_entry = tk.Entry(column_frame, width=20)
        column_entry.pack(padx=5, pady=5)
        ToolTip(column_entry, "Enter the name of the column you want to add or delete")
        
        add_column_button = tk.Button(column_frame, text="Add Column", command=editsql.add_column)
        add_column_button.pack(padx=5, pady=5)
        
        delete_column_button = tk.Button(column_frame, text="Delete Column", command=editsql.delete_column)
        delete_column_button.pack(padx=5, pady=5)

    def edit_record_section(self):
        """Section to edit records"""
        edit_frame = tk.Frame(self.window, bg=self.current_theme['bg'])
        edit_frame.pack(pady=10, padx=20, fill='x')
        
        edit_label = tk.Label(edit_frame, text="Edit Record", font=("Arial", 14), bg='white', fg='black')
        edit_label.pack(anchor='center')

        edit_entry = tk.Entry(edit_frame, width=20)
        edit_entry.pack(padx=5, pady=5)
        ToolTip(edit_entry, "Enter the record details you want to edit (table name, name of column and new data)")
        
        edit_record_button = tk.Button(edit_frame, text="Edit Record", command=editsql.edit_record)
        edit_record_button.pack(padx=5, pady=5)

    def create_control_buttons(self):
        button_frame = tk.Frame(self.window, bg=self.current_theme['bg'])
        button_frame.pack(pady=30)
        
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

