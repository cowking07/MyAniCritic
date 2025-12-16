import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select , WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class AC_ATS(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()

    def test_AC(self):
        driver = self.driver
        driver.maximize_window()
        wait = WebDriverWait(driver, 2)
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
            driver.find_element(By.XPATH, "//a[contains(text(), 'Add Rating')]").click()
            time.sleep(5)
            comment_box = wait.until(EC.element_to_be_clickable((By.ID, "comment")))
            comment_box.clear()
            comment_box.send_keys("this is ugly")
            time.sleep(3)
            rating_dropdown = Select(wait.until(EC.presence_of_element_located((By.ID, "rating"))))
            time.sleep(3)
            rating_dropdown.select_by_value("2")
            time.sleep(3)
            submit_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@type='submit' and @value='Add Rating']")))
            submit_btn.click()
            time.sleep(3)
            driver.find_element(By.LINK_TEXT, "Diary").click()
            time.sleep(5)
            # Wait for the diary review container to appear
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".rating-review")))

            diary_text = driver.find_element(By.TAG_NAME, "body").text.lower()

            # 1) The original bad word should NOT appear
            self.assertNotIn("ugly", diary_text)

            # 2) The masked version SHOULD appear (at least one star)
            self.assertIn("****", diary_text)

            self.driver.close()

            assert True

        except NoSuchElementException:
            driver.close()
            self.fail("Add Rating option not found.")
        time.sleep(3)

    def tearDown(self):
        self.driver.quit()


if __name__ == '__main__':
    unittest.main()