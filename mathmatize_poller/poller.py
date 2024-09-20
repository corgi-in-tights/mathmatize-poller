import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent # sus

from .monitor import PollMonitor
from .utils import get_web_element

class MathMatizePoller:
    def __init__(self, chromedriver_path, email, password) -> None:
        options = self.__create_options()
        self.__setup_web_driver(chromedriver_path, options)
        self._sign_in(email, password)

        self.monitor = None

    def __create_options(self):
        options = Options()
        user_agent = UserAgent().random
        options.add_argument(f'user-agent={user_agent}')
        return options

    def __setup_web_driver(self, chromedriver_path, options):
        if (chromedriver_path):
            self.service = Service(chromedriver_path)
            self.service.start()
            self.driver = webdriver.Chrome(service=self.service, options=options)
        else:
            self.driver = webdriver.Chrome(options=options)

        print ('Created web driver.')

    def _sign_in(self, email, password):
        self.driver.get('https://www.mathmatize.com/account/')

        get_web_element(
            self.driver, 
            EC.visibility_of_element_located, 
            "//input[@id='input-email']"
        ).send_keys(email)

        get_web_element(
            self.driver, 
            EC.visibility_of_element_located, 
            "//input[@id='input-password']"
        ).send_keys(password)

        time.sleep(0.5) # wait for inputs to fully register

        get_web_element(
            self.driver,
            EC.element_to_be_clickable,
            "//button[text()='SIGN IN' and contains(@class, 'mui-style-1fky9ur')]"
        ).click()

        get_web_element(
            self.driver,
            EC.visibility_of_element_located,
            "//button[text()='Sign Out']"
        )

        print ('Succesfully signed in.')

    def get_or_create_monitor(self, url, update_handler, duration, frequency, k=1.5, fail_handler=None):
        if not self.monitor:
            self.monitor = PollMonitor(self.driver, url, update_handler, duration, frequency, frequency_k=k, fail_handler=fail_handler)
            return self.monitor
        return self.monitor

        
    def close(self):
        print (f'Shutting down poller (and attached monitor).')
        if self.monitor:
            self.monitor.stop()
        self.driver.quit()



