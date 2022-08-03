"""
Test cases for the harness flows
"""
import pytest
import time
import json
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class TestHarnessFlows:
    """Test the harness based flows."""

    def setup_method(self):
        """Initialize the tests, connect to selenium grid."""

        options = webdriver.ChromeOptions()
        options.add_argument("--ignore-ssl-errors=yes")
        options.add_argument("--ignore-certificate-errors")
        self.driver = webdriver.Remote(
            command_executor="http://selenium-chrome:4444/wd/hub", options=options
        )

    def teardown_method(self):
        """Close the tests."""

        self.driver.quit()

    def wait_for_window(self, timeout=2, wh_then=[]):
        """Wait for a new window or tab to open."""
        time.sleep(round(timeout / 1000))
        wh_now = self.driver.window_handles
        if len(wh_now) > len(wh_then):
            return set(wh_now).difference(set(wh_then)).pop()

    def test_harness_basic_flow(self) -> int:
        """Test a basic harness flow."""
        self.driver.get("https://harness.qa.verify.interac-id.ca/")
        self.driver.maximize_window()
        self.driver.find_element(By.CSS_SELECTOR, "legend:nth-child(2) > span").click()
        self.driver.find_element(By.ID, "given_name").click()
        self.driver.find_element(By.ID, "family_name").click()
        self.driver.find_element(By.ID, "phone_number").click()
        self.driver.find_element(By.ID, "address").click()
        self.driver.find_element(By.ID, "birthdate").click()
        self.driver.find_element(By.ID, "email").click()
        self.driver.find_element(By.ID, "queryButton").click()
        window_handles = self.driver.window_handles
        WebDriverWait(self.driver, 30).until(
            expected_conditions.visibility_of_element_located((By.ID, "qrcode2"))
        )
        self.driver.find_element(By.ID, "qrcode2").click()
        self.driver.switch_to.window(self.wait_for_window(wh_then=window_handles))

        # Wait for and click on My Bank R14
        WebDriverWait(self.driver, 30).until(
            expected_conditions.visibility_of_element_located(
                (
                    By.CSS_SELECTOR,
                    "#c-fi-selector-item__logo-My-Bank-R14 > .c-dapc-asset",
                )
            )
        )
        self.driver.find_element(
            By.CSS_SELECTOR, "#c-fi-selector-item__logo-My-Bank-R14 > .c-dapc-asset"
        ).click()

        # Wait for new tab to be ready, then fill out form and click login
        WebDriverWait(self.driver, 30).until(
            expected_conditions.visibility_of_element_located((By.ID, "userid"))
        )
        self.driver.find_element(By.ID, "userid").click()
        self.driver.find_element(By.ID, "userid").send_keys("jdoe5+123")
        self.driver.find_element(By.ID, "password").click()
        self.driver.find_element(By.ID, "password").send_keys("password")
        self.driver.find_element(By.ID, "login").click()

        # Wait for and click on the submit button
        WebDriverWait(self.driver, 30).until(
            expected_conditions.visibility_of_element_located((By.ID, "submit_code"))
        )
        self.driver.find_element(By.ID, "submit_code").click()

        # Wait for and click on the consent button
        WebDriverWait(self.driver, 30).until(
            expected_conditions.visibility_of_element_located((By.ID, "consent_ok"))
        )
        self.driver.find_element(By.ID, "consent_ok").click()
        
        # Wait for the green checkmark on the panel and click on the "I Agree" button
        WebDriverWait(self.driver, 30).until(
            expected_conditions.visibility_of_element_located(
                (By.CSS_SELECTOR, ".c-dap-overview-expander__check")
            )
          )
        self.driver.find_element(By.CSS_SELECTOR, ".ui-loading-button").click()
        time.sleep(10)
        retval = 1
        if self.driver.find_element(By.CSS_SELECTOR, "html").text.startswith("Success:"):
            retval = 0
        return retval


def main() -> int:
    """Entry point, manage test run"""
    test_case = TestHarnessFlows()
    test_case.setup_method()
    ret_val = test_case.test_harness_basic_flow()
    test_case.teardown_method()
    return ret_val


# Run script if not imported as a module: standard idiom
if __name__ == "__main__":
    sys.exit(main()) 
