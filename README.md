# Web Automation Tool for SCM Portal

This automation tool helps in logging into the SCM Portal, solving CAPTCHAs, and uploading files automatically using Selenium WebDriver.

## Prerequisites

Before running the application, ensure you have the following installed:

- Python 3.x
- Tesseract OCR
  ```bash
  # For MacOS
  brew install tesseract
  
  # For Ubuntu/Debian
  sudo apt-get install tesseract-ocr
  
  # For Windows
  # Download installer from: https://github.com/UB-Mannheim/tesseract/wiki
  ```
- Chrome Browser
- ChromeDriver (automatically managed by webdriver-manager)

## Installation

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd <project-directory>
   ```

2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   
   # Activate virtual environment
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

1. Update the Tesseract path in `login.py` if different from default:
   ```python
   pytesseract.pytesseract.tesseract_cmd = '/opt/homebrew/bin/tesseract'  # Modify this path
   ```

2. Configure your user credentials in the `users` list at the bottom of `login.py`:
   ```python
   users = [
       {
           "username": "your_username",
           "password": "your_password",
           "file": "path_to_your_file.xlsx"
       }
   ]
   ```

## Usage

1. Place your Excel file (e.g., `SCMSample.xlsx`) in the project directory

2. Run the script:
   ```bash
   python login.py
   ```

The script will:
- Launch Chrome browser
- Log in to the portal
- Solve the CAPTCHA automatically
- Navigate to the upload section
- Upload the specified file
- Log out automatically

## Features

- Automated login with CAPTCHA solving
- File upload automation
- Multi-user support
- Detailed logging
- Error handling and recovery
- Automatic ChromeDriver management

## Logging

The application provides detailed logging information during execution. Logs include:
- Login status
- Navigation steps
- File upload progress
- Error messages (if any)

## Troubleshooting

If you encounter issues:

1. Check if Tesseract is properly installed and the path is correct
2. Ensure Chrome browser is installed
3. Verify internet connectivity
4. Check if the portal is accessible
5. Verify file paths and permissions
6. Check the logs for detailed error messages

## Dependencies

- selenium
- opencv-python
- pytesseract
- webdriver_manager
- logging




