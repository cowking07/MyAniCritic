import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By


class AC_ATS(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()

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

        driver.find_element(By.LINK_TEXT, "Movies & Animes").click()
        time.sleep(5)
        driver.find_element(By.LINK_TEXT, "Samurai Champloo").click()
        time.sleep(3)

        try:
            driver.find_element(By.XPATH, "//a[.//img[contains(translate(@alt,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'youtube')]]").click()
            time.sleep(5)
            self.driver.close()
            assert True

        except NoSuchElementException:
            driver.close()
            self.fail("Streaming option not found.")
        time.sleep(3)

    def tearDown(self):
        self.driver.quit()

if __name__ == '__main__':
    unittest.main()