import json

import pygame
from globals import *
from buttons_sign_in import *


class SignIn:
    def __init__(self, ttf_font="./assets/fonts/Sniglet-Regular.ttf", font_size=32):
        self.font = pygame.font.Font(ttf_font, font_size)

        self.button_q = ButtonSignIn(62, 182, "q")
        self.button_w = ButtonSignIn(130, 182, "w")
        self.button_e = ButtonSignIn(198, 182, "e")
        self.button_r = ButtonSignIn(266, 182, "r")
        self.button_t = ButtonSignIn(334, 182, "t")
        self.button_y = ButtonSignIn(402, 182, "y")
        self.button_u = ButtonSignIn(470, 182, "u")
        self.button_i = ButtonSignIn(538, 182, "i")
        self.button_o = ButtonSignIn(606, 182, "o")
        self.button_p = ButtonSignIn(674, 182, "p")

        self.button_a = ButtonSignIn(62, 250, "a")
        self.button_s = ButtonSignIn(130, 250, "s")
        self.button_d = ButtonSignIn(198, 250, "d")
        self.button_f = ButtonSignIn(266, 250, "f")
        self.button_g = ButtonSignIn(334, 250, "g")
        self.button_h = ButtonSignIn(402, 250, "h")
        self.button_j = ButtonSignIn(470, 250, "j")
        self.button_k = ButtonSignIn(538, 250, "k")
        self.button_l = ButtonSignIn(606, 250, "l")
        self.button__ = ButtonSignIn(674, 250, "_")

        self.button_z = ButtonSignIn(96, 318, "z")
        self.button_x = ButtonSignIn(164, 318, "x")
        self.button_c = ButtonSignIn(232, 318, "c")
        self.button_v = ButtonSignIn(300, 318, "v")
        self.button_b = ButtonSignIn(368, 318, "b")
        self.button_n = ButtonSignIn(436, 318, "n")
        self.button_m = ButtonSignIn(504, 318, "m")
        self.button_backspace = ButtonSignIn(572, 318, "clear")
        self.button_enter = ButtonSignIn(640, 318, "enter")

        self.button_0 = ButtonSignIn(62, 394, 0)
        self.button_1 = ButtonSignIn(130, 394, 1)
        self.button_2 = ButtonSignIn(198, 394, 2)
        self.button_3 = ButtonSignIn(266, 394, 3)
        self.button_4 = ButtonSignIn(334, 394, 4)
        self.button_5 = ButtonSignIn(402, 394, 5)
        self.button_6 = ButtonSignIn(470, 394, 6)
        self.button_7 = ButtonSignIn(538, 394, 7)
        self.button_8 = ButtonSignIn(606, 394, 8)
        self.button_9 = ButtonSignIn(674, 394, 9)

        self.button_sign_in_list = [self.button_q, self.button_w, self.button_e, self.button_r, self.button_t,
                                    self.button_y, self.button_u, self.button_i, self.button_o, self.button_p,
                                    self.button_a, self.button_s, self.button_d, self.button_f, self.button_g,
                                    self.button_h, self.button_j, self.button_k, self.button_l, self.button__,
                                    self.button_z,
                                    self.button_x, self.button_c, self.button_v, self.button_b, self.button_n,
                                    self.button_m, self.button_backspace, self.button_enter, self.button_0,
                                    self.button_1, self.button_2, self.button_3, self.button_4, self.button_5,
                                    self.button_6, self.button_7, self.button_8, self.button_9]

    def display_sign_in(self, screen, email_input, passwd_input):
        email_label = self.font.render("Email: ", True, BLACK)
        passwd_label = self.font.render("Password: ", True, BLACK)

        email_input_label = self.font.render(email_input, True, BLACK)
        password_input_label = self.font.render(passwd_input, True, BLACK)

        email_width = email_label.get_width()
        passwd_width = passwd_label.get_width()

        email_height = email_label.get_height()
        passwd_height = passwd_label.get_height()

        pos_y = 300

        screen.blit(email_label, (100, 50))
        screen.blit(passwd_label, (100, 50 + email_height))
        screen.blit(email_input_label, (100 + email_width + 20, 50))
        screen.blit(password_input_label, (100 + passwd_width + 20, 50 + email_height))

        for btn in self.button_sign_in_list:
            btn.draw(screen)
        pygame.display.flip()

        return False

