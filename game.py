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

pygame.init()

# OBJECTS
background = Background()
sprite = Sprite()
screen1_sprite = Sprite()
screen1_bubble_sprite = BubbleSprite(SCREEN_WIDTH / 2 - 50, 270)
sign_in = SignIn()

# SPRITE GROUPS
all_sprites = pygame.sprite.Group()

sprite_group = pygame.sprite.Group()
sprite_group.add(sprite)

screen1_sprite_group = pygame.sprite.Group()
screen1_sprite_group.add(screen1_sprite)

screen1_bubble_sprite_group = pygame.sprite.Group()
screen1_bubble_sprite_group.add(screen1_bubble_sprite)

enemies = pygame.sprite.Group()
bubbles = pygame.sprite.Group()


class Game:
    # CUSTOM EVENTS
    ADDbubble = pygame.USEREVENT + 1
    pygame.time.set_timer(ADDbubble, 5000)

    def __init__(self):
        self.screen_one = ScreenOne()
        self.display_screen_one = True

        # menu
        self.screen_two = Menu(("Standard 1", "Standard 2"),
                               ttf_font="./assets/fonts/Sniglet-Regular.ttf", font_size=64)
        self.display_screen_two = True

        self.standard_one_menu = Menu(("Level 1", "Level 2"),
                                      ttf_font="./assets/fonts/Sniglet-Regular.ttf", font_size=56)
        self.display_standard_one_menu = False
        self.display_standard_one_level = 0
        self.numbers_arr = []
        self.missing_num = None
        self.level1_buttons = []

        self.standard_two_menu = Menu(("Addition", "Subtraction", "Multiplication"),
                                      ttf_font="./assets/fonts/Sniglet-Regular.ttf", font_size=56)
        self.display_standard_two_menu = False

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

            #####################################################################
            # 2. MOUSE PRESS events
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not self.display_standard_two_menu and self.shell_rect.collidepoint(pygame.mouse.get_pos()):
                    self.shell_menu_check = not self.shell_menu_check

                if self.shell_menu_check:
                    if self.shell_menu.state == 0:
                        self.display_sign_in = not self.display_sign_in
                        pygame.display.update()

                if self.display_sign_in:
                    for btn in sign_in.button_sign_in_list:
                        if btn.isPressed():
                            self.username = self.username + btn.get_btn_value()

                            sign_in.display_sign_in(pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT]),
                                                    self.username)
                            pygame.display.flip()

            #####################################################################
            # 3. KEY DOWN events -> check what screen the key down events are occurring -> update accordingly
            if event.type == pygame.KEYDOWN:
                # if SCREEN TWO - standard 1, standard 2
                if self.display_screen_two:
                    if event.key == pygame.K_DOWN:
                        self.screen_two.update(key_press=pygame.K_DOWN, options=1)
                        pygame.display.flip()
                    elif event.key == pygame.K_UP:
                        self.screen_two.update(key_press=pygame.K_UP, options=1)
                        pygame.display.flip()

                    elif event.key == pygame.K_KP_ENTER:  # enter either standard 1 or standard 2 level
                        if self.screen_two.state == 0:
                            self.display_screen_two = False
                            self.display_standard_one_menu = True
                            pygame.time.wait(500)
                        elif self.screen_two.state == 1:
                            self.display_screen_two = False
                            self.display_standard_two_menu = True
                            pygame.time.wait(500)

                # if STANDARD ONE MENU SCREEN - level 1 (ordering nos), level 2 (counting objects)
                if self.display_standard_one_menu:
                    if event.key == pygame.K_DOWN:
                        self.standard_one_menu.update(key_press=pygame.K_DOWN, options=1)
                        pygame.display.flip()
                    elif event.key == pygame.K_UP:
                        self.standard_one_menu.update(key_press=pygame.K_UP, options=1)
                        pygame.display.flip()
                    elif event.key == pygame.K_KP_ENTER:  # enter either level 1 or level 2
                        if self.standard_one_menu.state == 0:
                            self.display_standard_one_level = 1
                            self.set_std1_level1_problem()
                            self.display_standard_one_menu = False
                            pygame.time.wait(500)
                        elif self.standard_one_menu.state == 1:
                            self.display_standard_one_level = 2
                            self.display_standard_one_menu = False
                            pygame.time.wait(500)

                # if STANDARD TWO MENU SCREEN - addition, subtraction, multiplication
                if self.display_standard_two_menu:
                    if event.key == pygame.K_DOWN:
                        self.standard_two_menu.update(key_press=pygame.K_DOWN, options=2)
                        pygame.display.flip()
                    elif event.key == pygame.K_UP:
                        self.standard_two_menu.update(key_press=pygame.K_UP, options=2)
                        pygame.display.flip()

                    elif event.key == pygame.K_KP_ENTER:
                        if self.standard_two_menu.state == 0:
                            self.operation = "addition"
                            self.set_problem()
                            self.display_standard_two_menu = False
                        elif self.standard_two_menu.state == 1:
                            self.operation = "subtraction"
                            self.set_problem()
                            self.display_standard_two_menu = False
                        elif self.standard_two_menu.state == 2:
                            print(self.standard_two_menu.state)
                            self.operation = "multiplication"
                            self.set_problem()
                            self.display_standard_two_menu = False

            #####################################################################
            # 4. ADDbubble Custom Event
            if event.type == self.ADDbubble:
                # create the new bubble and add it to sprite groups
                new_bubble = Bubbles()
                bubbles.add(new_bubble)

            #####################################################################
            # 5. COLLISION EVENT
            if self.display_ASD_game_screen:
                enemy_collisions = pygame.sprite.spritecollide(sprite, enemies, pygame.sprite.collide_mask)
                for enemy in enemy_collisions:
                    print(enemy.number)
                    enemy.bursting.update()
                    enemy.bursting.draw(screen)

                    if enemy.number == self.problem["result"]:
                        self.score += 5
                        self.sound_1.play()
                        self.reset_problem = True

            #####################################################################
            # 6. screen 1 COLLISION EVENT
            if pygame.sprite.spritecollide(screen1_sprite, screen1_bubble_sprite_group, pygame.sprite.collide_mask):
                screen1_bubble_sprite_group.update()
                screen1_bubble_sprite_group.draw(screen)
                self.display_screen_one = False

        #####################################################################
        # 7. MOVE SPRITE based on pressed key
        pressed_key = pygame.key.get_pressed()
        if pressed_key[K_ESCAPE]:
            self.score = 0
            self.count = 0
            self.display_screen_two = True
            self.display_standard_one_level = 0

        else:
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

        for i in range(0, 5):
            if num == self.missing_num:
                self.numbers_arr.append("?")
                print("missing num", self.missing_num)
            else:
                self.numbers_arr.append(num)

            num = num + 1

        self.level1_buttons = self.get_level1_button_list()

    #############################################################################
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
        choice = random.randint(1, 4)

        # define the width and height
        width = 72
        height = 72

        pos_x = random.randint(100, 300)
        pos_y = random.randint(150, 240)

        if choice == 1:
            btn = ButtonLevel1(pos_x, pos_y, width, height, self.missing_num)
            button_list.append(btn)
            enemies.add(btn)
        else:
            btn = ButtonLevel1(pos_x, pos_y, width, height, random.randint(1, 9))
            button_list.append(btn)
            enemies.add(btn)

        pos_x = random.randint(500, 700)
        pos_y = random.randint(150, 240)

        if choice == 2:
            btn = ButtonLevel1(pos_x, pos_y, width, height, self.missing_num)
            button_list.append(btn)
            enemies.add(btn)
        else:
            btn = ButtonLevel1(pos_x, pos_y, width, height, random.randint(1, 9))
            button_list.append(btn)
            enemies.add(btn)

        pos_x = random.randint(100, 300)
        pos_y = random.randint(340, 380)

        if choice == 3:
            btn = ButtonLevel1(pos_x, pos_y, width, height, self.missing_num)
            button_list.append(btn)
            enemies.add(btn)
        else:
            btn = ButtonLevel1(pos_x, pos_y, width, height, random.randint(1, 9))
            button_list.append(btn)
            enemies.add(btn)

        pos_x = random.randint(500, 700)
        pos_y = random.randint(340, 380)

        if choice == 4:
            btn = ButtonLevel1(pos_x, pos_y, width, height, self.missing_num)
            button_list.append(btn)
            enemies.add(btn)
        else:
            btn = ButtonLevel1(pos_x, pos_y, width, height, random.randint(1, 9))
            button_list.append(btn)
            enemies.add(btn)

        return button_list

    #############################################################################
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

        #############################################################################

        # screen 2
        elif self.display_screen_two:
            background.set_background(screen, "menu")
            time_wait = False

            self.screen_two.display_frame(screen)
            bubbles.update()
            for bubble in bubbles:
                screen.blit(bubble.surf, bubble.rect)

        #############################################################################

        # STANDARD ONE menu screen
        elif self.display_standard_one_menu:
            background.set_background(screen, "menu")
            time_wait = False

            self.standard_one_menu.display_frame(screen)
            bubbles.update()
            for bubble in bubbles:
                screen.blit(bubble.surf, bubble.rect)

        #############################################################################

        # ASD menu screen
        elif self.display_standard_two_menu:
            background.set_background(screen, "menu")
            time_wait = False

            self.standard_two_menu.display_frame(screen)

        #############################################################################

        # Game Over Screen
        elif self.count == 3:
            # if the count gets to 5 that means that the game is over
            msg_1 = "You answered " + str(self.score / 5) + " correctly"
            msg_2 = "Your score was " + str(self.score)
            self.display_message(screen, (msg_1, msg_2))

            self.display_standard_two_menu = True
            self.score = 0
            self.count = 0

            time_wait = True

        #############################################################################
        # Sign In Screen
        elif self.display_sign_in:
            background.set_background(screen, "menu")
            time_wait = False

            sign_in.display_sign_in(screen, self.username)

        #############################################################################
        # STANDARD 1 LEVEL 1 Game Screen
        elif self.display_standard_one_level == 1:
            background.set_background(screen, "standard1_level1")
            time_wait = False

            label_instruction = self.font.render("Pop the bubble with the missing number !", True, (254, 0, 154))
            label_instruction_w = label_instruction.get_width()

            pos_x = (SCREEN_WIDTH / 2) - (label_instruction_w / 2)
            screen.blit(label_instruction, (pos_x, 36))
            t_w = 0

            font = pygame.font.Font("./assets/fonts/Sniglet-Regular.ttf", 56)

            for i in range(4, -1, -1):
                if isinstance(self.numbers_arr[i], str):
                    label = font.render(self.numbers_arr[i], True, (255, 36, 0))
                else:
                    label = font.render(str(self.numbers_arr[i]), True, (15, 157, 8))

                label_w = label.get_width() + 128
                t_w = t_w + label_w
                pos_x = (SCREEN_WIDTH / 2) - (t_w / 2) + label_w + 64
                screen.blit(label, (pos_x, 108))

                # buttons
                for btn in self.level1_buttons:
                    btn.draw(screen)

        #############################################################################

        # STANDARD 1 LEVEL 2 Game Screen
        elif self.display_standard_one_level == 2:
            background.set_background(screen, "standard1_level2")
            time_wait = False

            label_instruction = self.font.render("How many rabbits are there !", True, (254, 0, 154))
            label_instruction_w = label_instruction.get_width()

            pos_x = (SCREEN_WIDTH / 2) - (label_instruction_w / 2)
            screen.blit(label_instruction, (pos_x, 36))

        #############################################################################

        # 3. ASD Game Screen
        else:
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

        pygame.display.flip()

        #############################################################################

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
