# CSV to SQL Database Converter

A user-friendly desktop application that converts CSV files to SQLite databases with comprehensive database editing tools and dark mode support.

![Python](https://img.shields.io/badge/python-v3.7+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)

## ✨ Features

### 🔄 CSV Conversion
- **Smart CSV Detection**: Automatically detects CSV delimiters and encoding
- **Data Type Mapping**: Intelligent conversion of data types to appropriate SQLite types
- **Column Name Sanitization**: Automatically cleans column names for SQL compatibility
- **Large File Support**: Handles large CSV files with progress feedback
- **Error Handling**: Comprehensive error handling with detailed feedback

### 🗄️ Database Management
- **View Database**: Browse all tables and data in an intuitive interface
- **Table Operations**: Create, delete, and modify database tables
- **Record Management**: Add, edit, and delete individual records
- **Column Management**: Add and remove columns from existing tables
- **Data Validation**: Built-in validation for SQL names and data integrity

### 🎨 User Interface
- **Dark Mode Support**: Toggle between light and dark themes
- **Intuitive GUI**: Clean, modern interface built with tkinter
- **Tooltips**: Helpful tooltips throughout the application
- **Progress Feedback**: Real-time status updates and validation
- **Responsive Design**: Organized layout with proper window management

## 📋 Requirements

- Python 3.7 or higher
- Required Python packages:
  ```
  pandas
  sqlite3 (built-in)
  tkinter (built-in)
  numpy
  ```

## 🚀 Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/csv-sql-converter.git
   cd csv-sql-converter
   ```

2. **Install dependencies**:
   ```bash
   pip install pandas numpy
   ```

3. **Run the application**:
   ```bash
   python main_gui.py
   ```

## 📖 Usage

### Converting CSV to SQLite

1. **Launch the application** by running `main_gui.py`
2. **Click "Start Conversion"** to open the conversion wizard
3. **Select your CSV file** using the file browser
4. **Enter database name** (will be saved as .db file)
5. **Enter table name** for your data
6. **Choose save location** for the database file
7. **Click "Convert"** to create your SQLite database

### Database Management

1. **Click "Database Tools"** from the main menu
2. **View Database**: Browse your data in a tabbed interface
3. **Manage Tables**: Create new tables or delete existing ones
4. **Manage Records**: Add, edit, or delete individual records
5. **Manage Columns**: Add or remove columns from tables

### Theme Customization

- **Toggle Dark Mode**: Click the theme button (🌙/☀️) in any window
- **Persistent Settings**: Theme preference is maintained across sessions
- **Consistent Styling**: All windows automatically update when theme changes

## 🏗️ Architecture

The application follows a modular design pattern:

```
├── main_gui.py           # Main application window and entry point
├── convert_gui.py        # CSV conversion wizard interface
├── converter.py          # Core CSV to SQLite conversion logic
├── edit_gui.py          # Database editing tools interface
├── edit_sql.py          # Database manipulation operations
├── theme_manager.py     # Dark/light mode theme management
├── GUI_tooltip.py       # Tooltip functionality
└── globals.py           # Global variable management
```

## 🔧 Configuration

The application uses a global configuration system through `globals.py`:

- `CSV_PATH`: Path to the selected CSV file
- `DB_NAME`: Name of the SQLite database
- `DB_PATH`: Directory path for database storage
- `TABLE_NAME`: Name of the table in the database

## 🛡️ Error Handling

The application includes comprehensive error handling for:

- **File Access**: Permission errors, missing files, corrupted data
- **Data Validation**: Invalid characters, malformed CSV files
- **Database Operations**: SQL errors, connection issues, data integrity
- **UI Operations**: Window management, theme application

## 🎯 Key Features Explained

### Smart CSV Processing
- Automatically detects CSV delimiters (comma, tab, semicolon, pipe)
- Handles various text encodings (UTF-8, Latin-1, CP1252, ISO-8859-1)
- Preserves data types during conversion (integers, floats, text, dates)
- Sanitizes column names for SQL compatibility

### Database Editing Tools
- **Table Management**: Create tables with custom schemas, delete unwanted tables
- **Record Operations**: Full CRUD operations with column selection
- **Column Management**: Add columns with default values, remove columns safely
- **Data Viewing**: Tabbed interface showing all tables with scrollable data grids

### Theme System
- **Consistent Theming**: All windows automatically inherit theme changes
- **Special Widget Support**: Custom colors for buttons, status indicators, and titles
- **Dynamic Updates**: Theme changes apply immediately without restart

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 🐛 Known Issues

- SQLite column deletion requires table recreation (SQLite limitation)
- Very large CSV files (>100MB) may require additional processing time
- Theme changes require window refresh for some system-specific widgets

## 🔮 Future Enhancements

- [ ] Support for additional database formats (MySQL, PostgreSQL)
- [ ] Batch CSV processing
- [ ] Data export functionality
- [ ] Advanced data filtering and querying
- [ ] Plugin system for custom data transformations
- [ ] Configuration file for user preferences

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙋‍♀️ Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/yourusername/csv-sql-converter/issues) page
2. Create a new issue with detailed information
3. Include your Python version, operating system, and error messages

## 🎉 Acknowledgments

- Built with Python and tkinter
- Uses pandas for efficient data processing
- SQLite for lightweight database storage
- Inspired by the need for simple data conversion tools

---

**Made with ❤️ for data enthusiasts everywhere!**