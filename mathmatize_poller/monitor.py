import random
import time
import asyncio

from selenium.webdriver.common.by import By
from selenium.common.exceptions import  NoSuchElementException

class PollMonitor:
    def __init__(self, driver, url, update_handler, duration, frequency, frequency_k, fail_handler=None) -> None:
        self.driver = driver
        self.url = url
        self.duration = duration
        self.update_handler = update_handler
        self.fail_handler = fail_handler

        self.frequency = frequency
        self.frequency_k = frequency_k
        self.running = False

    def is_time_ended(self, start_time, duration):
        current_time = time.monotonic()
        end_time = start_time + duration
        return current_time >= end_time


    async def _check_for_updates(self):
        print ('Initializing monitor loop.')
        while (self.running and not self.is_time_ended(self.start_time, self.duration)):
            if (self.is_submit_present()):
                self.update_handler()
            elif (self.fail_handler):
                self.fail_handler()
                

            randomized_freq = self.frequency + random.uniform(-self.frequency_k, self.frequency_k)
            await asyncio.sleep(randomized_freq - ((time.monotonic() - self.start_time) % randomized_freq))

    def is_submit_present(self):
        self.driver.get(self.url)

        try:
            _class = 'poller-identified'
            el = self.driver.find_element(By.XPATH, f"//button[text()='Submit' and not(contains(@class, '.{_class}'))]")
            self.driver.execute_script(f"arguments[0].classList.add('.{_class}');", el)

            return True
        except NoSuchElementException:
            return False

    def start(self):
        if not self.running:
            print ('Starting monitor...')
            self.start_time = time.monotonic()
            self.running = True
            asyncio.create_task(self._check_for_updates())


    def stop(self):
        """Graceful shutdown. Runs once last time."""
        if not self.running:
            print ('Stopping monitor...')
            self.running = False