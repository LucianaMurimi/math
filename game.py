import pygame.key
from pygame.locals import *
import random
from bg import *
from menu import Menu
from button import Button
from bubble import *
from screen_1 import *
from sprite import *
from burst import *
from sign_in import *


pygame.init()

# OBJECTS
background = Background()
sprite = Sprite()
screen1_swim = Sprite()
burst = Burst(SCREEN_WIDTH / 2, 270)
sign_in = SignIn()

# SPRITE GROUPS
all_sprites = pygame.sprite.Group()

sprite_group = pygame.sprite.Group()
sprite_group.add(sprite)

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
                         ttf_font="./assets/fonts/Sniglet-Regular.ttf", font_size=56)
        self.show_menu = True

        self.screen_one = ScreenOne()
        self.display_screen_one = True

        self.screen_two = Menu(("Level 1", "Level 2"),
                         ttf_font="./assets/fonts/Sniglet-Regular.ttf", font_size=64)
        self.display_screen_two = True

        self.shell_menu = Menu(("SIGN IN", "BACK", "EXIT"), ttf_font="./assets/fonts/Sniglet-Regular.ttf", font_size=42)
        self.shell_menu_check = False

        self.display_sign_in = False

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

        self.shell_image = pygame.image.load("./assets/images/shell.png").convert_alpha()

        self.shell_rect = pygame.Rect(SCREEN_WIDTH - 64 - 36, 24, 72, 72)

        # sound effects
        self.sound_1 = pygame.mixer.Sound("./assets/audio/item1.ogg")
        self.sound_2 = pygame.mixer.Sound("./assets/audio/item2.ogg")
        self.bubble_burst = pygame.mixer.Sound("./assets/audio/bubble_burst.mp3")

        self.username = ""

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
                elif self.shell_menu_check:
                    if self.shell_menu.state == 0:
                        self.display_sign_in = not self.display_sign_in
                        pygame.display.update()
                    elif self.shell_menu.state == 1:
                        print("1")
                for btn in sign_in.button_sign_in_list:
                    if btn.isPressed():
                        global USERNAME
                        print(btn.get_btn_value())
                        self.username = self.username + btn.get_btn_value()
                        screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
                        screen.fill(SKY_BLUE)
                        self.display_frame(screen)

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
            enemy_collisions = pygame.sprite.spritecollide(sprite, enemies, pygame.sprite.collide_mask)
            for enemy in enemy_collisions:
                print(enemy.number)
                enemy.bursting.update()
                enemy.bursting.draw(screen)

                if enemy.number == self.problem["result"]:
                    self.score += 5
                    self.sound_1.play()
                    self.reset_problem = True

        pressed_key = pygame.key.get_pressed()
        if pressed_key[K_ESCAPE]:
            self.show_menu = True
            self.score = 0
            self.count = 0
            self.shell_menu_check = False
        else:
            sprite.swim(pressed_key)
            sprite_group.draw(screen)


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
        self.shell_menu.update()

    def display_frame(self, screen):
        background.set_background(screen, self.show_menu)
        time_wait = False

        # for btn in sign_in.button_sign_in_list:
        #     if btn.isPressed():
        #         global USERNAME
        #         print(btn.get_btn_value())
        #         print(USERNAME)
        #         sign_in.display_sign_in(pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT]), btn.get_btn_value())
        #
        #         pygame.display.flip()

        # screen 1
        if self.display_screen_one:
            background.set_background(screen, "screen_1")
            time_wait = False

            self.screen_one.display_screen_one(screen)
            is_swimming = screen1_swim.swim_right(True)
            if is_swimming:
                screen1_swimming.draw(screen)
                screen1_swimming.update()
            else:
                # self.bubble_burst.play()
                bursting.update()
                bursting.draw(screen)

            bursting.draw(screen)

            # global TICKS
            TICKS = pygame.time.get_ticks()
            if TICKS > 3600:
                self.display_screen_one = False

        # screen 2
        elif self.display_screen_two:
            background.set_background(screen, "menu")
            time_wait = False

            self.screen_two.display_frame(screen)
            bubbles.update()
            for entity in all_sprites:
                screen.blit(entity.surf, entity.rect)

        # 1. Show menu
        elif self.show_menu:
            background.set_background(screen, "menu")
            time_wait = False

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

        elif self.display_sign_in:
            background.set_background(screen, "menu")
            time_wait = False

            sign_in.display_sign_in(screen, self.username)
            # for btn in sign_in.button_sign_in_list:
            #     if btn.isPressed():
            #         print("Luchi")
        # 3. Math Problem Screen
        else:
            # labels for each number
            label_1 = self.font.render(str(self.problem["num1"]), True, (127, 81, 0))
            label_2 = self.font.render(self.symbols[self.operation], True, (255, 255, 0))
            label_3 = self.font.render(str(self.problem["num2"]), True, (0, 122, 78))
            label_4 = self.font.render("  =  ", True, (254, 0, 154))

            label_5 = self.font.render("?", True, (242, 232, 213))


            # center the equation
            # t_w: total width
            t_w = label_1.get_width() + label_2.get_width() + label_3.get_width() + label_4.get_width() + label_5.get_width()
            pos_x = (SCREEN_WIDTH / 2) - (t_w / 2)

            screen.blit(label_1, (pos_x, 50))
            screen.blit(label_2, (pos_x + label_1.get_width(), 50))
            screen.blit(label_3, (pos_x + label_1.get_width() + label_2.get_width(), 50))
            screen.blit(label_4, (pos_x + label_1.get_width() + label_2.get_width() + label_3.get_width(), 50))
            screen.blit(label_5, (pos_x + label_1.get_width() + label_2.get_width() + label_3.get_width() + label_4.get_width(), 50))

            # buttons
            for btn in self.button_list:
                btn.draw(screen)

            screen.blit(self.shell_image, (SCREEN_WIDTH - 64 - 36, 24))

            # bubbles.update()
            sprite_group.update()
            sprite_group.draw(screen)

            pygame.display.update()

            if self.shell_menu_check:
                background.set_background(screen, "menu")
                time_wait = False

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
