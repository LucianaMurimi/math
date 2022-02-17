import random

import pygame.key
from bg import *
from menu import Menu
from button import Button
from bubble import *
from screen_1 import *
from sprite import *
from bubble_sprite import *
from sign_in import *
from button_level1 import *
from boy_sprite import *
from bee_sprite import *
from football_sprite import *
from butterfly_sprite import *
import time
from globals import *
from db import *


pygame.init()

# OBJECTS
background = Background()
db = DB()
sprite = Sprite(0, 80)
screen1_sprite = Sprite(200, 270)
screen1_bubble_sprite = BubbleSprite(500, 270)
boy_sprite = BoySprite(0, 260)
bee_sprite = BeeSprite(0, 228)
butterfly_sprite = ButterflySprite(SCREEN_WIDTH / 2 - 50, 360)
sign_in = SignIn()

# SPRITE GROUPS
all_sprites = pygame.sprite.Group()

sprite_group = pygame.sprite.Group()
sprite_group.add(sprite)

screen1_sprite_group = pygame.sprite.Group()
screen1_sprite_group.add(screen1_sprite)

screen1_bubble_sprite_group = pygame.sprite.Group()
screen1_bubble_sprite_group.add(screen1_bubble_sprite)

boy_sprite_group = pygame.sprite.Group()
boy_sprite_group.add(boy_sprite)

bee_sprite_group = pygame.sprite.Group()
bee_sprite_group.add(bee_sprite)

butterfly_sprite_group = pygame.sprite.Group()
butterfly_sprite_group.add(butterfly_sprite)

football_sprite_group = pygame.sprite.Group()

enemies = pygame.sprite.Group()
bubbles = pygame.sprite.Group()


class Game:
    # CUSTOM EVENTS
    ADDbubble = pygame.USEREVENT + 1
    pygame.time.set_timer(ADDbubble, 1000)

    def __init__(self):
        self.screen_one = ScreenOne()
        self.display_screen_one = True

        self.language_disp = "Kiswahili"
        self.language = "English"

        # menu
        self.screen_two = Menu(("Standard 1", "Standard 2", "--------------------", "Sign In", self.language_disp),
                               ttf_font="./assets/fonts/Sniglet-Regular.ttf", font_size=46)
        self.display_screen_two = True
        self.screen_two_kiswahili = None
        self.display_screen_two_kiswahili = False

        self.standard_one_menu = Menu(("Identifying missing numbers", "Counting objects"),
                                      ttf_font="./assets/fonts/Sniglet-Regular.ttf", font_size=36)

        self.standard_one_menu_kiswahili = Menu(("Kutambua nambari zinazokosekana", "Kuhesabu vitu"),
                                                ttf_font="./assets/fonts/Sniglet-Regular.ttf", font_size=36)
        self.display_standard_one_menu = False
        self.display_standard_one_menu_kiswahili = False
        self.display_standard_one_level = 0
        self.numbers_arr = []
        self.missing_num = None
        self.level1_buttons = []
        self.pos_x_missing = 0
        self.level2_buttons = []
        self.roll = False

        self.num_of_footballs = None

        self.standard_two_menu = Menu(("Addition", "Subtraction", "Multiplication"),
                                      ttf_font="./assets/fonts/Sniglet-Regular.ttf", font_size=56)
        self.standard_two_menu_kiswahili = Menu(("Nyongeza", "Kutoa", "Kuzidisha"),
                                      ttf_font="./assets/fonts/Sniglet-Regular.ttf", font_size=56)
        self.display_screen_two_menu = False
        self.display_standard_two_menu_kiswahili = False

        self.shell_menu = Menu(("SIGN IN", "BACK", "EXIT"), ttf_font="./assets/fonts/Sniglet-Regular.ttf", font_size=42)
        self.shell_menu_check = False

        self.display_sign_in = False

        # font
        self.font = pygame.font.Font("./assets/fonts/Sniglet-Regular.ttf", 42)
        self.score_font = pygame.font.Font("./assets/fonts/RosewellBlackRGH.otf", 20)

        self.display_ASD_game_screen = False
        # dictionary with keys: num1, num2, result
        # variables for creating the arithmetic problem
        self.problem = {"num1": 0, "num2": 0, "result": 0}
        self.symbols = {"addition": " + ", "subtraction": " - ", "multiplication": " x "}
        # variable for name of operation
        self.operation = ""
        self.button_list = ""

        self.reset_problem = False

        # score counter
        self.score = 0
        # counter for the number of problems
        self.count = 0

        self.shell_image = pygame.image.load("./assets/images/shell.png").convert_alpha()
        self.shell_rect = pygame.Rect(SCREEN_WIDTH - 64 - 36, 24, 72, 72)

        # sound effects
        # pygame.mixer.pre_init(44100, -16, 2, 2048)
        # pygame.mixer.init()
        # pygame.mixer.music.load("./assets/audio/intro.mp3")
        # pygame.mixer.music.play(1)

        self.sound_1 = pygame.mixer.Sound("./assets/audio/item1.ogg")
        self.sound_2 = pygame.mixer.Sound("./assets/audio/item2.ogg")
        self.gamestart_audio = pygame.mixer.Sound("./assets/audio/game start.mp3")
        self.bubble_burst = pygame.mixer.Sound("./assets/audio/bubble_burst.mp3")
        self.gameover_audio = pygame.mixer.Sound("./assets/audio/gameover.wav")
        self.wow = pygame.mixer.Sound("./assets/audio/wow.mp3")

        self.gamestart_audio.play()

        self.username = ""
        self.passwd = ""

    def process_events(self, screen):
        # EVENTS
        for event in pygame.event.get():
            # 1. quit game on EXIT
            if event.type == pygame.QUIT:
                return False

            #####################################################################
            # 2. MOUSE PRESS events
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not self.display_screen_two_menu and self.shell_rect.collidepoint(pygame.mouse.get_pos()):
                    self.shell_menu_check = not self.shell_menu_check

                if self.shell_menu_check:
                    if self.shell_menu.state == 0:
                        self.display_sign_in = not self.display_sign_in
                        pygame.display.update()

                if self.display_sign_in:
                    for btn in sign_in.button_sign_in_list:
                        btn_pressed = btn.isPressed()

                        if btn_pressed:
                            self.username = btn_pressed["username"]
                            self.passwd = btn_pressed["password"]

            #####################################################################
            # 3. KEY DOWN events -> check what screen the key down events are occurring -> update accordingly
            if event.type == pygame.KEYDOWN:
                # if SCREEN TWO - standard 1, standard 2
                if self.display_screen_two or self.display_screen_two_kiswahili:
                    if event.key == pygame.K_DOWN:
                        self.screen_two.update(key_press=pygame.K_DOWN, options=4)
                        if self.display_screen_two_kiswahili:
                            self.screen_two_kiswahili.update(key_press=pygame.K_DOWN, options=4)
                        pygame.display.flip()
                    elif event.key == pygame.K_UP:
                        self.screen_two.update(key_press=pygame.K_UP, options=4)
                        if self.display_screen_two_kiswahili:
                            self.screen_two_kiswahili.update(key_press=pygame.K_UP, options=4)
                        pygame.display.flip()

                    elif event.key == pygame.K_KP_ENTER:  # enter either standard 1 or standard 2 level
                        if self.screen_two.state == 0:
                            self.display_screen_two = False
                            self.display_standard_one_menu = True
                            pygame.time.wait(500)
                        elif self.screen_two.state == 1:
                            self.display_screen_two = False
                            self.display_screen_two_menu = True
                            pygame.time.wait(500)
                        elif self.screen_two.state == 3:
                            self.display_screen_two = False
                            self.display_sign_in = True

                        if self.display_screen_two_kiswahili:
                            if self.screen_two_kiswahili.state == 0:
                                self.display_screen_two_kiswahili = False
                                self.display_screen_two = False
                                self.display_standard_one_menu_kiswahili = True
                                pygame.time.wait(500)
                            elif self.screen_two_kiswahili.state == 1:
                                self.display_screen_two_kiswahili = False
                                self.display_screen_two = False
                                self.display_standard_two_menu_kiswahili = True
                                pygame.time.wait(500)
                            elif self.screen_two_kiswahili.state == 3:
                                self.display_screen_two_kiswahili = False
                                self.display_screen_two = False
                                self.display_sign_in = True
                            elif self.screen_two_kiswahili.state == 4:
                                self.language = "English"
                                self.language_disp = "Kiswahili"
                                self.display_screen_two_kiswahili = False
                                self.screen_two.state = 0
                                self.display_screen_two = True

                        elif self.screen_two.state == 4:
                            self.language = "Kiswahili"
                            self.language_disp = "English"
                            self.screen_two_kiswahili = (Menu(
                                ("Darasa la Kwanza", "Darasa la Pili", "--------------------", "Ingia",
                                 self.language_disp),
                                ttf_font="./assets/fonts/Sniglet-Regular.ttf", font_size=46))
                            self.display_screen_two_kiswahili = True

                # if STANDARD ONE MENU SCREEN - level 1 (ordering nos), level 2 (counting objects)
                elif self.display_standard_one_menu or self.display_standard_one_menu_kiswahili:
                    if event.key == pygame.K_DOWN:
                        if self.display_standard_one_menu:
                            self.standard_one_menu.update(key_press=pygame.K_DOWN, options=1)
                            pygame.display.flip()
                        else:
                            self.standard_one_menu_kiswahili.update(key_press=pygame.K_DOWN, options=1)
                            pygame.display.flip()
                    elif event.key == pygame.K_UP:
                        if self.display_standard_one_menu:
                            self.standard_one_menu.update(key_press=pygame.K_UP, options=1)
                            pygame.display.flip()
                        else:
                            self.standard_one_menu_kiswahili.update(key_press=pygame.K_UP, options=1)
                            pygame.display.flip()
                    elif event.key == pygame.K_KP_ENTER:  # enter either level 1 or level 2
                        if self.standard_one_menu.state == 0 or self.standard_one_menu_kiswahili.state == 0:
                            self.display_standard_one_level = 1
                            self.set_std1_level1_problem()
                            self.display_standard_one_menu = False
                            self.display_standard_one_menu_kiswahili = False
                            pygame.time.wait(500)

                        elif self.standard_one_menu.state == 1 or self.standard_one_menu_kiswahili.state == 1:
                            self.display_standard_one_level = 2
                            self.set_std1_level2_problem()
                            self.display_standard_one_menu = False
                            self.display_standard_one_menu_kiswahili = False
                            pygame.time.wait(500)

                # if STANDARD TWO MENU SCREEN - addition, subtraction, multiplication
                elif self.display_screen_two_menu or self.display_standard_two_menu_kiswahili:
                    if event.key == pygame.K_DOWN:
                        if self.display_screen_two_menu:
                            self.standard_two_menu.update(key_press=pygame.K_DOWN, options=2)
                            pygame.display.flip()
                        else:
                            self.standard_two_menu_kiswahili.update(key_press=pygame.K_DOWN, options=2)
                            pygame.display.flip()
                    elif event.key == pygame.K_UP:
                        if self.display_screen_two_menu:
                            self.standard_two_menu.update(key_press=pygame.K_UP, options=2)
                            pygame.display.flip()
                        else:
                            self.standard_two_menu_kiswahili.update(key_press=pygame.K_UP, options=2)
                            pygame.display.flip()

                    elif event.key == pygame.K_KP_ENTER:
                        if self.standard_two_menu.state == 0 or self.standard_two_menu_kiswahili.state == 0:
                            self.operation = "addition"
                            self.set_problem()
                            self.display_screen_two_menu = False
                            self.display_standard_two_menu_kiswahili = False

                        elif self.standard_two_menu.state == 1 or self.standard_two_menu_kiswahili.state == 1:
                            self.operation = "subtraction"
                            self.set_problem()
                            self.display_screen_two_menu = False
                            self.display_standard_two_menu_kiswahili = False

                        elif self.standard_two_menu.state == 2 or self.standard_two_menu_kiswahili.state == 2:
                            self.operation = "multiplication"
                            self.set_problem()
                            self.display_screen_two_menu = False
                            self.display_standard_two_menu_kiswahili = False


            #####################################################################
            # 4. ADDbubble Custom Event
            if event.type == self.ADDbubble and self.count == 3:
                # create the new bubble and add it to sprite groups
                new_bubble = Bubbles()
                bubbles.add(new_bubble)

            #####################################################################
            # 5. COLLISION EVENT
            if self.display_ASD_game_screen:
                enemy_collisions = pygame.sprite.spritecollide(sprite, enemies, pygame.sprite.collide_mask)
                for enemy in enemy_collisions:
                    enemy.bursting.update()
                    enemy.bursting.draw(screen)

                    if enemy.number == self.problem["result"]:
                        self.score += 5
                        global LEVEL2_SCORE
                        LEVEL2_SCORE = LEVEL2_SCORE + 5
                        if TABLENAME != "":
                            db.upload(0, self.score)
                        self.sound_1.play()

                        current_x = sprite.rect.x
                        current_y = sprite.rect.y
                        sprite.reposition(current_x, current_y)

                        self.reset_problem = True
                    else:
                        current_x = sprite.rect.x
                        current_y = sprite.rect.y
                        sprite.reposition(current_x, current_y)

                        self.reset_problem = True

            #####################################################################
            # 6. screen 1 COLLISION EVENT
            ## STANDARD 1 LEVEL 1
            global LEVEL1_SCORE
            if self.display_standard_one_level == 1:
                enemy_collisions = pygame.sprite.spritecollide(boy_sprite, enemies, pygame.sprite.collide_mask)
                for enemy in enemy_collisions:
                    current_x = enemy.rect.x
                    current_y = enemy.rect.y

                    if enemy.number == self.missing_num:
                        self.score += 5

                        LEVEL1_SCORE = LEVEL1_SCORE + 5
                        if TABLENAME != "":
                            db.upload(self.score, 0)
                        self.wow.play()

                        enemy.burst.kicking(current_x, self.pos_x_missing, current_y)

                        if self.pos_x_missing > current_x:
                            enemy.rect.move_ip((self.pos_x_missing - current_x + 48), -(current_y - 108 + 10))

                        elif self.pos_x_missing < current_x:
                            enemy.rect.move_ip(-(current_x - self.pos_x_missing - 48), -(current_y - 108 + 10))

                        enemy.bursting.draw(screen)

                    else:
                        ball_x = enemy.rect.x
                        while int(ball_x) < SCREEN_WIDTH:
                            enemy.rect.move_ip(ball_x + 5, 0)
                            ball_x = enemy.rect.x

                            enemy.burst.roll_off()
                            enemy.bursting.draw(screen)

                            pygame.display.update()
                            pygame.display.flip()

                    for enemy in enemies:
                        enemy.kill()

                    self.level2_buttons = []
                    self.missing_num = 0

                    current_x = boy_sprite.rect.x
                    current_y = boy_sprite.rect.y
                    boy_sprite.rect.move_ip(-(current_x), -(current_y - 260))

                    self.reset_problem = True

            ## STANDARD 1 LEVEL 2
            if self.display_standard_one_level == 2:
                enemy_collisions = pygame.sprite.spritecollide(bee_sprite, enemies, pygame.sprite.collide_mask)
                for enemy in enemy_collisions:
                    enemy.bursting.update()
                    enemy.bursting.draw(screen)

                    if enemy.number == self.num_of_footballs:
                        self.score += 5
                        LEVEL1_SCORE = LEVEL1_SCORE + 5
                        if TABLENAME != "":
                            db.upload(self.score, 0)
                        self.wow.play()
                        self.roll = True
                    else:
                        self.roll = True

        #####################################################################
        # 7. MOVE SPRITE based on pressed key
        pressed_key = pygame.key.get_pressed()
        if pressed_key[K_ESCAPE]:
            self.score = 0
            self.count = 0

            if self.display_standard_one_level == 1:
                self.display_standard_one_level = 0
                self.display_screen_two = False
                self.display_standard_one_menu = True
                self.score = 0
                self.count = 0

            if self.display_standard_one_level == 2:
                self.display_standard_one_level = 0
                self.display_screen_two = False
                self.display_standard_one_menu = True
                self.score = 0
                self.count = 0

            if self.display_standard_one_menu or self.display_screen_two_menu:
                if self.display_standard_one_menu:
                    self.display_standard_one_menu = False
                    self.display_screen_two = True
                elif self.display_screen_two_menu:
                    self.display_screen_two_menu = False
                    self.display_screen_two = True

            if self.display_ASD_game_screen:
                self.display_ASD_game_screen = False
                self.display_screen_two = False
                self.display_screen_two_menu = True
                self.score = 0
                self.count = 0

            if self.display_sign_in:
                self.display_sign_in = not self.display_sign_in
                self.display_screen_two_menu = True
                self.score = 0
                self.count = 0

            if SIGN_IN_EXIT:
                self.display_sign_in = False

        elif self.display_standard_one_level == 1:
            boy_sprite.run(pressed_key)
            boy_sprite_group.draw(screen)

        elif self.display_standard_one_level == 2:
            bee_sprite.fly(pressed_key)
            bee_sprite_group.draw(screen)

        elif self.display_ASD_game_screen:
            sprite.swim(pressed_key)
            sprite_group.draw(screen)

        return True

    #############################################################################
    def set_problem(self):
        self.display_ASD_game_screen = True
        if self.operation == "addition":
            self.addition()
        elif self.operation == "subtraction":
            self.subtraction()
        elif self.operation == "multiplication":
            self.multiplication()
        elif self.operation == "division":
            self.division()
        self.button_list = self.get_button_list()

    #############################################################################

    def set_std1_level1_problem(self):
        num = random.randint(1, 4)
        self.missing_num = random.randint(num, num + 4)
        self.numbers_arr = []

        for i in range(0, 5):
            if num == self.missing_num:
                self.numbers_arr.append("?")
                print("missing num", self.missing_num)
            else:
                self.numbers_arr.append(num)

            num = num + 1

        self.level1_buttons = self.get_level1_button_list()

    #############################################################################

    def set_std1_level2_problem(self):
        self.num_of_footballs = random.randint(1, 9)
        print("num of footballs: ", self.num_of_footballs)

        pos_x = (SCREEN_WIDTH / 2) - ((self.num_of_footballs * 64) + ((self.num_of_footballs - 1) * 16)) / 2
        for i in range(0, self.num_of_footballs):
            football_sprite_group.add(FootballSprite(pos_x, 300))
            pos_x = pos_x + 64 + 16

        self.level2_buttons = self.get_level2_button_list()

    #############################################################################
    def addition(self):
        a = random.randint(0, 10)
        b = random.randint(0, 10)
        self.problem["num1"] = a
        self.problem["num2"] = b
        self.problem["result"] = a + b
        self.operation = "addition"

    def subtraction(self):
        a = random.randint(0, 10)
        b = random.randint(0, 10)
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
        a = random.randint(0, 10)
        b = random.randint(0, 10)
        self.problem["num1"] = a
        self.problem["num2"] = b
        self.problem["result"] = a * b
        self.operation = "multiplication"

    #############################################################################

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

    #############################################################################
    def get_level1_button_list(self):
        # return a list with four buttons
        button_list = []

        # assign one of the buttons with the right answer
        choice = random.randint(1, 3)
        numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        numbers.remove(self.missing_num)

        # define the width and height
        width = 72
        height = 72

        pos_x = random.randint(276, 400)
        pos_y = random.randint(280, 380)

        if choice == 1:
            btn = ButtonLevel1(pos_x, pos_y, width, height, self.missing_num)
            button_list.append(btn)
            enemies.add(btn)
        else:
            btn = ButtonLevel1(pos_x, pos_y, width, height, numbers[random.randint(0, 2)])
            button_list.append(btn)
            enemies.add(btn)

        pos_x = random.randint(464, 588)
        pos_y = random.randint(280, 380)

        if choice == 2:
            btn = ButtonLevel1(pos_x, pos_y, width, height, self.missing_num)
            button_list.append(btn)
            enemies.add(btn)
        else:
            btn = ButtonLevel1(pos_x, pos_y, width, height, numbers[random.randint(3, 6)])
            button_list.append(btn)
            enemies.add(btn)

        pos_x = random.randint(652, 700)
        pos_y = random.randint(280, 380)

        if choice == 3:
            btn = ButtonLevel1(pos_x, pos_y, width, height, self.missing_num)
            button_list.append(btn)
            enemies.add(btn)
        else:
            btn = ButtonLevel1(pos_x, pos_y, width, height, numbers[random.randint(7, 8)])
            button_list.append(btn)
            enemies.add(btn)

        return button_list

    #############################################################################

    def get_level2_button_list(self):
        # return a list with three buttons
        button_list = []
        numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        numbers.remove(self.num_of_footballs)

        # assign one of the buttons with the right answer
        choice = random.randint(1, 3)

        # define the width and height
        width = 100
        height = 100

        pos_x = random.randint(100, 250)
        pos_y = random.randint(0, 100)

        if choice == 1:
            btn = Button(pos_x, pos_y, width, height, self.num_of_footballs)
            button_list.append(btn)
            enemies.add(btn)
        else:
            btn = Button(pos_x, pos_y, width, height, numbers[random.randint(0, 8)])
            button_list.append(btn)
            enemies.add(btn)

        pos_x = random.randint(350, 450)
        pos_y = random.randint(0, 100)

        if choice == 2:
            btn = Button(pos_x, pos_y, width, height, self.num_of_footballs)
            button_list.append(btn)
            enemies.add(btn)
        else:
            btn = Button(pos_x, pos_y, width, height, numbers[random.randint(0, 8)])
            button_list.append(btn)
            enemies.add(btn)

        pos_x = random.randint(550, 700)
        pos_y = random.randint(0, 100)

        if choice == 3:
            btn = Button(pos_x, pos_y, width, height, self.num_of_footballs)
            button_list.append(btn)
            enemies.add(btn)
        else:
            btn = Button(pos_x, pos_y, width, height, numbers[random.randint(0, 8)])
            button_list.append(btn)
            enemies.add(btn)

        return button_list

    ##############################################################################

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
        self.button_list = []

    #############################################################################

    def run_logic(self):
        if self.shell_menu_check:
            self.shell_menu.update()

    #############################################################################

    def display_frame(self, screen):
        background.set_background(screen, "screen_1")
        time_wait = False
        #############################################################################
        # screen 1
        if self.display_screen_one:
            background.set_background(screen, "screen_1")
            time_wait = False
            self.screen_one.display_screen_one(screen)

            screen1_sprite_group.draw(screen)
            screen1_bubble_sprite_group.draw(screen)

            screen1_sprite_group.update()
            screen1_sprite.swim_right()
            screen1_bubble_sprite.rect.move_ip(-5, 0)
            screen1_bubble_sprite.update()

            if pygame.sprite.spritecollide(screen1_sprite, screen1_bubble_sprite_group, pygame.sprite.collide_mask):
                self.display_screen_one = False

        #############################################################################

        # STANDARD ONE menu screen
        elif self.display_standard_one_menu:
            background.set_background(screen, "menu")
            time_wait = False

            self.standard_one_menu.display_frame(screen)
            bubbles.update()
            # for bubble in bubbles:
            #     screen.blit(bubble.surf, bubble.rect)

        elif self.display_standard_one_menu_kiswahili:
            background.set_background(screen, "menu")
            time_wait = False

            self.standard_one_menu_kiswahili.display_frame(screen)
        #############################################################################

        # ASD menu screen
        elif self.display_screen_two_menu:
            background.set_background(screen, "menu")
            time_wait = False

            self.standard_two_menu.display_frame(screen)

        #############################################################################

        # screen 2
        elif self.display_screen_two_kiswahili:
            background.set_background(screen, "menu")
            time_wait = False

            self.screen_two_kiswahili.display_frame(screen)

        elif self.display_standard_two_menu_kiswahili:
            background.set_background(screen, "menu")
            time_wait = False
            self.standard_two_menu_kiswahili.display_frame(screen)

        elif self.display_screen_two:
            background.set_background(screen, "menu")
            time_wait = False

            self.screen_two.display_frame(screen)
            bubbles.update()
            # for bubble in bubbles:
            #     screen.blit(bubble.surf, bubble.rect)

        #############################################################################

        # Game Over Screen
        elif self.count == 3:
            background.set_background(screen, "screen_1")

            # if the count gets to 5 that means that the game is over
            if self.language == "English":
                msg_1 = "Well Done!!!"
                msg_2 = "Your score is " + str(self.score)
            elif self.language == "Kiswahili":
                msg_1 = "Umefanya Vizuri!!!"
                msg_2 = "Alama yako ni " + str(self.score)

            self.display_message(screen, (msg_1, msg_2))

            self.display_screen_two_menu = True
            self.score = 0
            self.count = 0

            self.gameover_audio.play()
            time_wait = True

        #############################################################################
        # STANDARD 1 LEVEL 1 Game Screen
        elif self.display_standard_one_level == 1:
            background.set_background(screen, "standard1_level1")
            time_wait = False

            instruction_font = pygame.font.Font("./assets/fonts/Sniglet-Regular.ttf", 32)

            if self.language == "English":
                label_instruction = instruction_font.render("Kick the ball with the missing number !", True,
                                                            (254, 0, 154))
            elif self.language == "Kiswahili":
                label_instruction = instruction_font.render("Piga mpira ulio nambari inayokosekana !", True,
                                                            (254, 0, 154))

            label_instruction_w = label_instruction.get_width()

            pos_x = (SCREEN_WIDTH / 2) - (label_instruction_w / 2)
            screen.blit(label_instruction, (pos_x, 36))
            t_w = 0

            font = pygame.font.Font("./assets/fonts/Sniglet-Regular.ttf", 40)

            for i in range(4, -1, -1):
                if isinstance(self.numbers_arr[i], str):
                    label = font.render(self.numbers_arr[i], True, (255, 36, 0))
                    self.pos_x_missing = (SCREEN_WIDTH / 2) - ((t_w + label.get_width()) / 2) + label.get_width() + 64
                else:
                    label = font.render(str(self.numbers_arr[i]), True, (2, 83, 147))

                label_w = label.get_width() + 128
                t_w = t_w + label_w
                pos_x = (SCREEN_WIDTH / 2) - (t_w / 2) + label_w + 64
                screen.blit(label, (pos_x, 108))

                # buttons
                for btn in self.level1_buttons:
                    btn.draw(screen)

            boy_sprite_group.draw(screen)
            boy_sprite_group.update()

        #############################################################################

        # STANDARD 1 LEVEL 2 Game Screen
        elif self.display_standard_one_level == 2:
            background.set_background(screen, "standard1_level2")
            time_wait = False

            # butterfly_sprite_group.draw(screen)
            # butterfly_sprite.update()

            bee_sprite_group.draw(screen)
            bee_sprite.update()

            instruction_font = pygame.font.Font("./assets/fonts/Sniglet-Regular.ttf", 32)

            if self.language == "English":
                label_instruction = instruction_font.render("Pop the bubble with the correct number of balls !", True,
                                                        (254, 0, 154))
            elif self.language == "Kiswahili":
                label_instruction = instruction_font.render("Chopa kiputo kilicho idadi sahihi ya mipira !", True,
                                                            (254, 0, 154))

            label_instruction_w = label_instruction.get_width()

            pos_x = (SCREEN_WIDTH / 2) - (label_instruction_w / 2)
            screen.blit(label_instruction, (pos_x, 168))

            # buttons
            for btn in self.level2_buttons:
                btn.draw(screen)

            # football
            for ball in football_sprite_group:
                football_sprite_group.draw(screen)

            if self.roll:
                for ball in football_sprite_group:
                    ball.roll_right()

                    if ball.rect.x > SCREEN_WIDTH * 1.5:
                        for ball in football_sprite_group:
                            ball.kill()

                        self.level2_buttons = []

                        current_x = bee_sprite.rect.x
                        current_y = bee_sprite.rect.y
                        bee_sprite.rect.move_ip((current_x - current_x), -(current_y - 228))
                        self.roll = False
                        self.reset_problem = True

        #############################################################################

        # 3. ASD Game Screen
        elif self.display_ASD_game_screen:
            background.set_background(screen, "ASD_game_screen")
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
            screen.blit(label_5, (
                pos_x + label_1.get_width() + label_2.get_width() + label_3.get_width() + label_4.get_width(), 50))

            # buttons
            for btn in self.button_list:
                btn.draw(screen)

            screen.blit(self.shell_image, (SCREEN_WIDTH - 64 - 36, 24))

            # sprite
            sprite_group.draw(screen)
            sprite_group.update()

            pygame.display.update()

            if self.shell_menu_check:
                background.set_background(screen, "menu")
                time_wait = False

                self.shell_menu.display_frame(screen)
                pygame.display.update()

        #############################################################################
        # Sign In Screen
        elif self.display_sign_in:
            background.set_background(screen, "menu")
            time_wait = False

            sign_in.display_sign_in(screen, self.username, self.passwd)
        pygame.display.flip()

        #############################################################################

        # --- this is for the game to wait a few seconds to be able to show
        # --- what we have drawn before it change to another frame
        if self.reset_problem:
            # wait 1 second
            if self.display_standard_one_level == 2:
                self.set_std1_level2_problem()
                self.count += 1
                self.reset_problem = False
            elif self.display_standard_one_level == 1:
                pygame.time.wait(2000)
                self.set_std1_level1_problem()
                self.count += 1
                self.reset_problem = False
            else:
                pygame.time.wait(1000)
                self.set_problem()
                # increase count by 1
                self.count += 1
                self.reset_problem = False
        elif time_wait:
            # wait three seconds
            pygame.time.wait(4000)

    #############################################################################

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
