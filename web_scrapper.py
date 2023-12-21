from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
class ChessWebHandler:

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

        #Remove the first element, which is move number
        moves = list(map(lambda move: move.text.split("\n")[1:], moves))
        #Convert list of lists into list
        moves = [item for sublist in moves for item in sublist]
        return moves

    def make_move(self, move):
        ac = ActionChains(self.driver)
        square_from = str(ord(move[0]) - 96) + move[1]
        square_to = str(ord(move[2]) - 96) + move[3]
        element =self.driver.find_element(By.CLASS_NAME, "square-"+square_from)
        ac.move_to_element(element).move_by_offset(0, 0).click().perform()
        element =self.driver.find_element(By.CLASS_NAME, "square-"+square_to)
        ac.move_to_element(element).move_by_offset(0, 0).click().perform()


