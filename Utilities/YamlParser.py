import os

import yaml


class YamlParser:

    @staticmethod
    def get_env_data():
        env_data = None
        env_file = os.path.join(os.getcwd(), "Config", "Env.yaml")
        try:
            env_data = yaml.safe_load(open(env_file))
        except Exception as err:
            print(" -- FAILED - To get ENV details - {}".format(err))
        return env_data

    @staticmethod
    def get_test_data():
        test_data = None
        test_data_file = os.path.join(os.getcwd(), "TestParameter", "TestData.yaml")
        try:
            test_data = yaml.safe_load(open(test_data_file))
        except Exception as err:
            print(" -- FAILED - To get ENV details - {}".format(err))
        return test_data
