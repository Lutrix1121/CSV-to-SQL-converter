import tkinter as tk
from tkinter import messagebox
from GUI_tooltip import ToolTip
from edit_sql import editsql
from theme_manager import ThemableWindow, get_app_theme_manager


class editgui(ThemableWindow):
    """Database editing GUI with theme support"""
    
    def __init__(self, parent):
        # Initialize theming first
        ThemableWindow.__init__(self, get_app_theme_manager())
        
        self.parent = parent
        
        # Get current theme
        self.current_theme = self.theme_manager.get_current_theme()
        
        # Create window
        self.window = tk.Toplevel(parent)
        self.window.title("Edit database")
        self.window.geometry("1300x850")
        self.window.configure(bg=self.current_theme['bg'])
        self.window.resizable(width=False, height=False)
        
        self.window.transient(parent)
        self.window.grab_set()
        self.window.focus_set()
        
        try:
            self.setup_ui()
            # Apply initial theme
            self.apply_theme()
        except Exception as e:
            messagebox.showerror("UI Setup Error", f"Failed to create interface: {str(e)}")
            self.window.destroy()
    
    def on_theme_changed(self, new_theme):
        """Called when theme changes"""
        self.current_theme = new_theme
        self.window.configure(bg=self.current_theme['bg'])
        self.apply_theme()
        
    def setup_ui(self):
        """Setup the user interface"""
        # Theme toggle at top
        self.create_theme_toggle_section()
        
        # Title
        self.title_label = tk.Label(
            self.window, 
            text="Database Editing Tools",
            font=("Arial", 16, "bold"), 
            bg=self.current_theme['bg'], 
            fg=self.current_theme['title_color']
        )
        self.title_label.pack(pady=0)
        self.register_special_widget(self.title_label, 'title')
        
        self.view_db_section()
        self.add_delete_table_section()
        self.add_delete_record_section()
        self.edit_record_section()
        self.add_delete_column_section()
        self.create_control_buttons()

    def create_theme_toggle_section(self):
        """Create theme toggle button"""
        theme_frame = tk.Frame(self.window, bg=self.current_theme['bg'])
        theme_frame.pack(anchor='ne', padx=10, pady=5)
        
        self.theme_button = self.create_theme_toggle(theme_frame)
        self.theme_button.pack()
        self.register_special_widget(self.theme_button, 'theme_toggle')

    def view_db_section(self):
        """Section to view the database"""
        view_frame = tk.Frame(self.window, bg=self.current_theme['bg'])
        view_frame.pack(pady=(15,0), padx=20, fill='x')
        
        # Create a bordered section
        section_frame = tk.Frame(view_frame, bg=self.current_theme['bg'], relief='ridge', bd=2)
        section_frame.pack(fill='x', padx=10, pady=5)
        
        view_label = tk.Label(
            section_frame, 
            text="📋 View Database", 
            font=("Arial", 14, "bold"), 
            bg=self.current_theme['bg'], 
            fg=self.current_theme['text']
        )
        view_label.pack(pady=10)
        
        view_button = tk.Button(
            section_frame, 
            text="View Database Contents",
            command=editsql.view_database,
            font=("Arial", 11),
            width=25,
            height=2,
            bg=self.current_theme['button_bg'],
            fg=self.current_theme['button_fg'],
            cursor='hand2'
        )
        view_button.pack(pady=(0, 10))
        ToolTip(view_button, "Click to view the database contents in a new window")

    def add_delete_table_section(self):
        """Section to add or delete tables"""
        table_frame = tk.Frame(self.window, bg=self.current_theme['bg'])
        table_frame.pack(pady=0, padx=20, fill='x')
        
        # Create a bordered section
        section_frame = tk.Frame(table_frame, bg=self.current_theme['bg'], relief='ridge', bd=2)
        section_frame.pack(fill='x', padx=10, pady=5)
        
        table_label = tk.Label(
            section_frame, 
            text="🗃️ Manage Tables", 
            font=("Arial", 14, "bold"), 
            bg=self.current_theme['bg'], 
            fg=self.current_theme['text']
        )
        table_label.pack(pady=10)

        # Input section
        input_frame = tk.Frame(section_frame, bg=self.current_theme['bg'])
        input_frame.pack(pady=5)
        
        # Button section
        button_frame = tk.Frame(section_frame, bg=self.current_theme['bg'])
        button_frame.pack(pady=10)
        
        add_table_button = tk.Button(
            button_frame, 
            text="Add Table", 
            command=editsql.add_table,
            font=("Arial", 11),
            width=15,
            bg=self.current_theme['convert_bg'],
            fg=self.current_theme['convert_fg'],
            cursor='hand2'
        )
        add_table_button.pack(side='left', padx=5)
        self.register_special_widget(add_table_button, 'convert')
        
        delete_table_button = tk.Button(
            button_frame, 
            text="Delete Table", 
            command=editsql.delete_table,
            font=("Arial", 11),
            width=15,
            bg=self.current_theme['exit_bg'],
            fg=self.current_theme['exit_fg'],
            cursor='hand2'
        )
        delete_table_button.pack(side='left', padx=5)
        self.register_special_widget(delete_table_button, 'exit')

    def add_delete_record_section(self):
        """Section to add or delete records"""
        record_frame = tk.Frame(self.window, bg=self.current_theme['bg'])
        record_frame.pack(pady=0, padx=20, fill='x')
        
        # Create a bordered section
        section_frame = tk.Frame(record_frame, bg=self.current_theme['bg'], relief='ridge', bd=2)
        section_frame.pack(fill='x', padx=10, pady=5)
        
        record_label = tk.Label(
            section_frame, 
            text="📝 Manage Records", 
            font=("Arial", 14, "bold"), 
            bg=self.current_theme['bg'], 
            fg=self.current_theme['text']
        )
        record_label.pack(pady=10)
        
        # Button section
        button_frame = tk.Frame(section_frame, bg=self.current_theme['bg'])
        button_frame.pack(pady=10)
        
        add_record_button = tk.Button(
            button_frame, 
            text="Add Record", 
            command=editsql.add_record,
            font=("Arial", 11),
            width=15,
            bg=self.current_theme['convert_bg'],
            fg=self.current_theme['convert_fg'],
            cursor='hand2'
        )
        add_record_button.pack(side='left', padx=5)
        self.register_special_widget(add_record_button, 'convert')
        
        delete_record_button = tk.Button(
            button_frame, 
            text="Delete Record", 
            command=editsql.delete_record,
            font=("Arial", 11),
            width=15,
            bg=self.current_theme['exit_bg'],
            fg=self.current_theme['exit_fg'],
            cursor='hand2'
        )
        delete_record_button.pack(side='left', padx=5)
        self.register_special_widget(delete_record_button, 'exit')

    def add_delete_column_section(self):
        """Section to add or delete columns"""
        column_frame = tk.Frame(self.window, bg=self.current_theme['bg'])
        column_frame.pack(pady=0, padx=20, fill='x')
        
        # Create a bordered section
        section_frame = tk.Frame(column_frame, bg=self.current_theme['bg'], relief='ridge', bd=2)
        section_frame.pack(fill='x', padx=10, pady=5)
        
        column_label = tk.Label(
            section_frame, 
            text="🏛️ Manage Columns", 
            font=("Arial", 14, "bold"), 
            bg=self.current_theme['bg'], 
            fg=self.current_theme['text']
        )
        column_label.pack(pady=10)
        
        # Button section
        button_frame = tk.Frame(section_frame, bg=self.current_theme['bg'])
        button_frame.pack(pady=10)
        
        add_column_button = tk.Button(
            button_frame, 
            text="Add Column", 
            command=editsql.add_column,
            font=("Arial", 11),
            width=15,
            bg=self.current_theme['convert_bg'],
            fg=self.current_theme['convert_fg'],
            cursor='hand2'
        )
        add_column_button.pack(side='left', padx=5)
        self.register_special_widget(add_column_button, 'convert')
        
        delete_column_button = tk.Button(
            button_frame, 
            text="Delete Column", 
            command=editsql.delete_column,
            font=("Arial", 11),
            width=15,
            bg=self.current_theme['exit_bg'],
            fg=self.current_theme['exit_fg'],
            cursor='hand2'
        )
        delete_column_button.pack(side='left', padx=5)
        self.register_special_widget(delete_column_button, 'exit')

    def edit_record_section(self):
        """Section to edit records"""
        edit_frame = tk.Frame(self.window, bg=self.current_theme['bg'])
        edit_frame.pack(pady=0, padx=20, fill='x')
        
        # Create a bordered section
        section_frame = tk.Frame(edit_frame, bg=self.current_theme['bg'], relief='ridge', bd=2)
        section_frame.pack(fill='x', padx=10, pady=5)
        
        edit_label = tk.Label(
            section_frame, 
            text="✏️ Edit Records", 
            font=("Arial", 14, "bold"), 
            bg=self.current_theme['bg'], 
            fg=self.current_theme['text']
        )
        edit_label.pack(pady=10)
        
        # Button section
        button_frame = tk.Frame(section_frame, bg=self.current_theme['bg'])
        button_frame.pack(pady=10)
        
        edit_record_button = tk.Button(
            button_frame, 
            text="Edit Record", 
            command=editsql.edit_record,
            font=("Arial", 11),
            width=15,
            bg=self.current_theme['edit_bg'],
            fg=self.current_theme['edit_fg'],
            cursor='hand2'
        )
        edit_record_button.pack(pady=5)
        self.register_special_widget(edit_record_button, 'edit')

    def create_control_buttons(self):
        """Create control buttons"""
        button_frame = tk.Frame(self.window, bg=self.current_theme['bg'])
        button_frame.pack(pady=30)
        
        # Info/Help button
        help_button = tk.Button(
            button_frame, 
            text="Help & Info",
            command=self.show_help,
            font=("Arial", 12), 
            width=15, 
            height=2, 
            bg=self.current_theme['button_bg'],
            fg=self.current_theme['button_fg'],
            cursor='hand2'
        )
        help_button.pack(side='left', padx=10)
        ToolTip(help_button, "Show help information about database editing")
        
        # Close button
        done_button = tk.Button(
            button_frame, 
            text="Close",
            command=self.close_setup,
            font=("Arial", 12), 
            width=15, 
            height=2, 
            bg=self.current_theme['button_bg'],
            fg=self.current_theme['button_fg'],
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
            bg=self.current_theme['exit_bg'],
            fg=self.current_theme['exit_fg'],
            cursor='hand2'
        )
        cancel_button.pack(side='left', padx=10)
        self.register_special_widget(cancel_button, 'exit')

    def show_help(self):
        """Show help information"""
        help_text = """Database Editing Tools Help:

🔍 View Database: Display all tables and their contents
📊 Add Table: Create a new table in the database
🗑️ Delete Table: Remove an existing table
➕ Add Record: Insert new data into a table
❌ Delete Record: Remove specific records
📝 Edit Record: Modify existing record data
🏛️ Add Column: Add new columns to tables
🗂️ Delete Column: Remove columns from tables

Note: Always backup your database before making changes!"""
        
        messagebox.showinfo("Database Tools Help", help_text)

    def cancel_operation(self):
        """Cancel the operation with confirmation"""
        response = messagebox.askyesno("Cancel Operation", 
                                    "Are you sure you want to cancel?\n"
                                    "Any unsaved changes will be lost.")
        if response:
            # Call the parent's cleanup if it exists
            if hasattr(self.parent, 'edit_window') and self.parent.edit_window == self:
                self.parent.edit_window = None
            
            # Unregister from theme callbacks before destroying
            try:
                self.theme_manager.unregister_theme_callback(self.on_theme_changed)
            except:
                pass
            self.window.destroy()

    def close_setup(self):
        """Close the setup window"""
        try:
            # Call the parent's cleanup if it exists
            if hasattr(self.parent, 'edit_window') and self.parent.edit_window == self:
                self.parent.edit_window = None
            
            # Unregister from theme callbacks before destroying
            try:
                self.theme_manager.unregister_theme_callback(self.on_theme_changed)
            except:
                pass
            self.window.destroy()
        except Exception as e:
            print(f"Error closing window: {e}")

# Example usage for testing
if __name__ == "__main__":
    # Create main window for testing
    root = tk.Tk()
    root.withdraw()  # Hide main window
    
    # Create edit window
    edit_window = editgui(root)
    
    # Start GUI loop
    root.mainloop()
