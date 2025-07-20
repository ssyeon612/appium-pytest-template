class LoginPage:
    def __init__(self, driver):
        self.driver = driver

    def enter_username(self, username):
        self.driver.find_element_by_accessibility_id("usernameField").send_keys(username)

    def enter_password(self, password):
        self.driver.find_element_by_accessibility_id("passwordField").send_keys(password)

    def tap_login_button(self):
        self.driver.find_element_by_accessibility_id("loginButton").click()

    def is_logged_in(self):
        return self.driver.find_element_by_accessibility_id("homeScreen").is_displayed()
