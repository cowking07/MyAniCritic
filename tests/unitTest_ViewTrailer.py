import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By


class AC_ATS(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()

    def test_AC(self):
        driver = self.driver
        driver.maximize_window()
        user = 'testUser'
        pwd = 'AnimeForever'
        driver.get("http://127.0.0.1:8000")
        time.sleep(3)
        driver.find_element(By.XPATH, "//li[@class='dropdown' and contains(., 'Account')]").click()
        time.sleep(3)
        driver.find_element(By.XPATH, "//a[contains(., 'Login/Register')]").click()
        time.sleep(3)
        elem = driver.find_element(By.ID, "id_username")
        elem.send_keys(user)
        elem = driver.find_element(By.ID, "id_password")
        elem.send_keys(pwd)
        time.sleep(3)
        elem.send_keys(Keys.RETURN)
        time.sleep(3)

        # Access anime list
        driver.find_element(By.LINK_TEXT, "Movies & Animes").click()
        time.sleep(5)
        # Select Death Note title
        driver.find_element(By.LINK_TEXT, "Death Note").click()
        time.sleep(3)

        try:
        # Select watch trailer button
            driver.find_element(By.LINK_TEXT, "▶ Watch Trailer").click()
            self.driver.close()
            assert True

        except NoSuchElementException:
            driver.close()
            self.fail("Watch Trailer button not found")

        time.sleep(3)

    def tearDown(self):
        self.driver.quit()

if __name__ == '__main__':
    unittest.main()
