import os
import sys

import allure
import pytest
from dotenv import load_dotenv

from Libraries.Logger import LogGen
from TestLibraries.UITestLib import UI
from TestLocator.Locator import Locator
from Utilities.YamlParser import YamlParser

sys.path.append("")


@pytest.mark.usefixtures("browser")
class TestCase:
    load_dotenv()
    Logger = LogGen.logger()
    yaml_parser = YamlParser.get_env_data()
    account_type = "Trail"
    url = yaml_parser['LINK']["{}".format(account_type)]
    username = os.getenv("login")
    password = os.getenv("password")

    def allureLogs(self):
        with allure.step(self):
            pass

    @pytest.mark.ui
    @pytest.mark.order(8)
    @pytest.mark.testsuite
    def test_verify_violations(self, browser):
        allure.dynamic.title("Verify Violations in UI")
        allure.dynamic.description("Navigate to the URL: <Platform URL>/ui/scans-list/repositories/<REPO_NAME>/scan"
                                   "-descendants\n "
                                   "Click on the uploaded image.\n"
                                   "From the left-hand pane, click on Policy Violations.\n"
                                   "Verify that the severity of the violations aligns with the policy rule (e.g.,"
                                   "only high and critical severity violations should appear if the policy is setfor "
                                   "high severity")
        allure.dynamic.link(self.url)
        page = UI(browser)
        page.test_validate_url(self.url)
        page.test_login(self.username, self.password)
        page.test_check_element_click("Platform", Locator.platform)
        page.test_check_element_click("Xray", Locator.xray)
        page.test_check_element_click("Scans list", Locator.scans_list)
        page.test_check_element_click("Repo name", Locator.repo_name)
        page.test_check_element_click("Uploaded image", Locator.uploaded_image)
        page.test_check_element_click("Policy_violations", Locator.policy_violations)
        page.check_violations()

        # try:
        #     browser.get(self.url)
        #     if self.url in browser.current_url:
        #         with allure.step("-- SUCCESS - Able validate url : {}".format(self.url)):
        #             self.Logger.info("-- SUCCESS - Able validate url : {}".format(self.url))
        #             allure.attach(browser.get_screenshot_as_png(), name="Passed_Url",
        #                           attachment_type=AttachmentType.PNG)
        #             assert True
        #     else:
        #         with allure.step("-- FAILED - Unable to validate url : {}".format(self.url)):
        #             self.Logger.error("-- FAILED - Unable to validate url : {}".format(self.url))
        #             assert False
        #
        #     selenium_helpers.wait_for_presence_check(browser, By.NAME, Locator.username)
        #     if selenium_helpers.is_element_present(browser, By.NAME, Locator.username, visible=True):
        #         selenium_helpers.send_keys_to_element(browser, By.NAME, Locator.username, self.username)
        #         selenium_helpers.send_keys_to_element(browser, By.NAME, Locator.password, self.password)
        #         selenium_helpers.click_element(browser, By.XPATH, Locator.login)
        #         with allure.step("-- SUCCESS - Able to Login Successfully"):
        #             self.Logger.info("-- SUCCESS - Able to Login Successfully")
        #             allure.attach(browser.get_screenshot_as_png(), name="Passed_Login",
        #                           attachment_type=AttachmentType.PNG)
        #             assert True
        #     else:
        #         with allure.step("-- FAILED - Unable to Login"):
        #             self.Logger.error("-- FAILED - Unable to Login")
        #             assert False
        #
        #     selenium_helpers.wait_for_presence_check(browser, By.XPATH, Locator.platform)
        #     if selenium_helpers.is_element_present(browser, By.XPATH, Locator.platform, visible=True):
        #         selenium_helpers.get_element(browser, By.XPATH, Locator.platform, click=True)
        #         with allure.step("-- SUCCESS - Able to Platform from Dashboard"):
        #             self.Logger.info("-- SUCCESS - Able to Platform from Dashboard")
        #             allure.attach(browser.get_screenshot_as_png(), name="Passed_Platform",
        #                           attachment_type=AttachmentType.PNG)
        #
        #         selenium_helpers.wait_for_presence_check(browser, By.XPATH, Locator.xray)
        #         selenium_helpers.get_element(browser, By.XPATH, Locator.xray, click=True)
        #         with allure.step("-- SUCCESS - xray"):
        #             self.Logger.info("-- SUCCESS - xray")
        #             allure.attach(browser.get_screenshot_as_png(), name="Passed_Platform",
        #                           attachment_type=AttachmentType.PNG)
        #
        #         selenium_helpers.wait_for_presence_check(browser, By.XPATH, Locator.scans_list)
        #         selenium_helpers.get_element(browser, By.XPATH, Locator.scans_list, click=True)
        #         with allure.step("-- SUCCESS - scans_list"):
        #             self.Logger.info("-- SUCCESS - scans_list")
        #             allure.attach(browser.get_screenshot_as_png(), name="Passed_Platform",
        #                           attachment_type=AttachmentType.PNG)
        #
        #         selenium_helpers.wait_for_presence_check(browser, By.XPATH, Locator.repo_name)
        #         selenium_helpers.get_element(browser, By.XPATH, Locator.repo_name, click=True)
        #         with allure.step("-- SUCCESS - repo_name"):
        #             self.Logger.info("-- SUCCESS - repo_name")
        #             allure.attach(browser.get_screenshot_as_png(), name="Passed_Platform",
        #                           attachment_type=AttachmentType.PNG)
        #
        #         selenium_helpers.wait_for_presence_check(browser, By.XPATH, Locator.uploaded_image)
        #         selenium_helpers.get_element(browser, By.XPATH, Locator.uploaded_image, click=True)
        #         with allure.step("-- SUCCESS - uploaded_image"):
        #             self.Logger.info("-- SUCCESS - uploaded_image")
        #             allure.attach(browser.get_screenshot_as_png(), name="Passed_Platform",
        #                           attachment_type=AttachmentType.PNG)
        #
        #         selenium_helpers.wait_for_presence_check(browser, By.XPATH, Locator.policy_violations)
        #         selenium_helpers.get_element(browser, By.XPATH, Locator.policy_violations, click=True)
        #         with allure.step("-- SUCCESS - policy_violations"):
        #             self.Logger.info("-- SUCCESS - policy_violations")
        #             allure.attach(browser.get_screenshot_as_png(), name="Passed_Platform",
        #                           attachment_type=AttachmentType.PNG)
        #
        #         time.sleep(10)
        #         check = browser.find_element(By.XPATH,Locator.check_total_violations).text
        #         self.Logger.info(f"**************** {check} **************")
        #         check = check.replace("Violations", "")
        #
        #         time.sleep(10)
        #         for i in range(int(check)):
        #             if browser.find_element(By.XPATH,"(//span[@class='el-tooltip display-label'][normalize-space("
        #                                              ")='Security_policy_1'])[{}]".format(i+1)).text == \
        #                     "Security_policy_1":
        #                 self.Logger.info("Able to verify ")
        #
        #         assert True
        #     else:
        #         with allure.step("-- FAILED - Unable to Login"):
        #             self.Logger.error("-- FAILED - Unable to Login")
        #             assert False
        #
        # except Exception as err:
        #     with allure.step("Exception during login please check logs for more details : {}".format(err)):
        #         self.Logger.error("Exception during login please check logs for more details : {}".format(err))
        #         allure.attach(browser.get_screenshot_as_png(), name="Failed_Login",
        #                       attachment_type=AttachmentType.PNG)
        #         assert False
