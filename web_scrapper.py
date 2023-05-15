from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By

class ChessWebScrapper:

    def __init__(self):
        self.driver = Chrome()

    def open_page(self, url="https://www.chess.com/home"):
        self.driver.get(url)
    
    def login(self):
        #Read username and password from a file
        with open("C:/Users/delli/Documents/chess.com/credentials.txt") as f:
            username = f.readline()
            password = f.readline()

        self.driver.find_element(By.ID, "username").send_keys(username)
        self.driver.find_element(By.ID, "password").send_keys(password)
        self.driver.find_element(By.ID, "login").click()
    
    def get_current_position(self):
        moves = self.driver.find_elements(By.CLASS_NAME, "move")
        moves = list(map(lambda move: move.text.split("\n"), moves))
        return moves