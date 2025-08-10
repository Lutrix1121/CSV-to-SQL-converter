"""
Theme Manager Module for GUI Applications
Provides dark/light mode theming functionality that can be applied to any tkinter window.
"""

import tkinter as tk

class ThemeManager:
    """Manages theme switching and application for GUI windows"""
    
    def __init__(self):
        self.is_dark_mode = False
        self.themes = {
            'light': {
                'bg': 'white',
                'text': 'black',
                'button_bg': 'lightblue',
                'button_fg': 'black',
                'title_color': 'navy',
                'subtitle_color': 'gray',
                'status_good': 'green',
                'status_info': 'blue',
                'status_error': 'red',
                'status_warning': 'orange',
                'convert_bg': 'lightgreen',
                'convert_fg': 'darkgreen',
                'edit_bg': 'lightblue',
                'edit_fg': 'darkblue',
                'exit_bg': 'red',
                'exit_fg': 'white',
                'theme_button_bg': '#2c2c2c',
                'theme_button_fg': 'white',
                'entry_bg': 'white',
                'entry_fg': 'black',
                'frame_bg': 'white',
                'disabled_bg': 'lightgray',
                'disabled_fg': 'gray'
            },
            'dark': {
                'bg': '#2c2c2c',
                'text': 'white',
                'button_bg': '#404040',
                'button_fg': 'white',
                'title_color': '#87CEEB',
                'subtitle_color': '#B0B0B0',
                'status_good': '#90EE90',
                'status_info': '#87CEEB',
                'status_error': '#FF6B6B',
                'status_warning': '#FFD700',
                'convert_bg': '#228B22',
                'convert_fg': 'white',
                'edit_bg': '#4682B4',
                'edit_fg': 'white',
                'exit_bg': '#DC143C',
                'exit_fg': 'white',
                'theme_button_bg': 'white',
                'theme_button_fg': 'black',
                'entry_bg': '#404040',
                'entry_fg': 'white',
                'frame_bg': '#2c2c2c',
                'disabled_bg': '#555555',
                'disabled_fg': '#888888'
            }
        }
        
        self.current_theme = self.themes['light'].copy()
        self.theme_callbacks = []  # Store callbacks to notify when theme changes
    
    def get_current_theme(self):
        """Get the current theme dictionary"""
        return self.current_theme.copy()
    
    def get_theme_name(self):
        """Get current theme name"""
        return 'dark' if self.is_dark_mode else 'light'
    
    def toggle_theme(self):
        """Toggle between light and dark mode"""
        self.is_dark_mode = not self.is_dark_mode
        theme_name = 'dark' if self.is_dark_mode else 'light'
        self.current_theme = self.themes[theme_name].copy()
        
        # Notify all registered callbacks
        for callback in self.theme_callbacks:
            try:
                callback(self.current_theme)
            except Exception as e:
                print(f"Error in theme callback: {e}")
    
    def register_theme_callback(self, callback):
        """Register a callback to be called when theme changes"""
        self.theme_callbacks.append(callback)
    
    def unregister_theme_callback(self, callback):
        """Unregister a theme callback"""
        if callback in self.theme_callbacks:
            self.theme_callbacks.remove(callback)
    
    def get_theme_button_text(self):
        """Get appropriate text for theme toggle button"""
        return "🌙 Dark Mode" if not self.is_dark_mode else "☀️ Light Mode"
    
    def apply_theme_to_widget(self, widget, widget_type=None, special_role=None):
        """
        Apply current theme to a specific widget
        
        Args:
            widget: The tkinter widget to theme
            widget_type: Override widget class detection ('frame', 'label', 'button', 'entry')
            special_role: Special role for custom coloring ('title', 'subtitle', 'status_good', 
                         'status_error', 'convert', 'edit', 'exit', 'theme_toggle')
        """
        if not widget_type:
            widget_type = widget.winfo_class().lower()
        
        try:
            if widget_type == 'frame':
                widget.configure(bg=self.current_theme['bg'])
                
            elif widget_type == 'label':
                bg_color = self.current_theme['bg']
                
                if special_role == 'title':
                    fg_color = self.current_theme['title_color']
                elif special_role == 'subtitle':
                    fg_color = self.current_theme['subtitle_color']
                elif special_role == 'status_good':
                    fg_color = self.current_theme['status_good']
                elif special_role == 'status_info':
                    fg_color = self.current_theme['status_info']
                elif special_role == 'status_error':
                    fg_color = self.current_theme['status_error']
                elif special_role == 'status_warning':
                    fg_color = self.current_theme['status_warning']
                else:
                    fg_color = self.current_theme['text']
                
                widget.configure(bg=bg_color, fg=fg_color)
                
            elif widget_type == 'button':
                if special_role == 'convert':
                    bg_color = self.current_theme['convert_bg']
                    fg_color = self.current_theme['convert_fg']
                elif special_role == 'edit':
                    bg_color = self.current_theme['edit_bg']
                    fg_color = self.current_theme['edit_fg']
                elif special_role == 'exit':
                    bg_color = self.current_theme['exit_bg']
                    fg_color = self.current_theme['exit_fg']
                elif special_role == 'theme_toggle':
                    bg_color = self.current_theme['theme_button_bg']
                    fg_color = self.current_theme['theme_button_fg']
                else:
                    bg_color = self.current_theme['button_bg']
                    fg_color = self.current_theme['button_fg']
                
                widget.configure(bg=bg_color, fg=fg_color)
                
            elif widget_type == 'entry':
                widget.configure(
                    bg=self.current_theme['entry_bg'],
                    fg=self.current_theme['entry_fg'],
                    insertbackground=self.current_theme['text']  # Cursor color
                )
                
        except tk.TclError as e:
            # Some widgets might not support certain configure options
            print(f"Theme application warning for {widget}: {e}")
    
    def apply_theme_recursively(self, widget, special_widgets=None):
        """
        Recursively apply theme to a widget and all its children
        
        Args:
            widget: Root widget to start theming from
            special_widgets: Dict mapping widget objects to their special roles
        """
        if special_widgets is None:
            special_widgets = {}
        
        # Apply theme to current widget
        special_role = special_widgets.get(widget)
        self.apply_theme_to_widget(widget, special_role=special_role)
        
        # Recursively apply to children
        for child in widget.winfo_children():
            self.apply_theme_recursively(child, special_widgets)
    
    def create_theme_toggle_button(self, parent_frame, callback=None):
        """
        Create a theme toggle button
        
        Args:
            parent_frame: Parent frame to place the button in
            callback: Optional additional callback to run after theme toggle
        
        Returns:
            The created button widget
        """
        def toggle_with_callback():
            self.toggle_theme()
            if callback:
                callback()
        
        theme_button = tk.Button(
            parent_frame,
            text=self.get_theme_button_text(),
            command=toggle_with_callback,
            font=("Arial", 10),
            bg=self.current_theme['theme_button_bg'],
            fg=self.current_theme['theme_button_fg'],
            cursor='hand2',
            relief='flat',
            padx=5,
            pady=5
        )
        
        return theme_button


class ThemableWindow:
    """Mixin class that adds theming support to GUI windows"""
    
    def __init__(self, theme_manager=None):
        if theme_manager is None:
            self.theme_manager = ThemeManager()
        else:
            self.theme_manager = theme_manager
        
        self.special_widgets = {}  # Map widgets to their special roles
        
        # Register for theme updates
        self.theme_manager.register_theme_callback(self.on_theme_changed)
    
    def register_special_widget(self, widget, role):
        """Register a widget with a special theming role"""
        self.special_widgets[widget] = role
    
    def on_theme_changed(self, new_theme):
        """Called when theme changes - override in subclasses"""
        if hasattr(self, 'window'):
            self.apply_theme()
    
    def apply_theme(self):
        """Apply current theme to this window"""
        if hasattr(self, 'window'):
            self.theme_manager.apply_theme_recursively(self.window, self.special_widgets)
    
    def create_theme_toggle(self, parent_frame):
        """Create theme toggle button for this window"""
        return self.theme_manager.create_theme_toggle_button(
            parent_frame, 
            callback=lambda: self.apply_theme()
        )


# Singleton instance for application-wide theme management
app_theme_manager = ThemeManager()


def get_app_theme_manager():
    """Get the application's global theme manager"""
    return app_theme_manager
