"""Instappium main class"""

from .appium_webdriver import AppiumWebDriver
from .common.xpath import xpath
from .common import Logger

from time import sleep

class InstAppium (Logger):
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

    def __init__(self, username: str = '', password: str = '', device: str = '', logfolder: str = '', show_logs: bool = False, log_handler: object = None):
        """

        """
        Logger.__init__(self, username, logfolder, show_logs, log_handler)
        self.username = username
        self.password = password
        self.device = device

        try:
            self._webdriver = AppiumWebDriver(devicename=device, logger=self)
        except:
            self.logerror("Could not create webdriver; please make sure Appium is running")
            quit()

        self.highlight_print(message="Connected to Appium successfully", message_type="initialization", level="info")

        current_activity = self._webdriver.current_activity().split('.')[-1]

        # Lets log in!
        if 'SignedOut' in current_activity:
            check_login = self._webdriver.find_elements_by_xpath(xpath.read_xpath("login","login_button"))
            check_login[0].click()

            username_edit_text = self._webdriver.find_elements_by_xpath(xpath.read_xpath("login","login_username"))
            username_edit_text[0].set_value(username)

            password_edit_text = self._webdriver.find_elements_by_xpath(xpath.read_xpath("login","login_password"))
            password_edit_text[0].set_value(password)
            sleep(1)

            log_in = self._webdriver.find_elements_by_xpath(xpath.read_xpath("login","log_me_in"))
            log_in[0].click()

            if self._webdriver.current_activity().split('.')[-1] == 'MainActivity':
                self.highlight_print(message="Login successful", message_type="login", level="info")




