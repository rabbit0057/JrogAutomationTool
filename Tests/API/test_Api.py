import json
import os
import sys
import time
from datetime import datetime, timedelta

import allure
import docker
import pytest
import requests
from dotenv import load_dotenv

from Libraries.Logger import LogGen
from TestLocator.ApiEndPoint import ApiEndPoint
from Utilities.DataLoader import load_json
from Utilities.YamlParser import YamlParser

sys.path.append("")


@pytest.mark.usefixtures("api_client")
class TestCase:
    load_dotenv()
    Logger = LogGen.logger()
    yaml_parser = YamlParser.get_env_data()
    test_data = YamlParser.get_test_data()
    account_type = "Trail"
    url = yaml_parser['LINK']["{}".format(account_type)]
    artifactory_url = test_data['DOCKER_DATA']["{}".format("ARTIFACTORY_URL")]
    docker_repo = test_data['DOCKER_DATA']["{}".format("DOCKER_REPO")]
    source_image = test_data['DOCKER_DATA']["{}".format("SOURCE_IMAGE")]
    username = os.getenv("login")
    token = os.getenv("token")

    def allureLogs(self):
        with allure.step(self):
            pass

    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(token)
    }

    @pytest.mark.api
    @pytest.mark.api1
    @pytest.mark.testsuite
    @pytest.mark.order(1)
    def test_001(self, api_client, api_base_url):
        try:
            allure.dynamic.title("Create a Docker Repository")
            allure.dynamic.description("Use the Create Repository REST API to set up a Docker repository.")
            allure.dynamic.link(f"{api_base_url}{ApiEndPoint.create_docker_repo}")
            repo_config = load_json("TestParameter/repo_config.json")
            response = api_client.post(f"{self.url}{ApiEndPoint.create_docker_repo}", headers=self.headers,
                                       data=json.dumps(repo_config))
            if response.status_code == 200 or response.status_code == 201:
                with allure.step(
                        "-- SUCCESS - Docker repository created successfully! : {} - {}".format(response.status_code,
                                                                                                response.text)):
                    self.Logger.info(
                        "-- SUCCESS - Docker repository created successfully! : {} - {}".format(response.status_code,
                                                                                                response.text))
                allure.attach(str(response.status_code), name="Status Code",
                              attachment_type=allure.attachment_type.TEXT)
                allure.attach(str(repo_config), name="Payload", attachment_type=allure.attachment_type.TEXT)
                allure.attach(str(response.text), name="Response", attachment_type=allure.attachment_type.TEXT)
                assert True
            else:
                with allure.step("-- FAILED - To Create Docker repository : {} - {}".format(response.status_code,
                                                                                            response.text)):
                    self.Logger.error(
                        "-- FAILED - To Create Docker repository : {} - {}".format(response.status_code, response.text))
                    assert False
        except Exception as err:
            with allure.step(
                    "Exception during Create a Docker Repository please check logs for more details : {}".format(err)):
                self.Logger.error(
                    "Exception during Create a Docker Repository please check logs for more details : {}".format(err))
                allure.attach(str(response.status_code), name="Status Code",
                              attachment_type=allure.attachment_type.TEXT)
                allure.attach(str(repo_config), name="Payload", attachment_type=allure.attachment_type.TEXT)
                allure.attach(str(response.text), name="Response", attachment_type=allure.attachment_type.TEXT)
                assert False

    @pytest.mark.api2
    @pytest.mark.api
    @pytest.mark.testsuite
    @pytest.mark.order(2)
    def test_002(self, api_client, api_base_url):
        try:
            allure.dynamic.title("Verify Repository Creation")
            allure.dynamic.description(
                "Use the Get Repository REST API to confirm the repository was created successfully")
            allure.dynamic.link(f"{self.url}{ApiEndPoint.verify_docker_repo}")
            response = api_client.get(f"{self.url}{ApiEndPoint.verify_docker_repo}", headers=self.headers)
            data = response.json()
            if response.status_code == 200:
                for key in data:
                    if key['key'] == "docker-local":
                        with allure.step(
                                "-- SUCCESS - Able to validate Repository : {} *** Status Code : {}".format(key['key'],
                                                                                                            response.status_code)):
                            self.Logger.info(
                                "-- SUCCESS - Able to validate Repository : {} *** Status Code : {}".format(key['key'],
                                                                                                            response.status_code))
                        allure.attach(str(response.status_code), name="Status Code",
                                      attachment_type=allure.attachment_type.TEXT)
                        allure.attach(str(response.text), name="Response",
                                      attachment_type=allure.attachment_type.TEXT)
                        assert True
                        break
                    else:
                        with allure.step(
                                "-- FAILED - To validate Repository : {} *** Status Code : {}".format(key['key'],
                                                                                                      response.status_code)):
                            self.Logger.info(
                                "-- FAILED - To validate Repository : {} *** Status Code : {}".format(key['key'],
                                                                                                      response.status_code))
                        allure.attach(str(response.status_code), name="Status Code",
                                      attachment_type=allure.attachment_type.TEXT)
                        allure.attach(str(response.text), name="Response",
                                      attachment_type=allure.attachment_type.TEXT)
                        assert False
                        break
        except Exception as err:
            with allure.step(
                    "Exception during Verify Repository Creation please check logs for more details : {}".format(err)):
                self.Logger.error(
                    "Exception during Verify Repository Creation please check logs for more details : {}".format(err))
                allure.attach(str(response.status_code), name="Status Code",
                              attachment_type=allure.attachment_type.TEXT)
                allure.attach(str(response.text), name="Response", attachment_type=allure.attachment_type.TEXT)
                assert False

    @pytest.mark.api3
    @pytest.mark.api
    @pytest.mark.testsuite
    @pytest.mark.order(3)
    def test_003(self, api_client, api_base_url):
        try:
            allure.dynamic.title("Push a Docker Image:")
            allure.dynamic.description("Pull the Docker image alpine:3.9 \n"
                                       "Log in to your JFrog Platform using Docker CLI \n"
                                       "Tag and push the image to your newly created repository.")
            ARTIFACTORY_URL = self.artifactory_url
            DOCKER_REPO = self.docker_repo
            USERNAME = self.username
            API_KEY = self.token
            SOURCE_IMAGE = self.source_image
            TARGET_IMAGE = f"{ARTIFACTORY_URL}/{DOCKER_REPO}/alpine:3.9"

            client = docker.from_env()
            with allure.step(f"-- INFO - Pulling {SOURCE_IMAGE} from Docker Hub..."):
                self.Logger.info(f"-- INFO - Pulling {SOURCE_IMAGE} from Docker Hub...")

            client.images.pull(SOURCE_IMAGE)
            with allure.step(f"-- INFO - Successfully pulled {SOURCE_IMAGE}"):
                self.Logger.info(f"-- INFO - Successfully pulled {SOURCE_IMAGE}")

            with allure.step(f"-- INFO - Tagging image: {SOURCE_IMAGE} -> {TARGET_IMAGE}"):
                self.Logger.info(f"-- INFO - Tagging image: {SOURCE_IMAGE} -> {TARGET_IMAGE}")
            image = client.images.get(SOURCE_IMAGE)
            image.tag(TARGET_IMAGE)

            with allure.step(f"-- INFO - Pushing image to {TARGET_IMAGE}..."):
                self.Logger.info(f"-- INFO - Pushing image to {TARGET_IMAGE}...")
            push_result = client.images.push(TARGET_IMAGE, auth_config={'username': USERNAME, 'password': API_KEY})

            with allure.step(f"-- INFO - Push attempt completed, validating..."):
                self.Logger.info(f"-- INFO - Push attempt completed, validating...")

            validation_url = f"https://{ARTIFACTORY_URL}/ui/native/artifactory/{DOCKER_REPO}/alpine/3.9/manifest.json"
            headers = {"X-JFrog-Art-Api": API_KEY}

            time.sleep(5)

            response = requests.get(validation_url, headers=headers)

            if response.status_code == 200:
                with allure.step("-- SUCCESS -  Image successfully pushed to JFrog Artifactory"):
                    self.Logger.info("-- SUCCESS -  Image successfully pushed to JFrog Artifactory")
                assert True
            else:
                with allure.step("-- FAILED -  Image push failed! Verify repository and credentials."):
                    self.Logger.info("-- FAILED -  Image push failed! Verify repository and credentials.")
                assert False

        except docker.errors.APIError as e:
            self.Logger.info(f" -- FAILED - Docker API Error: {e}")
            assert False
        except requests.exceptions.RequestException as e:
            self.Logger.info(f" -- FAILED - JFrog API Error: {e}")
            assert False
        except Exception as e:
            self.Logger.info(f" -- FAILED - Unexpected Error: {e}")
            assert False

    @pytest.mark.api
    @pytest.mark.api4
    @pytest.mark.testsuite
    @pytest.mark.order(4)
    def test_004(self, api_client, api_base_url):
        try:
            allure.dynamic.title("Create a Security Policy")
            allure.dynamic.description("Use the Create Policy API to define a security policy with specific rules")
            allure.dynamic.link(f"{self.url}{ApiEndPoint.create_security_policy}")
            update_policies_name = "sec_policy_{}".format((datetime.now() + timedelta()).strftime('%y%m%d%a%H%M%S'))
            policies_config = {
                "name": "{}".format(update_policies_name),
                "description": "This is a specific CVEs security policy",
                "type": "security",
                "rules": [
                    {
                        "name": "some_rule",
                        "criteria": {
                            "malicious_package": False,
                            "fix_version_dependant": False,
                            "min_severity": "high"
                        },
                        "actions": {
                            "mails": [],
                            "webhooks": [],
                            "fail_build": False,
                            "block_release_bundle_distribution": False,
                            "block_release_bundle_promotion": False,
                            "notify_deployer": False,
                            "notify_watch_recipients": False,
                            "create_ticket_enabled": False,
                            "block_download": {
                                "active": False,
                                "unscanned": False
                            }
                        },
                        "priority": 1
                    }
                ]
            }
            response = api_client.post(f"{self.url}{ApiEndPoint.create_security_policy}", headers=self.headers,
                                       data=json.dumps(policies_config))
            if response.status_code == 200 or response.status_code == 201:
                with allure.step("-- SUCCESS - Policy has been successfully created  : {} - {}".format(
                        response.status_code,
                        response.text)):
                    self.Logger.info(
                        "-- SUCCESS - Policy has been successfully created : {} - {}".format(
                            response.status_code,
                            response.text))
                    allure.attach(str(response.status_code), name="Status Code",
                                  attachment_type=allure.attachment_type.TEXT)
                    allure.attach(str(policies_config), name="Payload", attachment_type=allure.attachment_type.TEXT)
                    allure.attach(str(response.text), name="Response", attachment_type=allure.attachment_type.TEXT)
                    assert True
            else:
                with allure.step(
                        "-- FAILED - To Create Policy : {} - {}".format(response.status_code, response.text)):
                    self.Logger.error(
                        "-- FAILED - To Create Policy : {} - {}".format(response.status_code, response.text))
                    assert False
        except Exception as err:
            with allure.step(
                    "Exception during Create a Security Policy please check logs for more details : {}".format(
                        err)):
                self.Logger.error(
                    "Exception during Create a Security Policy please check logs for more details : {}".format(
                        err))
                allure.attach(str(response.status_code), name="Status Code",
                              attachment_type=allure.attachment_type.TEXT)
                allure.attach(str(policies_config), name="Payload", attachment_type=allure.attachment_type.TEXT)
                allure.attach(str(response.text), name="Response", attachment_type=allure.attachment_type.TEXT)
                assert False

    @pytest.mark.api
    @pytest.mark.api5
    @pytest.mark.testsuite
    @pytest.mark.order(5)
    def test_005(self, api_client, api_base_url):
        try:
            allure.dynamic.title("Create a Watch")
            allure.dynamic.description("Use the Create Watch REST API to link the policy and repository")
            allure.dynamic.link(f"{self.url}{ApiEndPoint.create_watch}")
            update_watches_name = "example1-watch_{}".format((datetime.now() + timedelta()).strftime('%y%m%d%a%H%M%S'))
            watches_config = {
                "general_data": {
                    "name": "{}".format(update_watches_name),
                    "description": "This is an example watch #1",
                    "active": True
                },
                "project_resources": {
                    "resources": [
                        {
                            "type": "repository",
                            "bin_mgr_id": "default",
                            "name": "docker-local",
                            "filters": [
                                {
                                    "type": "regex",
                                    "value": ".*"
                                }
                            ]
                        }
                    ]
                },
                "assigned_policies": [
                    {
                        "name": "sec_policy_1",
                        "type": "security"
                    }
                ]
            }
            response = api_client.post(f"{self.url}{ApiEndPoint.create_watch}", headers=self.headers,
                                       data=json.dumps(watches_config))
            if response.status_code == 200 or response.status_code == 201:
                with allure.step("-- SUCCESS - Watch has been successfully created  : {} - {}".format(
                        response.status_code,
                        response.text)):
                    self.Logger.info(
                        "-- SUCCESS - Watch has been successfully created : {} - {}".format(
                            response.status_code,
                            response.text))
                    allure.attach(str(response.status_code), name="Status Code",
                                  attachment_type=allure.attachment_type.TEXT)
                    allure.attach(str(watches_config), name="Payload", attachment_type=allure.attachment_type.TEXT)
                    allure.attach(str(response.text), name="Response", attachment_type=allure.attachment_type.TEXT)
                    assert True
            elif response.status_code == 409:
                with allure.step("-- SUCCESS - Watch already exists  : {} - {}".format(
                        response.status_code,
                        response.text)):
                    self.Logger.info(
                        "-- SUCCESS - Watch already exists : {} - {}".format(
                            response.status_code,
                            response.text))
                    allure.attach(str(response.status_code), name="Status Code",
                                  attachment_type=allure.attachment_type.TEXT)
                    allure.attach(str(watches_config), name="Payload", attachment_type=allure.attachment_type.TEXT)
                    allure.attach(str(response.text), name="Response", attachment_type=allure.attachment_type.TEXT)
                    assert True
            else:
                with allure.step(
                        "-- FAILED - To Create Watch : {} - {}".format(response.status_code, response.text)):
                    self.Logger.error(
                        "-- FAILED - To Create Watch : {} - {}".format(response.status_code, response.text))

        except Exception as err:
            with allure.step("Exception during Create a Watch Policy please check logs for more details : {}".format(
                    err)):
                self.Logger.error(
                    "Exception during Create a Create a Watch please check logs for more details : {}".format(
                        err))
                allure.attach(str(response.status_code), name="Status Code",
                              attachment_type=allure.attachment_type.TEXT)
                allure.attach(str(watches_config), name="Payload", attachment_type=allure.attachment_type.TEXT)
                allure.attach(str(response.text), name="Response", attachment_type=allure.attachment_type.TEXT)
                assert False

    @pytest.mark.api
    @pytest.mark.api6
    @pytest.mark.testsuite
    @pytest.mark.order(6)
    def test_006(self, api_client, api_base_url):
        try:
            allure.dynamic.title("Check Scan Status:")
            allure.dynamic.description("Use the Xray REST API to verify that the image has been scanned \n"
                                       "Note that this is an asynchronous operation and will take time. Eventually,\n"
                                       "you will see overall: { 'status': 'DONE'}")
            allure.dynamic.link(f"{self.url}{ApiEndPoint.check_scan_status}")
            scan_config = {
                "repo": "docker-local",
                "path": "/alpine/3.9/manifest.json"
            }
            response = api_client.post(f"{self.url}{ApiEndPoint.check_scan_status}", headers=self.headers,
                                       data=json.dumps(scan_config))
            if response.status_code == 200 or response.status_code == 201:
                with allure.step("-- SUCCESS - Scan done successfully created  : {} ".format(
                        response.status_code)):
                    self.Logger.info(
                        "-- SUCCESS - Scan done successfully : {} ".format(
                            response.status_code))
                    allure.attach(str(response.status_code), name="Status Code",
                                  attachment_type=allure.attachment_type.TEXT)
                    allure.attach(str(scan_config), name="Payload", attachment_type=allure.attachment_type.TEXT)
                    allure.attach(str(response.text), name="Response", attachment_type=allure.attachment_type.TEXT)
                    assert True
            else:
                with allure.step(
                        "-- FAILED - To Scan : {} ".format(response.status_code)):
                    self.Logger.error(
                        "-- FAILED - To Scan : {} ".format(response.status_code))
                    assert False
        except Exception as err:
            with allure.step("Exception during Check Scan Status please check logs for more details : {}".format(
                    err)):
                self.Logger.error(
                    "Exception during Check Scan Status please check logs for more details : {}".format(
                        err))
                allure.attach(str(response.status_code), name="Status Code",
                              attachment_type=allure.attachment_type.TEXT)
                allure.attach(str(scan_config), name="Payload", attachment_type=allure.attachment_type.TEXT)
                allure.attach(str(response.text), name="Response", attachment_type=allure.attachment_type.TEXT)
                assert False

    @pytest.mark.api
    @pytest.mark.api7
    @pytest.mark.testsuite
    @pytest.mark.order(7)
    def test_007(self, api_client, api_base_url):
        try:
            allure.dynamic.title("Verify Violations")
            allure.dynamic.description("Use the Get Violation REST API to check if violations were generated \n"
                                       "Note that this is an asynchronous operation and will take time. Eventually,\n"
                                       "you will see the `total_violations > 0`")
            allure.dynamic.link(f"{self.url}{ApiEndPoint.verify_violations}")
            violations_config = {
                "filters": {
                    "watch_name": "example1-watch",
                    "violation_type": "Security",
                    "min_severity": "High",
                    "resources": {
                        "artifacts": [
                            {
                                "repo": "docker-local",
                                "path": "/alpine/3.9/manifest.json"
                            }
                        ]
                    }
                },
                "pagination": {
                    "order_by": "created",
                    "direction": "asc",
                    "limit": 100,
                    "offset": 1
                }
            }
            response = api_client.post(f"{self.url}{ApiEndPoint.verify_violations}", headers=self.headers,
                                       data=json.dumps(violations_config))
            if response.status_code == 200 or response.status_code == 201:
                with allure.step("-- SUCCESS - Generated Violations   : {} ".format(
                        response.status_code)):
                    self.Logger.info(
                        "-- SUCCESS - Generated Violations  : {} ".format(
                            response.status_code))
                    allure.attach(str(response.status_code), name="Status Code",
                                  attachment_type=allure.attachment_type.TEXT)
                    allure.attach(str(violations_config), name="Payload", attachment_type=allure.attachment_type.TEXT)
                    allure.attach(str(response.text), name="Response", attachment_type=allure.attachment_type.TEXT)
                    assert True
            else:
                with allure.step(
                        "-- FAILED - To Generated Violations : {} ".format(response.status_code)):
                    self.Logger.error(
                        "-- FAILED - To Generated Violations : {} ".format(response.status_code))
                    assert False
        except Exception as err:
            with allure.step("Exception during Verify Violations please check logs for more details : {}".format(
                    err)):
                self.Logger.error(
                    "Exception during Verify Violations please check logs for more details : {}".format(
                        err))
                allure.attach(str(response.status_code), name="Status Code",
                              attachment_type=allure.attachment_type.TEXT)
                allure.attach(str(violations_config), name="Payload", attachment_type=allure.attachment_type.TEXT)
                allure.attach(str(response.text), name="Response", attachment_type=allure.attachment_type.TEXT)
                assert False
