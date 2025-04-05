import pytest
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from Utilities.YamlParser import YamlParser

yaml_parser = YamlParser.get_env_data()
account_type = "Trail"
url = yaml_parser['LINK']["{}".format(account_type)]


@pytest.fixture(scope="session")
def api_base_url():
    return url


@pytest.fixture(scope="session")
def api_client():
    """ API Fixtures"""
    session = requests.Session()
    session.headers.update({
        "Content-Type": "application/json"
    })
    return session


@pytest.fixture(scope="class")
def browser():
    """ UI Fixtures"""
    options = Options()
    options.add_argument("--headless")  # Comment this for visible browser
    options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()
