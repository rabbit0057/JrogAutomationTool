import logging
import os


class LogGen:
    @staticmethod
    def logger():
        current_path = os.path.join(os.getcwd(), "Logs", "jfrog_automation.log")
        logging.basicConfig(filename=current_path, format='%s(asctime)s: %(levelname)s', datefmt='%m%d%Y %I:%M:%S: %p',
                            force=True)
        logs = logging.getLogger()
        logs.setLevel(logging.INFO)
        return logs
