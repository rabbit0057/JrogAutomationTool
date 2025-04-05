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
