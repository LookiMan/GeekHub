"""

Завдання: за допомогою браузера (Selenium) відкрити форму за наступним посиланням:
https://docs.google.com/forms/d/e/1FAIpQLScLhHgD5pMnwxl8JyRfXXsJekF8_pDG36XtSEwaGsFdU2egyw/viewform?usp=sf_link
заповнити і відправити її.
Зберегти два скріншоти: заповненої форми і повідомлення про відправлення форми.
В репозиторії скріншоти зберегти.
Корисні посилання:
https://www.selenium.dev/documentation/
https://chromedriver.chromium.org/downloads

"""
import os
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By


CHROMEDRIVER_PATH = "./src/chromedriver.exe"


class Robot(object):
    def __init__(self, wd):
        self.url = "https://docs.google.com/forms/d/e/1FAIpQLScLhHgD5pMnwxl8JyRfXXsJekF8_pDG36XtSEwaGsFdU2egyw/viewform"
        self.wd = wd
        self.output_path = Path(Path.cwd(), 'output')

    def start_robot(self):
        self.open_tab(self.url)
        self.fill_the_form("Владислав")
        self.screenshot_form("Filled form.png")
        self.submit_form()
        self.screenshot_form("Submited form.png")
        self.close_tab()
        return

    def open_tab(self, url):
        self.wd.get(url)
        return

    def close_tab(self):
        self.wd.close()
        return

    def fill_the_form(self, text):
        field = self.wd.find_element(By.CSS_SELECTOR, "input.exportInput")
        if field:
            field.send_keys(text)
        else:
            self.screenshot_form("Input field not found.png")
        return

    def submit_form(self):
        button = self.wd.find_element(By.CSS_SELECTOR, "span.exportLabel")
        if button:
            button.click()
        else:
            self.screenshot_form("Submit button not found.png")
        return

    def screenshot_form(self, filename):
        form = self.wd.find_element(By.CSS_SELECTOR, "div.exportFormCard")

        if not os.path.exists(self.output_path):
            os.mkdir(self.output_path)

        form.screenshot(str(self.output_path / filename))
        return


def main():
    options = webdriver.ChromeOptions()
    service = ChromeService(executable_path=CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=options)

    robot = Robot(driver)

    try:
        robot.start_robot()
    except Exception as exc:
        print(exc)
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
