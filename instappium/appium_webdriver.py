"""
Class to define everything needed to work with Appium
"""

#class import
from instappium.common import Logger

# libraries import
from appium import webdriver
from ppadb.client import Client as AdbClient
from time import sleep


class AppiumWebDriver:
    """
    Appium WebDriver class
    """
    _adb_client = None
    _web_driver_instance = None
    __DISPLAYSIZE = None

    def __init__(
        self,
        devicename: str = "",
        devicetimeout: int = 600,
        client_host: str = "127.0.0.1",
        client_port: int = 5037,
    ):

        self._adb_client = AdbClient(host=client_host, port=client_port)

        desired_caps = {}

        if any(devicename in device for device in self._get_adb_devices()):
            desired_caps["platformName"] = "Android"
            desired_caps["deviceName"] = devicename
            desired_caps["appPackage"] = "com.instagram.android"
            desired_caps["appActivity"] = "com.instagram.mainactivity.MainActivity"
            desired_caps["automationName"] = "UiAutomator2"
            desired_caps["noReset"] = True
            desired_caps["fullReset"] = False
            desired_caps["unicodeKeyboard"] = True
            desired_caps["resetKeyboard"] = True
            desired_caps["newCommandTimeout"] = devicetimeout

            try:
                self._web_driver_instance = webdriver.Remote(
                    "http://{}:4723/wd/hub".format(client_host), __desired_caps
                )
                Logger.info("Succesfully connected to: {}".format(devicename))
                self.__DISPLAYSIZE = self._web_driver_instance.get_window_size()
                sleep(10)
            except:
                # self.logger.error("Could not create webdriver, is Appium running?")
                Logger.error("Could not create webdriver; please make sure Appium is running")
                quit()  # TODO: nicer way of exiting

        else:

            Logger.error(
                "Invalid Device Name. \nList of available devices: [{}]".format(
                    ", ".join(self._get_adb_devices())
                )
            )
            quit()  # TODO: nicer way of exiting

    def _get_adb_devices(self):
        """
        protected function to check the current running simulators
        :return:
        """
        devices = []

        for device in self._adb_client.devices():
            devices.append(device.serial)

        return devices

    def get_driver(self):
        """
        wrapper for find_element by_xpath
        :param xpath:
        :return:
        """
        return self._web_driver_instance


    def find_elements_by_xpath(self, xpath: str = ""):
        """
        wrapper for find_element by_xpath
        :param xpath:
        :return:
        """
        return self._web_driver_instance.find_elements_by_xpath(xpath)

    def find_element_by_id(self, resource_id: str = ""):
        """
        wrapper for find_element_by_id
        :param resource_id:
        :return:
        """
        return self._web_driver_instance.find_element_by_id(resource_id)

    def find_element_by_uiautomator(self, uiautomator: str = ""):
        """
        wrapper for find_element_by_android_uiautomator
        :param uiautomator:
        :return:
        """
        return self._web_driver_instance.find_element_by_android_uiautomator(uiautomator)

    @staticmethod
    def click(webelem):
        """
        wrapper for element clicking
        :param webelem:
        :return:
        """
        webelem.click()

    def current_activity(self):
        return self._web_driver_instance.current_activity

    def swipe(self,x1,y1,x2,y2,duration):
        return self._web_driver_instance.swipe(x1,y1,x2,y2,duration)
