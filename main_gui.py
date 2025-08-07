import tkinter as tk
from tkinter import messagebox
import sys
import os
from GUI_tooltip import ToolTip
from convert_gui import SetupPathsWindow
import globals

class BaseWindow:
    """Base class for all GUI windows with common functionality"""
    
    def __init__(self, parent=None, title="Window", geometry="1000x850"):
        self.parent = parent
        
        # Initialize theme
        self.current_theme = {
            'bg': 'white',
            'text': 'black',
            'button_bg': 'lightblue',
            'button_fg': 'black'
        }
        
        if parent:
            self.window = tk.Toplevel(parent)
            self.window.transient(parent)
            self.window.grab_set()
            self.window.focus_set()
        else:
            self.window = tk.Tk()
            
        self.window.title(title)
        self.window.geometry(geometry)
        self.window.configure(bg=self.current_theme['bg'])
        self.window.resizable(width=False, height=False)

    def center_window(self):
        """Center the window on screen"""
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (self.window.winfo_width() // 2)
        y = (self.window.winfo_screenheight() // 2) - (self.window.winfo_height() // 2)
        self.window.geometry(f"+{x}+{y}")
    
    def create_button_frame(self, buttons_config):
        """Create a frame with buttons based on configuration"""
        button_frame = tk.Frame(self.window, bg=self.current_theme['bg'])
        button_frame.pack(pady=20)
        
        for config in buttons_config:
            button = tk.Button(
                button_frame,
                text=config['text'],
                command=config['command'],
                font=config.get('font', ("Arial", 12)),
                width=config.get('width', 15),
                height=config.get('height', 2),
                bg=config.get('bg', self.current_theme['button_bg']),
                fg=config.get('fg', self.current_theme['button_fg']),
                cursor='hand2'
            )
            button.pack(side='left', padx=10)
            
            # Add tooltip if provided
            if 'tooltip' in config:
                ToolTip(button, config['tooltip'])
        
        return button_frame

class MainGUI(BaseWindow):
    """Main GUI window class"""
    
    def __init__(self):
        super().__init__(None, "CSV to SQL Database Converter", "800x600")
        self.conversion_window = None
        self.setup_ui()
        self.center_window()
    
    def setup_ui(self):
        """Setup the main user interface"""
        try:
            self.create_title()
            self.create_status_section()
            self.create_action_buttons()
            self.create_terminate_button()
        except Exception as e:
            messagebox.showerror("UI Setup Error", f"Failed to create main interface: {str(e)}")
            self.window.destroy()

    def create_title(self):
        """Create title label"""
        title_label = tk.Label(
            self.window, 
            text="CSV to SQL Database Converter",
            font=("Arial", 24, "bold"), 
            bg=self.current_theme['bg'], 
            fg='navy'
        )
        title_label.pack(pady=30)
        
        # Subtitle
        subtitle_label = tk.Label(
            self.window,
            text="Convert your CSV files to SQLite databases with ease",
            font=("Arial", 12),
            bg=self.current_theme['bg'],
            fg='gray'
        )
        subtitle_label.pack(pady=(0, 20))

    def create_status_section(self):
        """Create status display section"""
        status_frame = tk.Frame(self.window, bg=self.current_theme['bg'])
        status_frame.pack(pady=20, padx=40, fill='x')
        
        status_title = tk.Label(
            status_frame,
            text="Current Status:",
            font=("Arial", 12, "bold"),
            bg=self.current_theme['bg'],
            fg='black'
        )
        status_title.pack(anchor='center')
        
        self.status_label = tk.Label(
            status_frame,
            text="Ready to convert CSV files",
            font=("Arial", 10),
            bg=self.current_theme['bg'],
            fg='green',
            justify='center'
        )
        self.status_label.pack(anchor='center', pady=(5, 0))
        
        # Display current global variables if set
        self.update_status_display()
    
    def update_status_display(self):
        """Update the status display with current settings"""
        status_parts = []
        
        if globals.CSV_PATH:
            filename = os.path.basename(globals.CSV_PATH)
            status_parts.append(f"CSV File: {filename}")
        
        if globals.DB_NAME:
            status_parts.append(f"Database: {globals.DB_NAME}")
            
        if globals.TABLE_NAME:
            status_parts.append(f"Table: {globals.TABLE_NAME}")
            
        if globals.DB_PATH:
            status_parts.append(f"Save Path: {globals.DB_PATH}")
        
        if status_parts:
            status_text = "Current Settings:\n" + "\n".join(status_parts)
            self.status_label.config(text=status_text, fg='blue')
        else:
            self.status_label.config(text="Ready to convert CSV files", fg='green')


    def create_action_buttons(self):
        """Create main action buttons"""
        button_frame = tk.Frame(self.window, bg=self.current_theme['bg'])
        button_frame.pack(pady=30)
        
        # Convert button
        convert_button = tk.Button(
            button_frame, 
            text="Start Conversion",
            command=self.open_conversion,
            font=("Arial", 16, "bold"), 
            width=20, 
            height=2, 
            bg='lightgreen',
            fg='darkgreen',
            cursor='hand2',
            relief='raised'
        )
        convert_button.pack(pady=(5, 20))
        ToolTip(convert_button, "Open the conversion wizard to convert CSV files to SQLite database")
    
        # Edit database button (placeholder for future functionality)
        editdb_button = tk.Button(
            button_frame, 
            text="Database Tools",
            command=self.open_edit_database,
            font=("Arial", 16, 'bold'), 
            width=20, 
            height=2, 
            bg='lightblue',
            fg='darkblue',
            cursor='hand2',
            state='disabled'  # Disabled until implemented
        )
        editdb_button.pack(pady=10)
        ToolTip(editdb_button, "Database editing tools (Coming soon)")
    
    def create_terminate_button(self):
        """Create terminate button"""
        terminate_frame = tk.Frame(self.window, bg=self.current_theme['bg'])
        terminate_frame.pack(side='bottom', pady=20)
        
        terminate_button = tk.Button(
            terminate_frame, 
            text="Exit Application",
            command=self.safe_exit,
            font=("Arial", 14, 'bold'), 
            width=20, 
            height=2, 
            bg='red',
            fg='black',
            cursor='hand2'
        )
        terminate_button.pack(pady=10)
        ToolTip(terminate_button, "Close the application")
    
    def safe_exit(self):
        """Safely exit the application with confirmation"""
        response = messagebox.askyesno(
            "Exit Application", 
            "Are you sure you want to exit the CSV to SQL Converter?"
        )
        if response:
            try:
                # Close any open conversion windows
                if self.conversion_window and hasattr(self.conversion_window, 'window'):
                    self.conversion_window.window.destroy()
            except:
                pass
            finally:
                self.window.destroy()
    
    def open_conversion(self):
        """Open the conversion setup window"""
        try:
            # Check if conversion window is already open
            if self.conversion_window and hasattr(self.conversion_window, 'window'):
                try:
                    # Try to bring existing window to front
                    self.conversion_window.window.lift()
                    self.conversion_window.window.focus_set()
                    return
                except tk.TclError:
                    # Window was destroyed, create new one
                    pass
            
            # Create new conversion window
            self.conversion_window = SetupPathsWindow(self.window)
            
            # Update status when conversion window is closed
            self.window.after(1000, self.check_conversion_window)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open conversion window:\n{str(e)}")
    
    def check_conversion_window(self):
        """Check if conversion window is still open and update status"""
        try:
            if self.conversion_window and hasattr(self.conversion_window, 'window'):
                # Check if window still exists
                self.conversion_window.window.winfo_exists()
                # Schedule next check
                self.window.after(1000, self.check_conversion_window)
            else:
                # Window is closed, update status
                self.update_status_display()
        except tk.TclError:
            # Window was destroyed, update status
            self.conversion_window = None
            self.update_status_display()
        except Exception:
            # Schedule next check in case of other errors
            self.window.after(1000, self.check_conversion_window)
    
    def open_edit_database(self):
        """Open database editing tools (placeholder)"""
        messagebox.showinfo(
            "Feature Coming Soon", 
            "Database editing tools will be available in a future version.\n\n"
            "For now, you can use external SQLite tools to view and edit your databases."
        )
    
    def run(self):
        """Start the main GUI loop"""
        try:
            self.window.protocol("WM_DELETE_WINDOW", self.safe_exit)
            self.window.mainloop()
        except Exception as e:
            messagebox.showerror("Application Error", f"An error occurred: {str(e)}")

# Factory function to maintain compatibility with existing code
def create_main_gui():
    """Create and run the main GUI application"""
    try:
        app = MainGUI()
        app.run()
    except Exception as e:
        if tk._default_root:  # If tkinter was initialized
            messagebox.showerror("Startup Error", f"Failed to start application:\n{str(e)}")
        else:
            print(f"Failed to start application: {str(e)}")

# Application entry point
if __name__ == "__main__":
    create_main_gui()
