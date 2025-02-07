import os
import time
import cv2
import pytesseract
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import logging
from selenium.common.exceptions import TimeoutException
from dotenv import load_dotenv

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class CaptchaSolver:
    pytesseract.pytesseract.tesseract_cmd = '/opt/homebrew/bin/tesseract'

    @staticmethod
    def solve(captcha_element):
        captcha_element.screenshot("captcha_image.png")
        img = cv2.imread('captcha_image.png')
        captcha_text = pytesseract.image_to_string(img, config='--psm 6')
        captcha_text = ''.join(char for char in captcha_text if char.isdigit() or char == '+')
        return sum(int(number) for number in captcha_text.split('+'))

class BrowserAutomation:
    def __init__(self, file_path, url):
        load_dotenv()  # Load environment variables from .env file
        self.username = os.getenv('SCM_USERNAME')
        self.password = os.getenv('SCM_PASSWORD')
        self.file_path = file_path
        self.url = url
        self.driver = self._init_driver()
    
    def _init_driver(self):
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        driver.get(self.url)
        return driver
    
    def login(self):
        try:
            self.driver.find_element(By.ID, "txtUserName").send_keys(self.username) # type: ignore
            self.driver.find_element(By.ID, "txtPwd").send_keys(self.password) # type: ignore
            captcha_element = self.driver.find_element(By.ID, "Captcha1_imgCtrl")
            captcha_solution = CaptchaSolver.solve(captcha_element)
            self.driver.find_element(By.ID, "txtCaptcha").send_keys(str(captcha_solution))
            self.driver.find_element(By.ID, "BtnLogin").click()
            time.sleep(2)
            print("Login successful.")
            return True
        except Exception as e:
            print(f"Login failed: {e}")
            return False
    
    def upload_file(self):
        try:
            self._navigate_to_upload_section()
            time.sleep(3)
            
            iframes = self.driver.find_elements(By.TAG_NAME, "iframe")
            logger.info(f"Found {len(iframes)} iframes")
            for idx, iframe in enumerate(iframes):
                logger.info(f"iframe {idx} id: {iframe.get_attribute('id')}")
                logger.info(f"iframe {idx} name: {iframe.get_attribute('name')}")
                #logger.info(f"iframe {idx} src: {iframe.get_attribute('src')}")
                logger.info("---")

            iframe = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "Frame0"))
            )
            logger.info("Found Frame0, switching to it")
            self.driver.switch_to.frame("Frame0")
            
            logger.info("Looking for file input element")
            file_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "WizardImport_FileUpload1"))
            )
            logger.info("Found file input element")
            
            file_path = self.file_path
            if not file_path:
                print(f"No file found for username {self.username}")
                return False
            logger.info(f"File path to upload: {os.path.abspath(file_path)}")
            file_input.send_keys(os.path.abspath(file_path))
            logger.info("Sent file path to input")
            
            logger.info("Looking for import button")
            import_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "WizardImport_btnImportFile"))
            )
            logger.info("Found import button, clicking it")
            import_button.click()
            logger.info("Clicked import button")
            
            try:
                logger.info("Waiting for upload confirmation")
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.ID, "WizardImport_lblMessage"))
                )
                logger.info("Upload confirmation found")
                
                #logger.info("Current page source after upload:")
                #logger.info(self.driver.page_source)
                
            except TimeoutException:
                logger.error("Upload confirmation not found")
            
            self.driver.switch_to.default_content()
            return True
            
        except Exception as e:
            logger.error(f"Upload failed with error: {str(e)}")
            logger.error(f"Current URL: {self.driver.current_url}")
            logger.error(f"Page source at error:")
            #logger.error(self.driver.page_source)
            self.driver.switch_to.default_content()
            return False
    
    def logout(self):
        try:
            self.driver.switch_to.default_content()
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "Navigation1_lnkbtnLogOut"))).click()
            print("Logout successful.")
        except Exception as e:
            print(f"Logout failed: {e}")
        finally:
            self.driver.quit()
    
    def run(self):
        if self.login():
            if self.upload_file():
                self.logout()
            else:
                print("Upload failed, skipping logout.")
                self.driver.quit()

    def _navigate_to_upload_section(self) -> None:
        try:
            logger.info("Starting navigation to upload section")
            
            transaction_link = self.driver.find_element(By.ID, "Navigation1_ulTransaction")
            logger.info("Found transaction menu")
            transaction_link.click()
            logger.info("Clicked transaction menu")
            
            time.sleep(3)  # Wait for menu to expand
            
            multiple_sales_link = self.driver.find_element(By.ID, "Navigation1_lnkbtnDispMultipleEntry")
            logger.info("Found multiple sales entry link")
            multiple_sales_link.click()
            logger.info("Clicked multiple sales entry")
            
            time.sleep(3)  # Wait for page load
            logger.info(f"Current URL after navigation: {self.driver.current_url}")
            
        except Exception as e:
            logger.error(f"Navigation failed: {str(e)}")
            logger.error(f"Current URL: {self.driver.current_url}")
            raise

    def handle_upload_workflow(self, username: str) -> bool:
        try:
            self._navigate_to_upload_section()
            time.sleep(3)
            
            iframes = self.driver.find_elements(By.TAG_NAME, "iframe")
            logger.info("Checking available iframes")

            iframe = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "Frame0"))
            )
            logger.info("Found Frame0, switching to it")
            self.driver.switch_to.frame("Frame0")
            
            logger.info("Looking for file input element")
            file_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "WizardImport_FileUpload1"))
            )
            logger.info("Found file input element")
            
            file_path = self.file_path
            logger.info("Uploading file")
            file_input.send_keys(os.path.abspath(file_path))
            logger.info("File selected successfully")
            
            logger.info("Looking for import button")
            import_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "WizardImport_btnImportFile"))
            )
            logger.info("Found import button")
            import_button.click()
            logger.info("Clicked import button")
            
            try:
                logger.info("Waiting for upload confirmation")
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.ID, "WizardImport_lblMessage"))
                )
                logger.info("Upload completed successfully")
                
            except TimeoutException:
                logger.error("Upload confirmation not found")
            
            self.driver.switch_to.default_content()
            return True
            
        except Exception as e:
            logger.error(f"Upload failed: {str(e)}")
            self.driver.switch_to.default_content()
            return False
        

if __name__ == "__main__":
    url = "https://scmexcise.mahaonline.gov.in/retailer/"
    file_path = "SCMSample.xlsx"
    
    bot = BrowserAutomation(file_path=file_path, url=url)
    bot.run()
