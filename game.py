import pygame
import random
from bubble import Bubbles
from button import Button
from menu import Menu
from globals import *
from player import Player

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

pygame.init()


class Game:
    ADDBUBBLES = pygame.USEREVENT + 1
    pygame.time.set_timer(ADDBUBBLES, 1000)

    bubbles = pygame.sprite.Group()
    player = Player()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)

    enemies = pygame.sprite.Group()

    def __init__(self):
        self.all_sprites = pygame.sprite.Group()
        # menu
        self.menu = Menu(("Addition", "Subtraction", "Multiplication", "Division"),
                         ttf_font="RosewellBlackRGH.otf", font_size=42)
        self.show_menu = True

        # new font object
        self.font = pygame.font.Font(None, 64)

        # font for the score msg
        self.score_font = pygame.font.Font("RosewellBlackRGH.otf", 20)

        # dictionary with keys: num1, num2, result
        # variables for creating the arithmetic problem
        self.problem = {"num1": 0, "num2": 0, "result": 0}

        # variable for name of operation
        self.operation = ""
        self.symbols = self.get_symbols()
        self.button_list = self.get_button_list()

        self.reset_problem = False
        # score counter
        self.score = 0
        # counter for the number of problems
        self.count = 0
        

        self.pressed_keys = pygame.key.get_pressed()

        self.background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.background.fill(SKY_BLUE)

        # sound effects
        self.sound_1 = pygame.mixer.Sound("item1.ogg")
        self.sound_2 = pygame.mixer.Sound("item2.ogg")

    def process_events(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
                # Update the player sprite based on user keypresses

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.show_menu:
                    if self.menu.state == 0:
                        self.operation = "addition"
                        self.set_problem()
                        self.show_menu = False
                    elif self.menu.state == 1:
                        self.operation = "subtraction"
                        self.set_problem()
                        self.show_menu = False
                    elif self.menu.state == 2:
                        self.operation = "multiplication"
                        self.set_problem()
                        self.show_menu = False
                    elif self.menu.state == 3:
                        self.operation = "division"
                        self.set_problem()
                        self.show_menu = False

                else:
                    self.check_result()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.show_menu = True
                    self.score = 0
                    self.count = 0
                if event.key == K_UP or event.key == K_DOWN or \
                        event.key == K_LEFT or event.key == K_RIGHT:
                    self.player.update(event.key)
            if pygame.sprite.spritecollideany(self.player, self.enemies):
                # If so, then remove the player and stop the loop
                self.player.kill()
                return False

                # if event.type == self.ADDBUBBLES:
                # Create the new enemy and add it to sprite groups
                # new_bubble = Bubbles()
                # self.bubbles.add(new_bubble)
                # self.all_sprites.add(new_bubble)


                    # set time_wait True to wait 3 seconds
        return True

    def set_problem(self):
        if self.operation == "addition":
            self.addition()
        elif self.operation == "subtraction":
            self.subtraction()
        elif self.operation == "multiplication":
            self.multiplication()
        elif self.operation == "division":
            self.division()
        self.button_list = self.get_button_list()

    def addition(self):
        a = random.randint(0, 100)
        b = random.randint(0, 100)
        self.problem["num1"] = a
        self.problem["num2"] = b
        self.problem["result"] = a + b
        self.operation = "addition"

    def subtraction(self):
        a = random.randint(0, 100)
        b = random.randint(0, 100)
        if a > b:
            self.problem["num1"] = a
            self.problem["num2"] = b
            self.problem["result"] = a - b
        else:
            self.problem["num1"] = b
            self.problem["num2"] = a
            self.problem["result"] = b - a
        self.operation = "subtraction"

    def multiplication(self):
        a = random.randint(0, 12)
        b = random.randint(0, 12)
        self.problem["num1"] = a
        self.problem["num2"] = b
        self.problem["result"] = a * b
        self.operation = "multiplication"

    def division(self):
        divisor = random.randint(1, 12)
        dividend = divisor * random.randint(1, 12)
        quotient = dividend / divisor
        self.problem["num1"] = dividend
        self.problem["num2"] = divisor
        self.problem["result"] = quotient
        self.operation = "division"

    def get_button_list(self):
        # return a list with four buttons
        button_list = []

        # random center values
        random_x = []
        random_y = []

        # assign one of the buttons with the right answer
        choice = random.randint(1, 4)

        # define the width and height
        width = 100
        height = 100

        # t_w: total width
        t_w = width * 2 + 50
        posX = random.randint(100, 300)
        posY = random.randint(150, 240)
        random_x.append(posX)
        random_y.append(posY)
        # random_center.append({"x": posX, "y": posY})

        if choice == 1:
            btn = Button(posX, posY, width, height, self.problem["result"])
            button_list.append(btn)
            self.enemies.add(btn)
        else:
            btn = Button(posX, posY, width, height, random.randint(0, 100))
            button_list.append(btn)
            self.enemies.add(btn)

        # def getPosVal(r):
        #     new_posX = random.randint(100, 700)
        #     new_posY = random.randint(150, 380)
        #
        #     for i in range(r):
        #         if self.check_in_range(new_posX, random_x[i] - width, random_x[i] + width) and \
        #                 self.check_in_range(new_posY, random_y[i] - height, random_y[i] + height):
        #
        #             getPosVal(r)
        #         else:
        #             random_x.append(new_posX)
        #             random_y.append(new_posY)
        #             return

        # print(getPosVal(posX, posY, 1)[0])

        posX = random.randint(500, 700)
        posY = random.randint(150, 240)


        # if new_posX in range(random_center[0]["x_1"]-width//2, random_center[0]["x_1"]+width//2, 1):
        #     if new_posX + width > 700:
        #         posX = new_posX - width
        #     else:
        #         posX = new_posX + width
        # else:
        #     posX = new_posX
        # if new_posY in range(random_center[0]["y_1"]-height//2, random_center[0]["y_1"]+height//2, 1):
        #     if new_posY + height > 400:
        #         posY = new_posY - height
        #     else:
        #         posY = new_posY + height
        # else:
        #     posY = new_posY
        # random_center.append({"x_2": posX, "y_2": posY})

        if choice == 2:
            btn = Button(posX, posY, width, height, self.problem["result"])
            button_list.append(btn)
            self.enemies.add(btn)
        else:
            btn = Button(posX, posY, width, height, random.randint(0, 100))
            button_list.append(btn)
            self.enemies.add(btn)

        # posX = (SCREEN_WIDTH / 2) - (t_w / 2)
        # posY = 300

        # new_posX = random.randint(100, 700)
        # new_posY = random.randint(150, 380)
        # if new_posX in range(random_center[0]["x_1"] - width // 2, random_center[0]["x_1"] + width // 2, 1)\
        #         or new_posX in range(random_center[1]["x_2"] - width // 2, random_center[1]["x_2"] + width // 2, 1):
        #     if new_posX + width > 700:
        #         posX = new_posX - width
        #     else:
        #         posX = new_posX + width
        # else:
        #     posX = new_posX
        #
        # if new_posY in range(random_center[0]["y_1"] - height // 2, random_center[0]["y_1"] + height // 2, 1)\
        #         or new_posY in range(random_center[1]["y_2"] - height // 2, random_center[1]["y_2"] + height // 2, 1):
        #     if new_posY + height > 400:
        #         posY = new_posY - height
        #     else:
        #         posY = new_posY + height
        # else:
        #     posY = new_posY
        # random_center.append({"x_3": posX, "y_3": posY})

        posX = random.randint(100, 300)
        posY = random.randint(340, 380)


        if choice == 3:
            btn = Button(posX, posY, width, height, self.problem["result"])
            button_list.append(btn)
            self.enemies.add(btn)
        else:
            btn = Button(posX, posY, width, height, random.randint(0, 100))
            button_list.append(btn)
            self.enemies.add(btn)

        # posX = (SCREEN_WIDTH / 2) - (t_w / 2) + 150
        # new_posX = random.randint(100, 700)
        # new_posY = random.randint(150, 380)
        # if new_posX in range(random_center[0]["x_1"] - width // 2, random_center[0]["x_1"] + width // 2, 1) \
        #         or new_posX in range(random_center[1]["x_2"] - width // 2, random_center[1]["x_2"] + width // 2, 1)\
        #         or new_posX in range(random_center[2]["x_3"] - width // 2, random_center[2]["x_3"] + width // 2, 1):
        #     if new_posX + width > 700:
        #         posX = new_posX - width
        #     else:
        #         posX = new_posX + width
        # else:
        #     posX = new_posX
        #
        # if new_posY in range(random_center[0]["y_1"] - height // 2, random_center[0]["y_1"] + height // 2, 1) \
        #         or new_posY in range(random_center[1]["y_2"] - height // 2, random_center[1]["y_2"] + height // 2, 1)\
        #         or new_posY in range(random_center[2]["y_3"] - height // 2, random_center[2]["y_3"] + height // 2, 1):
        #     if new_posY + height > 400:
        #         posY = new_posY - height
        #     else:
        #         posY = new_posY + height
        # else:
        #     posY = new_posY
        # random_center.append({"x_4": posX, "y_4": posY})

        posX = random.randint(500, 700)
        posY = random.randint(340, 380)

        if choice == 4:
            btn = Button(posX, posY, width, height, self.problem["result"])
            button_list.append(btn)
            self.enemies.add(btn)
        else:
            btn = Button(posX, posY, width, height, random.randint(0, 100))
            button_list.append(btn)
            self.enemies.add(btn)

        return button_list

    def check_in_range(self, val, start, stop):
        if val in range(start, stop, 1):
            print("True")
            return True
        else:
            print("False")
            return False

    def check_result(self):
        for button in self.button_list:
            if button.isPressed():
                if button.get_number() == self.problem["result"]:
                    # set color to green when correct
                    button.set_color(GREEN)
                    # increase score
                    self.score += 5
                    # Play sound effect
                    self.sound_1.play()
                else:
                    # set color to red when incorrect
                    button.set_color(RED)
                    # play sound effect
                    self.sound_2.play()

                # set reset_problem True so it can go to the next problem
                self.reset_problem = True

    def get_symbols(self):
        """ Return a dictionary with all the operation symbols """
        symbols = {}
        sprite_sheet = pygame.image.load("symbols.png").convert()
        image = self.get_image(sprite_sheet, 0, 0, 64, 64)
        symbols["addition"] = image
        image = self.get_image(sprite_sheet, 64, 0, 64, 64)
        symbols["subtraction"] = image
        image = self.get_image(sprite_sheet, 128, 0, 64, 64)
        symbols["multiplication"] = image
        image = self.get_image(sprite_sheet, 192, 0, 64, 64)
        symbols["division"] = image

        return symbols

    def get_image(self, sprite_sheet, x, y, width, height):
        """ This method will cut an image and return it """
        # Create a new blank image
        image = pygame.Surface([width, height]).convert()
        image.set_colorkey((255, 255, 255))
        # Copy the sprite from the large sheet onto the smaller
        image.blit(sprite_sheet, (0, 0), (x, y, width, height))
        # Return the image
        return image

    def run_logic(self):
        # Update menu
        self.menu.update()

    def display_frame(self, screen):

        # draw the background image
        screen.blit(self.background, (0, 0))
        # screen.blit(pygame.image.load("bubbles.png").convert(), (0, 0))

        # True: call pygame.time.wait()
        time_wait = False
        # --- Drawing code should go here
        if self.show_menu:
            self.menu.display_frame(screen)
        elif self.count == 3:
            # if the count gets to 20 that means that the game is over
            # and we are going to display how many answers were correct
            # and the score
            msg_1 = "You answered " + str(self.score / 5) + " correctly"
            msg_2 = "Your score was " + str(self.score)
            self.display_message(screen, (msg_1, msg_2))
            self.show_menu = True
            # reset score and count to 0
            self.score = 0
            self.count = 0
            # set time_wait True to wait 3 seconds
            time_wait = True
        else:
            # Create labels for the each number
            label_1 = self.font.render(str(self.problem["num1"]), True, BLACK)
            label_2 = self.font.render(str(self.problem["num2"]) + " = ?", True, BLACK)
            # t_w: total width
            t_w = label_1.get_width() + label_2.get_width() + 64  # 64: length of symbol
            posX = (SCREEN_WIDTH / 2) - (t_w / 2)
            screen.blit(label_1, (posX, 50))
            # print the symbol into the screen

            screen.blit(self.symbols[self.operation], (posX + label_1.get_width(), 40))

            screen.blit(label_2, (posX + label_1.get_width() + 64, 50))
            # Go to through every button and draw it
            for btn in self.button_list:
                btn.draw(screen)
            # display the score
            score_label = self.score_font.render("Score : " + str(self.score), True, (15, 157, 8))
            screen.blit(score_label, (10, 10))

            self.bubbles.update()
            # Draw all sprites
            # for entity in self.all_sprites:
            #     screen.blit(entity.surf, entity.rect)
            screen.blit(self.player.surf, self.player.rect)
        # --- Go ahead and update the screen with what we've drawn
        pygame.display.flip()
        # --- This is for the game to wait a few seconds to be able to show
        # --- what we have drawn before it change to another frame
        if self.reset_problem:
            # wait 1 second
            pygame.time.wait(1000)
            self.set_problem()
            # Increase count by 1
            self.count += 1
            self.reset_problem = False
        elif time_wait:
            # wait three seconds
            pygame.time.wait(4000)

    def display_message(self, screen, items):
        """ display every string that is inside of a tuple(args) """
        for index, message in enumerate(items):
            label = self.font.render(message, True, BLACK)
            # Get the width and height of the label
            width = label.get_width()
            height = label.get_height()

            posX = (SCREEN_WIDTH / 2) - (width / 2)
            # t_h: total height of text block
            t_h = len(items) * height
            posY = (SCREEN_HEIGHT / 2) - (t_h / 2) + (index * height)

            screen.blit(label, (posX, posY))
