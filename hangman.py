from settings import *
import customtkinter as ck
import random


class Initialization:
    def __init__(self):
        ck.set_appearance_mode("dark")
        ck.set_default_color_theme("blue")

        self.window = ck.CTk()
        self.window.title("Hangman")
        self.window.geometry(f"{MAIN_WIDTH}x{MAIN_HEIGHT}")
        self.window.minsize(MAIN_WIDTH, MAIN_HEIGHT)
        self.window.rowconfigure(0, weight=1)
        self.window.columnconfigure(0, weight=1)

        self.word_list = []
        self.new_word_list = []
        self.keyboard_buttons = {}
        self.custom = "Custom"
        self.used_letters = set()
        self.word_variable = ck.StringVar()
        self.result_variable = ck.StringVar(value="")
        self.current_difficulty = ck.StringVar(value="Normal")
        self.new_difficulty = ck.StringVar(value="Normal")
        self.custom_min_var = ck.StringVar(value=DIFFICULTY[self.custom][0])
        self.custom_max_var = ck.StringVar(value=DIFFICULTY[self.custom][1])
        self.lives_checkbox_var = ck.StringVar(value="off")
        self.status = STATUS[0]
        self.lives = NUMBER_OF_LIVES
        self.custom_lives = self.lives
        self.lives_checkbox_is_on = False
        self.round = 1
        self.rounds_won = 0
        self.is_lost = False
        self.slider_used = False


class CreateBase(Initialization):
    def __init__(self):
        super().__init__()


    def create_frames(self):
        self.word_frame = ck.CTkFrame(self.window, fg_color=BACKGROUND_COLOR)
        self.word_frame.grid(row=0, column=0, sticky="nesw")

        self.keyboard_frame = ck.CTkFrame(self.window, fg_color=BACKGROUND_COLOR)
        self.keyboard_frame.grid(row=1, column=0, sticky="nesw")

        self.side_frame = ck.CTkFrame(self.window, fg_color=SIDE_BAR_COLOR)
        self.side_frame.grid(row=0, column=1, rowspan=2, sticky="nesw")


    def create_word_labels(self):
        word_label = ck.CTkLabel(self.word_frame, textvariable=self.word_variable, 
                                 text_font=WORD_FONT)
        word_label.grid(row=0, column=0)
        word_label.place(relx=0.5, rely=0.5, anchor=ck.CENTER)

        self.result_label = ck.CTkLabel(self.word_frame, textvariable=self.result_variable,
                                        text_font=RESULT_FONT, text_color=BACKGROUND_COLOR)
        self.result_label.grid(row=0, column=0)
        self.result_label.place(relx=0.5, rely=0.8, anchor=ck.CENTER)


    def create_side_labels(self):
        self.round_label = ck.CTkLabel(self.side_frame, 
                                       text=f"Round {self.round}", 
                                       text_font=KEYBOARD_FONT)
        self.round_label.grid(row=1, column=0, pady=(10, 0)) 

        self.lives_text_label = ck.CTkLabel(self.side_frame, 
                                            text=f"Lives: {self.lives}", 
                                            text_font=KEYBOARD_FONT)
        self.lives_text_label.grid(row=2, column=0, pady=(0, 30))

        difficulty_label = ck.CTkLabel(self.side_frame, 
                                       textvariable=self.current_difficulty, 
                                       text_font=KEYBOARD_FONT)
        difficulty_label.grid(row=3, column=0, padx=10)

        self.rounds_won_label = ck.CTkLabel(self.side_frame, 
                                       text=f"Won: {self.rounds_won}", 
                                       text_font=KEYBOARD_FONT)
        self.rounds_won_label.grid(row=4, column=0, padx=10)


class PlayGame(CreateBase):
    def __init__(self):
        super().__init__()

    
    def load_word_list(self):
        try:
            with open("word_list.txt", "r") as file:
                words = file.readlines()
            for word in words:
                word = word.rstrip("\n").upper()
                self.word_list.append(word)
        except:
            print("Missing file")

    
    def play_game(self):
        self.initialize_game()
        self.get_word()
        self.show_result()


    def initialize_game(self):
        self.new_word_list = []
        self.used_letters = set()
        self.status = STATUS[0]

        if self.is_lost == True:
            self.round = 1
            self.rounds_won = 0
            self.is_lost = False
        if self.lives_checkbox_is_on == False or self.lives == 0:
            self.lives = self.custom_lives
        self.lives_text_label.configure(text=f"Lives: {self.lives}")

        for letter in self.keyboard_buttons:
            self.keyboard_buttons[letter].configure(fg_color=DARK_BLUE, state=ck.NORMAL)
        self.round_label.configure(text=f"Round {self.round}")
        self.round +=1


    def get_word(self):
        for word in self.word_list:
            if (len(word) >= DIFFICULTY[self.current_difficulty.get()][0]
                    and len(word) <= DIFFICULTY[self.current_difficulty.get()][1]):
                self.new_word_list.append(word)
        self.secret_word = random.choice(self.new_word_list)
        new_word = "_ " * len(self.secret_word)
        self.word_variable.set(new_word.strip())
        # print(f"{self.secret_word} ({len(self.secret_word)})")


    def update_word(self, letter):
        word = self.word_variable.get().split(" ")
        for index, char in enumerate(self.secret_word):
            if letter == char:
                word[index] = letter
        self.word_variable.set(" ".join(word))
        self.update_lives(word, letter)


    def update_lives(self, word, letter):
        if letter not in self.used_letters and self.status == STATUS[0]:
            self.used_letters.add(letter)
            if letter not in self.secret_word:
                self.lives -= 1
            self.lives_text_label.configure(text=f"Lives: {self.lives}")
            self.keyboard_buttons[letter].configure(fg_color=DISABLED_BUTTON_COLOR, 
                                                    state=ck.DISABLED)
        self.update_result(word)

        
    def update_result(self, word):
        if self.lives == 0:
            self.status = STATUS[1]
            self.word_variable.set(" ".join([letter for letter in self.secret_word]))
        elif set(word).issubset(self.used_letters):
            self.status = STATUS[2]
        if self.status != STATUS[0]:
            for letter in self.keyboard_buttons:
                self.keyboard_buttons[letter].configure(state=ck.DISABLED)
            self.show_result()


    def show_result(self):
        if self.status == STATUS[1]:
            self.result_variable.set("You Lost!")
            self.result_label.configure(text_color=RED)
            self.is_lost = True
        elif self.status == STATUS[2]:
            self.result_variable.set("You Won!")
            self.result_label.configure(text_color=GREEN)
            self.rounds_won += 1
        else:
            self.result_variable.set("")
        self.rounds_won_label.configure(text=f"Won: {self.rounds_won}")


class MainWindow(PlayGame):     
    def create_button(self, frame, text, row, column, font, command):
        button = ck.CTkButton(frame, text=text, border_width=BORDER_WIDTH,
                              corner_radius=BUTTON_CORNER_RADIUS, text_font=font,
                              command=command)
        button.grid(row=row, column=column)
        return button


    def create_keyboard_buttons(self):
        row, column = 0, 0
        for letter in ALPHABET:
            if column == len(ALPHABET)/2:
                row += 1
                column = 0
            self.keyboard_buttons[letter] = self.create_button(self.keyboard_frame,
                                                               text=letter, 
                                                               row=row, column=column,
                                                               font=KEYBOARD_FONT, 
                                                               command= lambda letter=letter: 
                                                               self.update_word(letter))
            self.keyboard_buttons[letter].configure(height=BUTTON_HEIGHT)
            self.keyboard_frame.columnconfigure(column, weight=1)
            column += 1


    def create_side_buttons(self):
        new_game_button = self.create_button(self.side_frame, text="New Game", 
                                             row=0, column=0, font=KEYBOARD_FONT, 
                                             command=self.play_game)
        new_game_button.configure(fg_color=GREEN, text_color=INNER_TEXT_COLOR, 
                                  hover_color=GREEN_HOVER_COLOR)
        new_game_button.grid_configure(pady=(10, 0))  

        settings_button = self.create_button(self.side_frame, text="Settings", 
                                             row=5, column=0, font=KEYBOARD_FONT, 
                                             command=self.settings)
        settings_button.configure(fg_color=SETTINGS_COLOR, text_color=INNER_TEXT_COLOR, 
                                  hover_color=SETTINGS_COLOR)
        settings_button.grid_configure(pady=(15, 20))

        quit_button = self.create_button(self.side_frame, text="Quit",
                                         row=6, column=0, 
                                         font=KEYBOARD_FONT, 
                                         command=self.window.quit)
        quit_button.configure(fg_color=RED, text_color=INNER_TEXT_COLOR, 
                              hover_color=RED_HOVER_COLOR)


class SettingsWindow(MainWindow):
    def __init__(self):
        super().__init__()


    def settings(self):
        self.settings_window = ck.CTkToplevel()
        self.settings_window.geometry(f"{SETTINGS_WIDTH}x{SETTINGS_HEIGHT}")
        self.settings_window.minsize(SETTINGS_WIDTH, SETTINGS_HEIGHT)
        self.settings_window.maxsize(SETTINGS_WIDTH, SETTINGS_HEIGHT)
        self.settings_window.title("Settings")
        
        self.create_settings_labels()
        self.create_difficulty_list()
        self.create_custom_option()
        self.create_lives_checkbox()
        self.create_lives_slider()
        self.create_save_button()
        self.show_custom_lives()
        self.track_difficulty()

        self.current_min = self.custom_min_var.get()
        self.current_max = self.custom_max_var.get()


    def create_settings_labels(self):
        select_text = ck.CTkLabel(self.settings_window, text="Select Difficulty: ",
                                  text_font=KEYBOARD_FONT)
        select_text.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        lives_text = ck.CTkLabel(self.settings_window, text="Select Number Of Lives: ",
                                 text_font=KEYBOARD_FONT)
        lives_text.grid(row=6, column=0, padx=10, pady=20, sticky="w")


    def create_difficulty_list(self):
        row, column = 1, 0
        for key in DIFFICULTY.keys():
            min_length = DIFFICULTY[key][0]
            max_length = DIFFICULTY[key][1]
            if key != self.custom:
                text = f"{key}:  {min_length}-{max_length} letter word"
            else: text = f"{key}: "

            difficulty_radio = ck.CTkRadioButton(self.settings_window, 
                                                 text=text, value=key,
                                                 variable=self.new_difficulty, 
                                                 text_font=SETTINGS_FONT,
                                                 command=self.track_difficulty)
            difficulty_radio.grid(row=row, column=column, padx=20, pady=5, sticky="w")
            row += 1


    def create_option_menu(self, variable, length, column, command):
        option_menu = ck.CTkOptionMenu(self.settings_window, width=60, values=length,
                                       variable=variable, text_font=DROPDOWN_FONT,
                                       dynamic_resizing=False, command=command)
        option_menu.grid(row=4, column=column)
        return option_menu


    def create_custom_option(self):
        row, column = 5, 0
        length = [str(num) for num in range(1, MAX_WORD_LENGTH+1)]
        self.custom_min = self.create_option_menu(variable=self.custom_min_var,
                                                  length=length, column=0, 
                                                  command=self.set_custom_option_min)
        self.custom_min.grid_configure(row=row, column=column, padx=120, sticky="w")

        custom_dash = ck.CTkLabel(self.settings_window, text="-", width=1,
                                  text_font=KEYBOARD_FONT)
        custom_dash.grid(row=row, column=column, padx=185, sticky="w")

        self.custom_max = self.create_option_menu(variable=self.custom_max_var, 
                                                  length=length, column=2,
                                                  command=self.set_custom_option_max)
        self.custom_max.grid_configure(row=row, column=column, padx=200, sticky="w")

        custom_text = ck.CTkLabel(self.settings_window, text="letter word", width=1, 
                                  text_font=SETTINGS_FONT)
        custom_text.grid(row=row, column=column, padx=265, sticky="w")


    def create_lives_checkbox(self):
        self.lives_checkbox = ck.CTkCheckBox(self.settings_window, text="Cumulative",
                                             variable=self.lives_checkbox_var,
                                             text_font=SETTINGS_FONT,
                                             command=self.update_lives_checkbox)
        self.lives_checkbox.grid(row=6, column=0, padx=300, pady=(5, 0), sticky="w")

        if self.lives_checkbox_is_on == True:
            self.lives_checkbox.select()
        else:
            self.lives_checkbox.deselect()


    def create_lives_slider(self):
        lives_slider = ck.CTkSlider(self.settings_window, width=SLIDER_WIDTH,
                                    from_=CUSTOM_LIVES[0], to=CUSTOM_LIVES[1],
                                    command=self.update_custom_lives)
        lives_slider.grid(row=7, column=0, padx=30, sticky="w")
        lives_slider.set(self.lives)

        lives_min = ck.CTkLabel(self.settings_window, text=f"{CUSTOM_LIVES[0]}", width=1,
                                text_font=DROPDOWN_FONT)
        lives_min.grid(row=7, column=0, padx=20, sticky="w")

        lives_max = ck.CTkLabel(self.settings_window, text=f"{CUSTOM_LIVES[1]}", width=1,
                                text_font=DROPDOWN_FONT)
        lives_max.grid(row=7, column=0, padx=330, sticky="w")


    def update_lives_checkbox(self):
        if self.lives_checkbox_var.get() == "1":
            self.lives_checkbox_is_on = True
        else:
            self.lives_checkbox_is_on = False


    def update_custom_lives(self, lives):
        self.slider_used = True
        self.lives = int(lives)
        self.lives_label.configure(text=f"[ {self.lives} ]")


    def show_custom_lives(self):
        self.lives_label = ck.CTkLabel(self.settings_window, text=f"[ {self.lives} ]", width=1,
                                       text_font=SETTINGS_FONT, relief=ck.RIDGE)
        self.lives_label.grid(row=6, column=0, padx=230, pady=5, sticky="w")


    def track_difficulty(self):
        if self.new_difficulty.get() != self.custom:
            self.custom_min.configure(state=ck.DISABLED)
            self.custom_max.configure(state=ck.DISABLED)
        else:
            self.custom_min.configure(state=ck.NORMAL)
            self.custom_max.configure(state=ck.NORMAL)


    def set_custom_option_min(self, choice):
        DIFFICULTY[self.custom][0] = int(choice)
        length = [str(num) for num in range(int(choice), MAX_WORD_LENGTH+1)]
        self.custom_max.configure(values=length)


    def set_custom_option_max(self, choice):
        DIFFICULTY[self.custom][1] = int(choice)
        length = [str(num) for num in range(1, int(choice)+1)]
        self.custom_min.configure(values=length)


    def create_save_button(self):
        save_button = self.create_button(self.settings_window, text="Save",
                                         row=11, column=0, font=KEYBOARD_FONT,
                                         command=self.save_settings)
        save_button.configure(fg_color=GREEN, text_color=INNER_TEXT_COLOR, 
                              hover_color=GREEN_HOVER_COLOR)
        save_button.grid_configure(padx=140, pady=(10, 0), sticky="w")


    def save_settings(self):
        if self.current_difficulty.get() != self.new_difficulty.get():
            self.current_difficulty.set(self.new_difficulty.get())
            self.play_game()
        elif (self.current_min != self.custom_min_var.get() or
                self.current_max != self.custom_max_var.get()):
            self.current_min = self.custom_min_var.get()
            self.current_max = self.custom_max_var.get()
            self.play_game()
        if self.custom_lives != self.lives and self.slider_used == True:
            self.custom_lives = self.lives
            self.lives_text_label.configure(text=f"Lives: {self.custom_lives}")
            self.round = 1
            self.rounds_won = 0
            self.play_game()      
        self.update_lives_checkbox()
        self.settings_window.withdraw()
        self.slider_used = False
        

class Hangman(SettingsWindow):
    def __init__(self):
        super().__init__()
        self.load_word_list()
        self.create_frames()
        self.create_keyboard_buttons()
        self.create_side_buttons()
        self.create_word_labels()
        self.create_side_labels()
        self.play_game()
        

if __name__ == "__main__":
    hangman = Hangman()
    hangman.window.mainloop()
    