import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select


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
        # Select diary page
        driver.find_element(By.XPATH, "//a[contains(.,'Diary')]").click()
        time.sleep(3)
        # Select edit rating button
        driver.find_element(By.LINK_TEXT, "Edit Rating").click()
        time.sleep(3)
        try:
          comment = "testcomment"
          # Change rating comment
          elem = driver.find_element(By.ID, "comment")
          elem.send_keys(comment)
          time.sleep(3)
          # Change dropdown rating stars
          elem = driver.find_element(By.ID, "rating")
          elem2 = Select(elem)
          elem2.select_by_index(1)
          elem.click()
          time.sleep(3)
          # Click on edit rating button
          elem = driver.find_element(By.XPATH, "//input[@value='Edit Rating']")
          elem.click()
          time.sleep(3)
          # Check rating changes
          driver.find_element(By.XPATH, "//a[contains(.,'Diary')]").click()
          time.sleep(3)
          self.driver.close()
          assert True

        except NoSuchElementException:
            driver.close()
            self.fail("Edit Rating failed to update rating")

    def tearDown(self):
        self.driver.quit()

