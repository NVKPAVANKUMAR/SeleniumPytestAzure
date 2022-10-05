import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture(scope="class")
def chrome_driver(request):
    options_obj = webdriver.ChromeOptions()
    options_obj.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])
    options_obj.add_experimental_option("excludeSwitches", ["enable-logging"])
    options_obj.add_experimental_option("excludeSwitches", ["enable-automation"])
    options_obj.add_argument("--disable-notifications")
    options_obj.add_argument('ignore-certificate-errors')
    options_obj.add_argument("--start-maximized")
    options_obj.add_argument('--headless')

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options_obj)
    driver.implicitly_wait(10)
    driver.maximize_window()
    request.cls.driver = driver
    yield
    driver.quit()


@pytest.mark.usefixtures("chrome_driver")
class BaseTest:
    pass


class TestOrangeHRM(BaseTest):
    def test_orangehrm_title(self):
        self.driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
        assert self.driver.title == 'OrangeHRM'
        assert self.driver.current_url

    def test_orangehrm_login(self):
        self.driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
        self.driver.find_element(By.NAME, "username").send_keys("Admin")
        self.driver.find_element(By.NAME, "password").send_keys("admin123")
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
