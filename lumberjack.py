from io import BytesIO

import numpy
import pyautogui
from PIL import Image
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

branch = {161, 116, 56, 255}


class Game:
    driver = webdriver.Firefox()
    isRight = False
    interval = 0.00015

    def __init__(self):
        self.driver.set_window_size(600, 800)
        self.driver.get(
            "https://tbot.xyz/lumber"
            "#eyJ1Ijo1NDAxODc0MjgsIm4iOiJIQG1pZHIzemEgIiwiZyI6Ikx1bWJlckphY2siLCJjaSI6IjMxMzY0OTU4NDY0OTg0NTMyOTIiLCJpI"
            "joiQkFBQUFPbG9BUUFrbXpJZ0FjdlJqSXBHRVNNIn0zMzJlMzYxMGVlNjRlYzA2Y2FiNDNlNTMyZjY2OTdlMw==&tgShareScoreUrl=tg"
            "%3A%2F%2Fshare_game_score%3Fhash%3Dn5FSzjfd65_o5wSM4Qi-Uc2p0PhKB6k70jE3EIjvC6w"
        )
        assert "LumberJack" in self.driver.title
        self.left = self.driver.find_element_by_class_name("button_left")
        self.right = self.driver.find_element_by_id("button_right")
        self.play_button = self.driver.find_element_by_class_name("button")
        self.score = self.driver.find_element_by_class_name("score_value")
        self.page_wrap = self.driver.find_element_by_id("page_wrap")

    def chop(self):
        if self.isRight:
            pyautogui.press('right', interval=self.interval, _pause=False)
        else:
            pyautogui.press('left', interval=self.interval, _pause=False)

    def process(self):
        img: Image = Image.open(BytesIO(self.driver.get_screenshot_as_png()))

        if self.isRight:
            region: Image = img.crop((469, 280, 470, 340))
        else:
            region = img.crop((261, 280, 262, 340))

        for row in numpy.asarray(region):
            for item in row:
                if branch == set(item):
                    self.isRight = not self.isRight
                    return

    def play(self):
        self.process()
        self.chop()

    def start(self):
        self.play_button.click()
        while not self.is_game_finished():
            self.play()

    def get_score(self):
        print(self.score.text)

    def is_game_finished(self):
        if self.page_wrap.get_attribute("class") == "page_wrap ready in_result":
            return True
        else:
            return False


if __name__ == '__main__':
    game = Game()
    # Number of retries
    for i in range(10):
        game.start()
        game.get_score()
