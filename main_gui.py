import tkinter as tk
from edit_gui import editgui
from tkinter import messagebox
import sys
import os
from GUI_tooltip import ToolTip
from convert_gui import SetupPathsWindow
from theme_manager import ThemableWindow, get_app_theme_manager
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

class MainGUI(BaseWindow, ThemableWindow):
    """Main GUI window class with dark mode support"""
    
    def __init__(self):
        # Initialize theming first
        ThemableWindow.__init__(self, get_app_theme_manager())
        
        # Initialize base window
        BaseWindow.__init__(self, None, "CSV to SQL Database Converter", "800x650")
        
        self.conversion_window = None
        self.edit_window = None
        
        # Get initial theme
        self.current_theme = self.theme_manager.get_current_theme()
        
        self.setup_ui()
        self.center_window()
        
        # Apply initial theme
        self.apply_theme()
    
    def setup_ui(self):
        """Setup the main user interface"""
        try:
            self.create_theme_toggle_section()
            self.create_title()
            self.create_status_section()
            self.create_action_buttons()
            self.create_terminate_button()
        except Exception as e:
            messagebox.showerror("UI Setup Error", f"Failed to create main interface: {str(e)}")
            self.window.destroy()

    def create_theme_toggle_section(self):
        """Create theme toggle button in top-right corner"""
        theme_frame = tk.Frame(self.window, bg=self.current_theme['bg'])
        theme_frame.pack(anchor='ne', padx=10, pady=10)
        
        self.theme_button = self.create_theme_toggle(theme_frame)
        self.theme_button.pack()
        ToolTip(self.theme_button, "Toggle between light and dark mode")
        
        # Register the theme button as special widget
        self.register_special_widget(self.theme_button, 'theme_toggle')

    def create_title(self):
        """Create title label"""
        self.title_label = tk.Label(
            self.window, 
            text="CSV to SQL Database Converter",
            font=("Arial", 24, "bold"), 
            bg=self.current_theme['bg'], 
            fg=self.current_theme['title_color']
        )
        self.title_label.pack(pady=0)
        
        # Register as special widget
        self.register_special_widget(self.title_label, 'title')
        
        # Subtitle
        self.subtitle_label = tk.Label(
            self.window,
            text="Convert your CSV files to SQLite databases with ease",
            font=("Arial", 12),
            bg=self.current_theme['bg'],
            fg=self.current_theme['subtitle_color']
        )
        self.subtitle_label.pack(pady=(10, 20))
        
        # Register as special widget
        self.register_special_widget(self.subtitle_label, 'subtitle')

    def create_status_section(self):
        """Create status display section"""
        status_frame = tk.Frame(self.window, bg=self.current_theme['bg'])
        status_frame.pack(pady=20, padx=40, fill='x')
        
        self.status_title = tk.Label(
            status_frame,
            text="Current Status:",
            font=("Arial", 12, "bold"),
            bg=self.current_theme['bg'],
            fg=self.current_theme['text']
        )
        self.status_title.pack(anchor='center')
        
        self.status_label = tk.Label(
            status_frame,
            text="Ready to convert CSV files",
            font=("Arial", 10),
            bg=self.current_theme['bg'],
            fg=self.current_theme['status_good'],
            justify='center'
        )
        self.status_label.pack(anchor='center', pady=(5, 0))
        
        # Register status label for dynamic coloring
        self.register_special_widget(self.status_label, 'status_dynamic')
        
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
            self.status_label.config(
                text=status_text, 
                fg=self.current_theme['status_info']
            )
            # Update special role for proper theming
            self.register_special_widget(self.status_label, 'status_info')
        else:
            self.status_label.config(
                text="Ready to convert CSV files", 
                fg=self.current_theme['status_good']
            )
            # Update special role for proper theming
            self.register_special_widget(self.status_label, 'status_good')

    def create_action_buttons(self):
        """Create main action buttons"""
        button_frame = tk.Frame(self.window, bg=self.current_theme['bg'])
        button_frame.pack(pady=30)
        
        # Convert button
        self.convert_button = tk.Button(
            button_frame, 
            text="Start Conversion",
            command=self.open_conversion,
            font=("Arial", 16, "bold"), 
            width=20, 
            height=2, 
            bg=self.current_theme['convert_bg'],
            fg=self.current_theme['convert_fg'],
            cursor='hand2',
            relief='raised'
        )
        self.convert_button.pack(pady=(5, 20))
        ToolTip(self.convert_button, "Open the conversion wizard to convert CSV files to SQLite database")
        
        # Register as special widget
        self.register_special_widget(self.convert_button, 'convert')
    
        # Edit database button
        self.editdb_button = tk.Button(
            button_frame, 
            text="Database Tools",
            command=self.open_edit_database,
            font=("Arial", 16, 'bold'), 
            width=20, 
            height=2, 
            bg=self.current_theme['edit_bg'],
            fg=self.current_theme['edit_fg'],
            cursor='hand2',
        )
        self.editdb_button.pack(pady=10)
        ToolTip(self.editdb_button, "Database editing tools")
        
        # Register as special widget
        self.register_special_widget(self.editdb_button, 'edit')
    
    def create_terminate_button(self):
        """Create terminate button"""
        terminate_frame = tk.Frame(self.window, bg=self.current_theme['bg'])
        terminate_frame.pack(side='bottom', pady=20)
        
        self.terminate_button = tk.Button(
            terminate_frame, 
            text="Exit Application",
            command=self.safe_exit,
            font=("Arial", 14, 'bold'), 
            width=20, 
            height=2, 
            bg=self.current_theme['exit_bg'],
            fg=self.current_theme['exit_fg'],
            cursor='hand2'
        )
        self.terminate_button.pack(pady=10)
        ToolTip(self.terminate_button, "Close the application")
        
        # Register as special widget
        self.register_special_widget(self.terminate_button, 'exit')
    
    def on_theme_changed(self, new_theme):
        """Called when theme changes"""
        self.current_theme = new_theme
        
        # Update the main window background
        self.window.configure(bg=self.current_theme['bg'])
        
        # Apply theme to all widgets
        self.apply_theme()
        
        # Update theme button text
        self.theme_button.config(text=self.theme_manager.get_theme_button_text())
        
        # Re-apply status display colors
        self.update_status_display()
    
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
                
                # Close any open edit windows
                if self.edit_window and hasattr(self.edit_window, 'window'):
                    self.edit_window.window.destroy()
                    
            except:
                pass
            finally:
                # Unregister from theme callbacks
                self.theme_manager.unregister_theme_callback(self.on_theme_changed)
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
                    # Window was destroyed, clean up reference
                    self.conversion_window = None
            
            # Create new conversion window
            self.conversion_window = SetupPathsWindow(self.window)
            
            # Set up proper cleanup when window is closed
            def on_conversion_close():
                try:
                    if self.conversion_window:
                        # Unregister theme callback before destroying
                        if hasattr(self.conversion_window, 'theme_manager'):
                            self.conversion_window.theme_manager.unregister_theme_callback(
                                self.conversion_window.on_theme_changed
                            )
                        self.conversion_window = None
                        self.update_status_display()
                except Exception as e:
                    print(f"Error during conversion window cleanup: {e}")
            
            # Bind the cleanup to window close event
            self.conversion_window.window.protocol("WM_DELETE_WINDOW", on_conversion_close)
            
            # Update status when conversion window is closed
            self.window.after(1000, self.check_conversion_window)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open conversion window:\n{str(e)}")
    
    def check_conversion_window(self):
        """Check if conversion window is still open and update status"""
        try:
            if self.conversion_window and hasattr(self.conversion_window, 'window'):
                try:
                    # Check if window still exists
                    self.conversion_window.window.winfo_exists()
                    # Schedule next check
                    self.window.after(1000, self.check_conversion_window)
                except tk.TclError:
                    # Window was destroyed, clean up
                    self.conversion_window = None
                    self.update_status_display()
            else:
                # Window is closed, update status
                self.update_status_display()
        except Exception as e:
            # Clean up on any error
            self.conversion_window = None
            self.update_status_display()
    
    def open_edit_database(self):
        """Open database editing tools"""
        try:
            # Check if edit window is already open
            if self.edit_window and hasattr(self.edit_window, 'window'):
                try:
                    # Try to bring existing window to front
                    self.edit_window.window.lift()
                    self.edit_window.window.focus_set()
                    return
                except tk.TclError:
                    # Window was destroyed, clean up reference
                    self.edit_window = None
            
            # Create new edit window
            self.edit_window = editgui(self.window)
            
            # Set up proper cleanup when window is closed
            def on_edit_close():
                try:
                    if self.edit_window:
                        # Unregister theme callback before destroying
                        if hasattr(self.edit_window, 'theme_manager'):
                            self.edit_window.theme_manager.unregister_theme_callback(
                                self.edit_window.on_theme_changed
                            )
                        self.edit_window = None
                except Exception as e:
                    print(f"Error during edit window cleanup: {e}")
            
            # Bind the cleanup to window close event
            self.edit_window.window.protocol("WM_DELETE_WINDOW", on_edit_close)
            
            # Update status when edit window is closed
            self.window.after(1000, self.check_edit_window)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open edit window:\n{str(e)}")
    
    def check_edit_window(self):
        """Check if edit window is still open"""
        try:
            if self.edit_window and hasattr(self.edit_window, 'window'):
                try:
                    # Check if window still exists
                    self.edit_window.window.winfo_exists()
                    # Schedule next check
                    self.window.after(1000, self.check_edit_window)
                except tk.TclError:
                    # Window was destroyed, clean up
                    self.edit_window = None
            else:
                # Window is closed
                self.edit_window = None
        except Exception as e:
            # Clean up on any error
            self.edit_window = None
    
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