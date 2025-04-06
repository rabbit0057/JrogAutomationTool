import time

import allure
from allure_commons.types import AttachmentType
from selenium.webdriver.common.by import By

from Libraries.Logger import LogGen
from TestLocator.Locator import Locator
from Utilities.UI_Utilities import SeleniumHelpers


class UI(SeleniumHelpers):
    Logger = LogGen.logger()

    def __init__(self, driver):
        self.driver = driver
        self.helper = SeleniumHelpers(driver)

    def test_validate_url(self, url):
        try:
            self.driver.get(url)
            if url in self.driver.current_url:
                with allure.step("-- SUCCESS - Able validate to url : {}".format(url)):
                    self.Logger.info("-- SUCCESS - Able validate to url : {}".format(url))
                    allure.attach(self.driver.get_screenshot_as_png(), name="Passed_Url",
                                  attachment_type=AttachmentType.PNG)
                    assert True
            else:
                with allure.step("-- FAILED - Unable to validate url : {}".format(url)):
                    self.Logger.error("-- FAILED - Unable to validate url : {}".format(url))
                    assert False
        except Exception as err:
            with allure.step("Exception during login please check logs for more details : {}".format(err)):
                self.Logger.error("Exception during login please check logs for more details : {}".format(err))
                allure.attach(self.driver.get_screenshot_as_png(), name="Failed_Login",
                              attachment_type=AttachmentType.PNG)
                assert False

    def test_login(self, username, password):
        try:
            self.helper.wait_for_presence_check(self.driver, By.NAME, Locator.username)
            if self.helper.is_element_present(self.driver, By.NAME, Locator.username, visible=True):
                self.helper.send_keys_to_element(self.driver, By.NAME, Locator.username, username)
                self.helper.send_keys_to_element(self.driver, By.NAME, Locator.password, password)
                self.helper.click_element(self.driver, By.XPATH, Locator.login)
                with allure.step("-- SUCCESS - Able to Login Successfully"):
                    self.Logger.info("-- SUCCESS - Able to Login Successfully")
                    allure.attach(self.driver.get_screenshot_as_png(), name="Passed_Login",
                                  attachment_type=AttachmentType.PNG)
                    assert True
            else:
                with allure.step("-- FAILED - Unable to Login"):
                    self.Logger.error("-- FAILED - Unable to Login")
                    assert False
        except Exception as err:
            with allure.step("Exception during login please check logs for more details : {}".format(err)):
                self.Logger.error("Exception during login please check logs for more details : {}".format(err))
                allure.attach(self.driver.get_screenshot_as_png(), name="Failed_Login",
                              attachment_type=AttachmentType.PNG)
                assert False

    def test_check_element_click(self, element_value, element_locator):
        try:
            self.helper.wait_for_presence_check(self.driver, By.XPATH, element_locator)
            if self.helper.is_element_present(self.driver, By.XPATH, element_locator, visible=True):
                self.helper.get_element(self.driver, By.XPATH, element_locator).click()
                with allure.step("-- SUCCESS - Navigate to {}".format(element_value)):
                    self.Logger.info("-- SUCCESS - Navigate to {}".format(element_value))
                    allure.attach(self.driver.get_screenshot_as_png(), name="Passed_{}".format(element_value),
                                  attachment_type=AttachmentType.PNG)
                    assert True
            else:
                with allure.step("-- FAILED - To Navigate - {}".format(element_value)):
                    self.Logger.error("-- FAILED - To Navigate - {}".format(element_value))
                    assert False
        except Exception as err:
            with allure.step("Exception during login please check logs for more details : {}".format(err)):
                self.Logger.error("Exception during login please check logs for more details : {}".format(err))
                allure.attach(self.driver.get_screenshot_as_png(), name="Failed_Login",
                              attachment_type=AttachmentType.PNG)
                assert False

    def check_violations(self):
        try:
            self.helper.wait_for_presence_check(self.driver, By.XPATH, Locator.violations_filter)
            if self.helper.is_element_present(self.driver, By.XPATH, Locator.violations_filter, visible=True):
                self.helper.get_element(self.driver, By.XPATH, Locator.violations_filter).click()
                with allure.step("-- SUCCESS - Navigate to Violations Filter"):
                    self.Logger.info("-- SUCCESS - Navigate to Violations Filter")
                    allure.attach(self.driver.get_screenshot_as_png(), name="Passed_Violation_Filter",
                                  attachment_type=AttachmentType.PNG)
                time.sleep(10)
                self.helper.wait_for_presence_check(self.driver, By.XPATH, Locator.check_total_violations)
                check_total_violations = self.driver.find_element(By.XPATH, Locator.check_total_violations).text
                extract_check_total_violations = check_total_violations.replace("Violations", "")
                self.helper.wait_for_presence_check(self.driver, By.XPATH, Locator.severity_risk)
                self.helper.get_element(self.driver, By.XPATH, Locator.severity_risk).click()
                time.sleep(10)
                critical = self.driver.find_element(By.XPATH, Locator.critical).text
                high = self.driver.find_element(By.XPATH, Locator.high).text
                medium = self.driver.find_element(By.XPATH, Locator.medium).text
                low = self.driver.find_element(By.XPATH, Locator.low).text
                unknown = self.driver.find_element(By.XPATH, Locator.unknown).text
                self.Logger.info("****** {} {} {} {} {} {} ****".format(critical, high, medium, low, unknown,
                                                                        extract_check_total_violations))

                if int(medium) and int(low) and int(unknown) > 0:
                    with allure.step("-- FAILED - Only high and critical severity violations should appear if the "
                                     "policy is set for high severity"):
                        self.Logger.error("-- FAILED - Only high and critical severity violations should appear if the "
                                          "policy is set for high severity")
                        allure.attach(self.driver.get_screenshot_as_png(), name="Failed_Violations_UI",
                                      attachment_type=AttachmentType.PNG)
                        assert False
                elif int(extract_check_total_violations) == int(critical) + int(high):
                    with allure.step("-- SUCCESS - Only high and critical severity violations should appear if the "
                                     "policy is set for high severity"):
                        self.Logger.error(
                            "-- SUCCESS - Only high and critical severity violations should appear if the "
                            "policy is set for high severity")
                        allure.attach(self.driver.get_screenshot_as_png(), name="Passed_Violations_UI",
                                      attachment_type=AttachmentType.PNG)
                        assert True
                else:
                    with allure.step("-- FAILED - To verify policy "):
                        self.Logger.error("-- FAILED - To verify policy")
                        assert False
            else:
                with allure.step("-- FAILED - To Validate Last Scan Status"):
                    self.Logger.error("-- FAILED - To Validate Last Scan Status")
                    assert False
        except Exception as err:
            with allure.step(
                    "Exception during Verify Violations in UI please check logs for more details : {}".format(err)):
                self.Logger.error(
                    "Exception during Verify Violations in UI please check logs for more details : {}".format(err))
                allure.attach(self.driver.get_screenshot_as_png(), name="Failed_Verify_Violations_UI",
                              attachment_type=AttachmentType.PNG)
                assert False
