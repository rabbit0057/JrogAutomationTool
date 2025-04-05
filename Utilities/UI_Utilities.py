from selenium.common.exceptions import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class SeleniumHelpers:
    def __init__(self, driver):
        self.driver = driver

    #
    def click_element(self, driver, by: By, locator: str, timeout=10):
        """ Wait until the element is clickable and then click """
        element = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((by, locator))
        )
        element.click()

    def send_keys_to_element(self, driver, by: By, locator: str, text: str, clear_first=True, timeout=10):
        """ Wait for input field, optionally clear, and send keys """
        element = WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located((by, locator))
        )
        if clear_first:
            element.clear()
        element.send_keys(text)

    def is_element_present(self, driver, by: By, locator: str, visible: bool = False, timeout=5) -> bool:
        """
        Returns True if element is present in DOM.
        If visible=True, checks visibility as well.
        """
        try:
            if visible:
                WebDriverWait(driver, timeout).until(
                    EC.visibility_of_element_located((by, locator))
                )
            else:
                driver.find_element(by, locator)
            return True
        except (NoSuchElementException, TimeoutException):
            return False

    def wait_for_presence_check(self, driver, by: By, locator: str, timeout=200):
        """
        Waits for element to be present in DOM (not necessarily visible).
        Returns the WebElement if found.
        """
        try:
            element = WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located((by, locator))
            )
            return element
        except TimeoutException:
            raise AssertionError(f"Element not present: {locator} using {by}")

    def get_element(self, driver, by: By, locator: str, visible: bool = True, click: bool = False, timeout=10):
        """
        Waits for an element and returns it.
        If click=True, clicks the element before returning.
        """
        try:
            if visible:
                element = WebDriverWait(driver, timeout).until(
                    EC.visibility_of_element_located((by, locator))
                )
            else:
                element = WebDriverWait(driver, timeout).until(
                    EC.presence_of_element_located((by, locator))
                )

            if click:
                element.click()

            return element

        except TimeoutException:
            raise AssertionError(f"Element not found (visible={visible}): {locator} using {by}")

    def get_text(self, driver, by: By, locator: str, timeout=10):
        """ Wait until the element is clickable and then click """
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, locator))
        )
        element.text

    def getByType(self, locatorType):
        locatorType = locatorType.lower()
        if locatorType == "id":
            return By.ID
        elif locatorType == "name":
            return By.NAME
        elif locatorType == "css":
            return By.CSS_SELECTOR
        elif locatorType == "class":
            return By.CLASS_NAME
        elif locatorType == "link":
            return By.LINK_TEXT
        else:
            self.Logger.info("Locator type " + locatorType + "not correct/supported")

    def waitForPresenceCheck(self, driver, locator, locatorType="xpath", timeout=10, pollFrequency=0.5):
        element = None
        try:
            byType = self.getByType(locatorType)
            wait = WebDriverWait(driver, timeout, pollFrequency=pollFrequency,
                                 ignored_exceptions=[NoSuchElementException,
                                                     ElementNotVisibleException,
                                                     ElementNotVisibleException])
            element = wait.until(EC.presence_of_element_located((byType, locator)))
        except:
            return element

    def getElement(self, driver, locator, locatorType="xpath"):
        element = None
        try:
            locatorType = locatorType.lower()
            byType = self.getByType(locatorType)
            element = driver.find_element(byType, locator)
        except:
            return element

    def isElementPresent(self, locator, locatorType="xpath"):
        try:
            element = self.getElement(locator, locatorType)
            if element is not None:
                return True
            else:
                return False
        except:
            return False

    def sendKeys(self, data, locator, locatorType="xpath"):
        try:
            element = self.getElement(locator, locatorType)
            element.send_keys(data)
        except:
            a = 1
