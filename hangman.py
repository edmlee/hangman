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
        self.keyboard_buttons = {}
        self.word_variable = ck.StringVar()
        self.used_letters = set()
        self.status = STATUS[0]
        self.difficulty = "Normal"

        self.load_word_list()
        self.create_frames()
        self.create_keyboard_buttons()
        self.create_side_buttons()
        self.create_labels()
        self.play_game()


    def load_word_list(self):
        try:
            with open("word_list.txt", "r") as file:
                words = file.readlines()
            for word in words:
                word = word.rstrip("\n").upper()
                if len(word) >= MIN_WORD_LENGTH:
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


    def create_difficulty_window(self):
        self.difficulty_window = ck.CTkToplevel()
        self.difficulty_window.geometry(f"{POPUP_WIDTH}x{POPUP_HEIGHT}")

        label = ck.CTkLabel(self.difficulty_window, text="Select Difficulty: ", text_font=KEYBOARD_FONT)
        label.grid(padx=10, pady=20, sticky="w")
        self.create_radio_buttons()
        

    def create_button(self, frame, text, row, column, font, command):
        button = ck.CTkButton(frame, text=text, border_width=BORDER_WIDTH,
                              corner_radius=BUTTON_CORNER_RADIUS, text_font=font, command=command)
        button.grid(row=row, column=column)
        return button


    def create_keyboard_buttons(self):
        row = 0
        column = 0
        for letter in ALPHABET:
            if column == len(ALPHABET) / 2:
                row += 1
                column = 0
            self.keyboard_buttons[letter] = self.create_button(self.keyboard_frame, text=letter, 
                                                               row=row, column=column, font=KEYBOARD_FONT, 
                                                               command= lambda letter=letter: self.update_word(letter))
            self.keyboard_buttons[letter].configure(height=BUTTON_HEIGHT)
            self.keyboard_frame.columnconfigure(column, weight=1)
            column += 1
 

    def create_side_buttons(self):
        self.new_game_button = self.create_button(self.side_frame, text="New Game", row=0, column=0,
                                                  font=KEYBOARD_FONT, command=self.play_game)                                       
        self.new_game_button.configure(fg_color=GREEN, text_color=INNER_TEXT_COLOR, hover_color=GREEN_HOVER_COLOR)
        self.new_game_button.grid_configure(pady=(10, 0))  

        self.difficulty_button = self.create_button(self.side_frame, text="Change\nDifficulty", row=4, column=0,
                                                    font=KEYBOARD_FONT, command=self.create_difficulty_window)
        self.difficulty_button.configure(fg_color=DIFFICULTY_COLOR, text_color=INNER_TEXT_COLOR, hover_color=DIFFICULTY_COLOR)

        self.difficulty_button.grid_configure(pady=(0, 15))

        self.quit_button = self.create_button(self.side_frame, text="Quit", row=5, column=0, 
                                              font=KEYBOARD_FONT, command=self.window.quit)
        self.quit_button.configure(fg_color=RED, text_color=INNER_TEXT_COLOR, hover_color=RED_HOVER_COLOR)


    def create_radio_buttons(self):
        var = ck.IntVar()
        value = 1
        for difficulty in DIFFICULTY.keys():
            button = ck.CTkRadioButton(self.difficulty_window, text=difficulty, variable=var, value=value, text_font=DIFFICULTY_FONT)
            button.grid(padx=20, sticky="w")
            value += 1
        return


    def create_labels(self):
        self.lives = NUMBER_OF_LIVES

        self.word_label = ck.CTkLabel(self.word_frame, textvariable=self.word_variable, text_font=WORD_FONT)
        self.word_label.grid(row=0, column=0)
        self.word_label.place(relx=0.5, rely=0.5, anchor=ck.CENTER)

        self.lives_text_label = ck.CTkLabel(self.side_frame, text=f"Lives: {self.lives}", text_font=KEYBOARD_FONT)
        self.lives_text_label.grid(row=1, column=0, pady=30)

        self.difficulty_label = ck.CTkLabel(self.side_frame, text=f"Difficulty: {self.difficulty}", text_font=KEYBOARD_FONT)
        self.difficulty_label.grid(row=3, column=0, padx=10, pady=(0, 20))
        
    
    def play_game(self):
        self.status = STATUS[0]
        self.used_letters = set()
        self.lives = NUMBER_OF_LIVES
        self.lives_text_label.configure(text=f"Lives: {self.lives}")
        for letter in self.keyboard_buttons:
            self.keyboard_buttons[letter].configure(fg_color=DARK_BLUE, state=ck.NORMAL)

        self.secret_word = random.choice(self.word_list)
        word = "_ " * len(self.secret_word)
        self.word_variable.set(word.strip())
        print(self.secret_word)


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
            self.keyboard_buttons[letter].configure(fg_color=DISABLED_BUTTON_COLOR, state=ck.DISABLED)
        self.update_status(word)

        
    def update_status(self, word):
        if self.lives == 0:
            self.status = STATUS[1]
        elif set(word).issubset(self.used_letters):
            self.status = STATUS[2]
        if self.status != STATUS[0]:
            for letter in self.keyboard_buttons:
                self.keyboard_buttons[letter].configure(state=ck.DISABLED)


    def set_difficulty(self, min_length, max_length):           
        pass


    def select_difficulty(self):
        pass


if __name__ == "__main__":
    hangman = Hangman()
    hangman.window.mainloop()
    