from settings import *
import customtkinter as ck
import random


class Hangman():
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
        self.used_letters = set()
        self.word_variable = ck.StringVar()
        self.result_variable = ck.StringVar(value="")
        self.display_difficulty = ck.StringVar(value="Normal")
        self.selected_difficulty = ck.StringVar(value="Normal")
        self.custom_variable_min = ck.StringVar(value=DIFFICULTY["Custom"][0])
        self.custom_variable_max = ck.StringVar(value=DIFFICULTY["Custom"][1])
        self.status = STATUS[0]

        self.load_word_list()
        self.create_frames()
        self.create_keyboard_buttons()
        self.create_side_buttons()
        self.create_labels()
        self.create_result_label()
        self.play_game()


    def load_word_list(self):
        try:
            with open("word_list.txt", "r") as file:
                words = file.readlines()
            for word in words:
                word = word.rstrip("\n").upper()
                self.word_list.append(word)
        except:
            print("Missing file")


    def create_frames(self):
        self.word_frame = ck.CTkFrame(self.window, fg_color=BACKGROUND_COLOR)
        self.word_frame.grid(row=0, column=0, sticky="nesw")

        self.keyboard_frame = ck.CTkFrame(self.window, fg_color=BACKGROUND_COLOR)
        self.keyboard_frame.grid(row=1, column=0, sticky="nesw")

        self.side_frame = ck.CTkFrame(self.window, fg_color=SIDE_BAR_COLOR)
        self.side_frame.grid(row=0, column=1, rowspan=2, sticky="nesw")
      

    def create_button(self, frame, text, row, column, font, command):
        button = ck.CTkButton(frame, text=text, border_width=BORDER_WIDTH,
                              corner_radius=BUTTON_CORNER_RADIUS, text_font=font,
                              command=command)
        button.grid(row=row, column=column)
        return button


    def difficulty_window(self):
        self.difficulty_window = ck.CTkToplevel()
        self.difficulty_window.geometry(f"{POPUP_WIDTH}x{POPUP_HEIGHT}")
        self.difficulty_window.title("Change Difficulty")

        label = ck.CTkLabel(self.difficulty_window, text="Select Difficulty: ",
                            text_font=KEYBOARD_FONT)
        label.grid(padx=10, pady=20, sticky="w")
        self.create_radio_buttons()
        self.create_custom_option()

        save_button = self.create_button(self.difficulty_window, text="Save",
                                         row=5, column=0, font=KEYBOARD_FONT,
                                         command=self.set_difficulty)
        save_button.configure(fg_color=GREEN, text_color=INNER_TEXT_COLOR, 
                              hover_color=GREEN_HOVER_COLOR)
        save_button.grid_configure(padx=55, pady=20)


    def create_keyboard_buttons(self):
        row = 0
        column = 0
        for letter in ALPHABET:
            if column == len(ALPHABET) / 2:
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

        difficulty_button = self.create_button(self.side_frame, 
                                                    text="Change\nDifficulty", 
                                                    row=4, column=0, font=KEYBOARD_FONT, 
                                                    command=self.difficulty_window)
        difficulty_button.configure(fg_color=DIFFICULTY_COLOR, 
                                         text_color=INNER_TEXT_COLOR, 
                                         hover_color=DIFFICULTY_COLOR)
        difficulty_button.grid_configure(pady=(0, 15))

        quit_button = self.create_button(self.side_frame, text="Quit",
                                              row=5, column=0, 
                                              font=KEYBOARD_FONT, 
                                              command=self.window.quit)
        quit_button.configure(fg_color=RED, text_color=INNER_TEXT_COLOR, 
                                   hover_color=RED_HOVER_COLOR)


    def create_radio_buttons(self):
        for key in DIFFICULTY.keys():
            min_length = DIFFICULTY[key][0]
            max_length = DIFFICULTY[key][1]
            if key != "Custom":
                text = f"{key}:  {min_length}-{max_length} letter word"
            else: text = f"{key}: "

            difficulty_radio = ck.CTkRadioButton(self.difficulty_window, 
                                                      text=text, 
                                                      variable=self.selected_difficulty, 
                                                      value=key, 
                                                      text_font=DIFFICULTY_FONT)
            difficulty_radio.grid(padx=20, pady=5, sticky="w")


    def create_labels(self):
        self.lives = NUMBER_OF_LIVES

        word_label = ck.CTkLabel(self.word_frame, textvariable=self.word_variable, 
                                 text_font=WORD_FONT)
        word_label.grid(row=0, column=0)
        word_label.place(relx=0.5, rely=0.5, anchor=ck.CENTER)

        self.lives_text_label = ck.CTkLabel(self.side_frame, 
                                            text=f"Lives: {self.lives}", 
                                            text_font=KEYBOARD_FONT)
        self.lives_text_label.grid(row=1, column=0, pady=30)

        difficulty_label = ck.CTkLabel(self.side_frame, 
                                            textvariable=self.display_difficulty, 
                                            text_font=KEYBOARD_FONT)
        difficulty_label.grid(row=3, column=0, padx=10, pady=(0, 20))


    def create_result_label(self):
        self.result_label = ck.CTkLabel(self.word_frame, textvariable=self.result_variable,
                                        text_font=RESULT_FONT, text_color=BACKGROUND_COLOR)
        self.result_label.grid(row=0, column=0)
        self.result_label.place(relx=0.5, rely=0.8, anchor=ck.CENTER)


    def create_option_menu(self, variable, length, column, command):
        option_menu = ck.CTkOptionMenu(self.difficulty_window, width=60, values=length,
                                       variable=variable, text_font=DROPDOWN_FONT,
                                       dynamic_resizing=False, command=command)
        option_menu.grid(row=4, column=column)
        return option_menu

    
    def create_custom_option(self):
        length = [str(number) for number in range(1, MAX_WORD_LENGTH+1)]
        custom_min = self.create_option_menu(variable=self.custom_variable_min, length=length,
                                             column=0, command=self.set_custom_option_min)
        custom_min.grid_configure(padx=120, row=4, column=0, sticky="w")

        custom_dash = ck.CTkLabel(self.difficulty_window, text="-", width=1,
                                  text_font=KEYBOARD_FONT)
        custom_dash.grid(padx=185, row=4, column=0, sticky="w")

        custom_max = self.create_option_menu(variable=self.custom_variable_max, length=length,
                                             column=2, command=self.set_custom_option_max)
        custom_max.grid_configure(padx=200, row=4, column=0, sticky="w")

        custom_text = ck.CTkLabel(self.difficulty_window, text="letter word", width=1, 
                                  text_font=DIFFICULTY_FONT)
        custom_text.grid(padx=265, row=4, column=0, sticky="w")

    
    def play_game(self):
        self.initialize_game()
        self.get_word()
        self.show_result()


    def initialize_game(self):
        self.new_word_list = []
        self.used_letters = set()
        self.status = STATUS[0]
        self.lives = NUMBER_OF_LIVES
        self.lives_text_label.configure(text=f"Lives: {self.lives}")
        for letter in self.keyboard_buttons:
            self.keyboard_buttons[letter].configure(fg_color=DARK_BLUE, state=ck.NORMAL)


    def get_word(self):
        for word in self.word_list:
            if (len(word) >= DIFFICULTY[self.display_difficulty.get()][0]
                    and len(word) <= DIFFICULTY[self.display_difficulty.get()][1]):
                self.new_word_list.append(word)
        self.secret_word = random.choice(self.new_word_list)
        new_word = "_ " * len(self.secret_word)
        self.word_variable.set(new_word.strip())
        print(f"{self.secret_word} ({len(self.secret_word)})")


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
        elif self.status == STATUS[2]:
            self.result_variable.set("You Won!")
            self.result_label.configure(text_color=GREEN)
        else:
            self.result_variable.set("") 


    def set_difficulty(self):
        if self.display_difficulty.get() != self.selected_difficulty.get():
            self.display_difficulty.set(self.selected_difficulty.get())
            self.play_game()
        self.difficulty_window.destroy() 


    def set_custom_option_min(self, choice):
        DIFFICULTY["Custom"][0] = choice
        print("min", DIFFICULTY["Custom"])

        return

    def set_custom_option_max(self, choice):
        DIFFICULTY["Custom"][1] = choice
        print("max", DIFFICULTY["Custom"])

        return



if __name__ == "__main__":
    hangman = Hangman()
    hangman.window.mainloop()
    