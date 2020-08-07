"""Instappium main class"""

from .appium_webdriver import AppiumWebDriver
from .common.xpath import xpath
from .common import Logger

from time import sleep


class InstAppium(object):
    """
    Class to be instantiated to use the script
    class variable:
        - None
    instance variable:
        - _webdriver
        - username
        - password
        - device

    """

    def __init__(
        self,
        username: str = "",
        password: str = "",
        device: str = "",
        logfolder: str = "",
        show_logs: bool = False,
        log_handler: object = None,
    ):
        """

        """
        Logger.initlogger(username, logfolder, show_logs, log_handler)
        self.username = username
        self.password = password
        self.device = device

        # ideally we should launch appium here
        # so there is no external dependency
        # todo: when it's stable

        try:
            self._webdriver = AppiumWebDriver(devicename=device)
        except:
            Logger.logerror(
                "Could not create webdriver; please make sure Appium is running"
            )
            quit()

        Logger.highlight_print(
            message="Connected to Appium successfully",
            message_type="initialization",
            level="info",
        )
        self._webdriver.keep_alive()

        current_activity = self._webdriver.current_activity().split(".")[-1]

        # Lets log in!
        if "SignedOut" in current_activity:
            # print(self._webdriver._web_driver_instance.page_source)
            check_login = self._webdriver.find_elements_by_xpath(
                xpath.read_xpath("login", "login_button")
            )
            if check_login:
                check_login[0].click()
                sleep(5)

            print(self._webdriver._web_driver_instance.page_source)

            username_edit_text = self._webdriver.find_elements_by_xpath(
                xpath.read_xpath("login", "login_username")
            )
            if username_edit_text:
                username_edit_text[0].set_value(username)

            password_edit_text = self._webdriver.find_elements_by_xpath(
                xpath.read_xpath("login", "login_password")
            )
            if password_edit_text:
                password_edit_text[0].set_value(password)
            sleep(5)

            log_in = self._webdriver.find_elements_by_xpath(
                xpath.read_xpath("login", "log_me_in_button")
            )
            if log_in:
                log_in[0].click()
            
            sleep(2)

            if self._webdriver.current_activity().split(".")[-1] == "MainActivity":
                Logger.highlight_print(
                    message="Login successful", message_type="login", level="info"
                )
