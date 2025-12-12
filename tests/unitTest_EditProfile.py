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
        driver.find_element(By.XPATH, "//li[@class='dropdown' and contains(., 'Account')]").click()
        time.sleep(3)
        driver.find_element(By.XPATH, "//a[contains(., 'Profile')]").click()
        time.sleep(3)
        driver.find_element(By.XPATH, "//a[contains(., 'Edit Profile')]").click()
        time.sleep(3)
        try:
            # Try to find the *currently* selected avatar
            currently_selected = driver.find_element(By.CSS_SELECTOR, "img.avatar-option.selected")
            current_filename = currently_selected.get_attribute("data-avatar-filename")
        except NoSuchElementException:
            current_filename = None  # No avatar is selected
        if current_filename == 'avatar8.jpg':
            driver.find_element(By.CSS_SELECTOR, "img.avatar-option[data-avatar-filename='avatar7.jpg']").click()
        else:
            driver.find_element(By.CSS_SELECTOR, "img.avatar-option[data-avatar-filename='avatar8.jpg']").click()
        time.sleep(3)
        driver.find_element(By.XPATH, "//button[contains(., 'Update Profile')]").click()
        time.sleep(3)
        try:
            avatar_elem = driver.find_element(By.CLASS_NAME, "avatar-image")
            avatar_elem_src = avatar_elem.get_attribute("src")
            #Since current_filename is the previous avatar, I must check for the new filename.
            if current_filename == 'avatar8.jpg':
                self.assertIn("avatar7", avatar_elem_src)
                self.driver.close()
                assert True
            else:
                self.assertIn("avatar8", avatar_elem_src)
                self.driver.close()
                assert True
        except NoSuchElementException:
            driver.close()
            self.fail("The avatar was not successfully updated.")

        time.sleep(3)

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
