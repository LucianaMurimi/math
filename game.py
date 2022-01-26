import pygame.key
from pygame.locals import *
import random
from bg import *
from menu import Menu
from button import Button
from spritesheet import *
from bubble import *
from screen1 import *
from swim import *
from burst import *


pygame.init()

# OBJECTS
background = Background()
swim = Swim()
screen1_swim = Swim()
burst = Burst(SCREEN_WIDTH / 2, 278)
spritesheet = Spritesheet("./assets/images/bubbles/bubble_burst.png", 3, 3)

# SPRITE GROUPS
all_sprites = pygame.sprite.Group()
swimming = pygame.sprite.Group()
swimming.add(swim)

screen1_swimming = pygame.sprite.Group()
screen1_swimming.add(screen1_swim)

bursting = pygame.sprite.Group()
bursting.add(burst)

enemies = pygame.sprite.Group()
bubbles = pygame.sprite.Group()


class Game:
    # CUSTOM EVENTS
    ADDbubble = pygame.USEREVENT + 1
    pygame.time.set_timer(ADDbubble, 5000)

    def __init__(self):
        # menu
        self.menu = Menu(("Addition", "Subtraction", "Multiplication"),
                         ttf_font="./assets/fonts/Sniglet-Regular.ttf", font_size=64)
        self.show_menu = True

        self.screen_one = ScreenOne()
        self.display_screen_one = True

        self.screen_two = Menu(("Level 1", "Level 2"),
                         ttf_font="./assets/fonts/Sniglet-Regular.ttf", font_size=64)
        self.display_screen_two = True

        self.shell_menu = Menu(("Sign In", "Back", "Exit"), ttf_font="./assets/fonts/Sniglet-Regular.ttf", font_size=64)
        self.shell_menu_check = False

        # font
        self.font = pygame.font.Font("./assets/fonts/Sniglet-Regular.ttf", 42)
        self.score_font = pygame.font.Font("./assets/fonts/RosewellBlackRGH.otf", 20)

        # dictionary with keys: num1, num2, result
        # variables for creating the arithmetic problem
        self.problem = {"num1": 0, "num2": 0, "result": 0}
        self.symbols = {"addition": " + ", "subtraction": " - ", "multiplication": " x "}
        # variable for name of operation
        self.operation = ""
        self.button_list = self.get_button_list()

        self.reset_problem = False

        # score counter
        self.score = 0
        # counter for the number of problems
        self.count = 0

        self.shell_image = pygame.image.load("./assets/images/menu_img.png").convert_alpha()

        self.shell_rect = pygame.Rect(SCREEN_WIDTH - 64 - 36, 24, 72, 72)

        # sound effects
        self.sound_1 = pygame.mixer.Sound("./assets/audio/item1.ogg")
        self.sound_2 = pygame.mixer.Sound("./assets/audio/item2.ogg")
        self.bubble_burst = pygame.mixer.Sound("./assets/audio/bubble_burst.mp3")

    def process_events(self, screen):
        # EVENTS
        for event in pygame.event.get():
            # 1. quit game on EXIT
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.MOUSEBUTTONDOWN:
                # 2. MENU Window - SELECT Operation
                if self.display_screen_two:
                    if self.screen_two.state == 0:
                        self.display_screen_two = False
                        pygame.time.wait(500)
                    elif self.screen_two.state == 1:
                        self.display_screen_two = False
                        pygame.time.wait(500)
                elif self.show_menu:
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

                # 3. CHECK RESULT
                else:
                    self.check_result()

                if not self.show_menu and self.shell_rect.collidepoint(pygame.mouse.get_pos()):
                    self.shell_menu_check = not self.shell_menu_check

            if event.type == self.ADDbubble:
                # create the new bubble and add it to sprite groups
                new_bubble = Bubbles()
                bubbles.add(new_bubble)
                all_sprites.add(new_bubble)

            # enemyCollisions = pygame.sprite.spritecollide(swim, enemies, True, False)
            enemy_collisions = pygame.sprite.spritecollide(swim, enemies, pygame.sprite.collide_mask)
            for enemy in enemy_collisions:
                print(enemy.number)
                enemy.bursting.update()
                enemy.bursting.draw(screen)

        pressed_key = pygame.key.get_pressed()
        if pressed_key[K_ESCAPE]:
            self.show_menu = True
            self.score = 0
            self.count = 0
            self.shell_menu_check = False
        else:
            swim.move(pressed_key)
            swimming.draw(screen)

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

    #######################################################
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
    #######################################################

    def get_button_list(self):
        # return a list with four buttons
        button_list = []

        # assign one of the buttons with the right answer
        choice = random.randint(1, 4)

        # define the width and height
        width = 100
        height = 100

        pos_x = random.randint(100, 300)
        pos_y = random.randint(150, 240)

        if choice == 1:
            btn = Button(pos_x, pos_y, width, height, self.problem["result"])
            button_list.append(btn)
            enemies.add(btn)
        else:
            btn = Button(pos_x, pos_y, width, height, random.randint(0, 100))
            button_list.append(btn)
            enemies.add(btn)

        pos_x = random.randint(500, 700)
        pos_y = random.randint(150, 240)

        if choice == 2:
            btn = Button(pos_x, pos_y, width, height, self.problem["result"])
            button_list.append(btn)
            enemies.add(btn)
        else:
            btn = Button(pos_x, pos_y, width, height, random.randint(0, 100))
            button_list.append(btn)
            enemies.add(btn)

        pos_x = random.randint(100, 300)
        pos_y = random.randint(340, 380)

        if choice == 3:
            btn = Button(pos_x, pos_y, width, height, self.problem["result"])
            button_list.append(btn)
            enemies.add(btn)
        else:
            btn = Button(pos_x, pos_y, width, height, random.randint(0, 100))
            button_list.append(btn)
            enemies.add(btn)

        pos_x = random.randint(500, 700)
        pos_y = random.randint(340, 380)

        if choice == 4:
            btn = Button(pos_x, pos_y, width, height, self.problem["result"])
            button_list.append(btn)
            enemies.add(btn)
        else:
            btn = Button(pos_x, pos_y, width, height, random.randint(0, 100))
            button_list.append(btn)
            enemies.add(btn)

        return button_list

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

    def run_logic(self):
        # update menu
        self.menu.update()
        self.screen_two.update()

    def display_frame(self, screen):
        background.set_background(screen, self.show_menu)
        time_wait = False

        # screen 1
        if self.display_screen_one:
            self.screen_one.display_screen_one(screen)
            is_swimming = screen1_swim.swim_right(True)
            if is_swimming:
                screen1_swimming.draw(screen)
                screen1_swimming.update()
            else:
                self.bubble_burst.play()
                bursting.update()
                bursting.draw(screen)

            bursting.draw(screen)

            global TICKS
            TICKS = pygame.time.get_ticks()
            if TICKS > 3600:
                self.display_screen_one = False

        # screen 2
        elif self.display_screen_two:
            self.screen_two.display_frame(screen)
            bubbles.update()
            for entity in all_sprites:
                screen.blit(entity.surf, entity.rect)

        # 1. Show menu
        elif self.show_menu:
            self.menu.display_frame(screen)

        # 2. Game Over Screen
        elif self.count == 3:
            # if the count gets to 3 that means that the game is over
            msg_1 = "You answered " + str(self.score / 5) + " correctly"
            msg_2 = "Your score was " + str(self.score)
            self.display_message(screen, (msg_1, msg_2))

            self.show_menu = True
            # reset score and count to 0
            self.score = 0
            self.count = 0
            # set time_wait True to wait 3 seconds
            time_wait = True

        # 3. Math Problem Screen
        else:
            # labels for each number
            label_1 = self.font.render(str(self.problem["num1"]), True, BLACK)
            label_2 = self.font.render(self.symbols[self.operation], True, BLACK)
            label_3 = self.font.render(str(self.problem["num2"]) + " = ?", True, BLACK)

            # center the equation
            # t_w: total width
            t_w = label_1.get_width() + label_2.get_width() + label_3.get_width()  # 64: length of symbol
            pos_x = (SCREEN_WIDTH / 2) - (t_w / 2)

            screen.blit(label_1, (pos_x, 50))
            screen.blit(label_2, (pos_x + label_1.get_width(), 50))
            screen.blit(label_3, (pos_x + label_1.get_width() + label_2.get_width(), 50))

            # buttons
            for btn in self.button_list:
                btn.draw(screen)

            # score
            # score_label = self.score_font.render("Score : " + str(self.score), True, (15, 157, 8))
            # screen.blit(score_label, (SCREEN_WIDTH - score_label.get_width() - 20, 10))

            screen.blit(self.shell_image, (SCREEN_WIDTH - 64 - 36, 24))

            # bubbles.update()
            swimming.update()
            swimming.draw(screen)

            pygame.display.update()

            if self.shell_menu_check:
                background.set_background(screen, True)
                self.shell_menu.display_frame(screen)
                pygame.display.update()

        pygame.display.flip()

        # --- this is for the game to wait a few seconds to be able to show
        # --- what we have drawn before it change to another frame
        if self.reset_problem:
            # wait 1 second
            pygame.time.wait(1000)
            self.set_problem()
            # increase count by 1
            self.count += 1
            self.reset_problem = False
        elif time_wait:
            # wait three seconds
            pygame.time.wait(4000)

    def display_message(self, screen, items):
        """ display every string that is inside of a tuple(args) """
        for index, message in enumerate(items):
            label = self.font.render(message, True, BLACK)
            # get the width and height of the label
            width = label.get_width()
            height = label.get_height()

            pos_x = (SCREEN_WIDTH / 2) - (width / 2)
            # t_h: total height of text block
            t_h = len(items) * height
            pos_y = (SCREEN_HEIGHT / 2) - (t_h / 2) + (index * height)

            screen.blit(label, (pos_x, pos_y))
