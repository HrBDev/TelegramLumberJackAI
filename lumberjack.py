import numpy
import pyautogui
from PIL import Image
from selenium import webdriver

branch = {161, 116, 56, 255}


class Game:
    driver = webdriver.Firefox()
    isRight = False
    interval = 0.0082

    def __init__(self):
        self.driver.set_window_size(600, 800)
        self.driver.get(
            "https://tbot.xyz/lumber"
            "#eyJ1Ijo1NDAxODc0MjgsIm4iOiJIQG1pZHIzemEgIiwiZyI6Ikx1bWJlckphY2siLCJjaSI6IjMxMzY0OTU4NDY0OTg0NTMyOTIiLCJpIjoiQkFBQUFPbG9BUUFrbXpJZ0FjdlJqSXBHRVNNIn0zMzJlMzYxMGVlNjRlYzA2Y2FiNDNlNTMyZjY2OTdlMw==&tgShareScoreUrl=tg%3A%2F%2Fshare_game_score%3Fhash%3Dn5FSzjfd65_o5wSM4Qi-Uc2p0PhKB6k70jE3EIjvC6w"
        )
        assert "LumberJack" in self.driver.title
        self.left = self.driver.find_element_by_class_name("button_left")
        self.right = self.driver.find_element_by_id("button_right")
        self.play_button = self.driver.find_element_by_class_name("button")

    def chop(self):
        if self.isRight:
            pyautogui.press('right', interval=self.interval, _pause=False)
        else:
            pyautogui.press('left', interval=self.interval, _pause=False)

    def process(self):
        self.driver.save_screenshot('./scr.png')
        self.driver.get_screenshot_as_png()
        # img_file: Image = Image.open('./scr.png')
        # img_file = BytesIO(base64.b64decode(self.driver.get_screenshot_as_base64()))
        img: Image = Image.open('./scr.png')

        if self.isRight:
            region: Image = img.crop((469, 325, 471, 345))
            # region.save('./regionRight.png')
        else:
            region = img.crop((261, 325, 263, 345))
            # region.save('./regionLeft.png')

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
        while True:
            self.play()


if __name__ == '__main__':
    game = Game()
    game.start()
