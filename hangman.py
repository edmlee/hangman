from settings import *
import customtkinter as ck
import random


class Hangman():
    def __init__(self):
        ck.set_appearance_mode("dark")
        ck.set_default_color_theme("blue")

        self.window = ck.CTk()
        self.window.title("Hangman")
        self.window.geometry(f"{WIDTH}x{HEIGHT}")
        self.window.minsize(WIDTH, HEIGHT)
        self.window.rowconfigure(0, weight=1)
        self.window.columnconfigure(0, weight=1)

        self.word_list = self.load_word_list()
        self.create_frames()
        self.create_keyboard_buttons()
        self.create_side_buttons()
        self.create_labels()
        self.play_game()


    def load_word_list(self):
        words = []
        try:
            with open("word_list.txt", "r") as file:
                word_list = file.readlines()
            for word in word_list:
                word = word.rstrip("\n").upper()
                if len(word) >= MIN_WORD_LENGTH:
                    words.append(word)
        except:
            print("Missing file")
        return words


    def create_frames(self):
        self.word_frame = ck.CTkFrame(self.window, fg_color=BACKGROUND_COLOR)
        self.word_frame.grid(row=0, column=0, sticky="nesw")

        self.keyboard_frame = ck.CTkFrame(self.window, fg_color=BACKGROUND_COLOR)
        self.keyboard_frame.grid(row=1, column=0, sticky="nesw")

        self.side_frame = ck.CTkFrame(self.window, fg_color=SIDE_BAR_COLOR)
        self.side_frame.grid(row=0, column=1, rowspan=2, sticky="nesw")


    def create_button(self, frame, text, row, column, font, command):
        button = ck.CTkButton(frame, text=text, border_width=BORDER_WIDTH,
                              corner_radius=BUTTON_CORNER_RADIUS, text_font=font, command=command)
        button.grid(row=row, column=column, sticky="nesw")
        return button


    def create_keyboard_buttons(self):
        row = 0
        column = 0
        for letter in ALPHABET:
            if column == len(ALPHABET) / 2:
                row += 1
                column = 0
            button = self.create_button(self.keyboard_frame, text=letter, row=row, column=column, font=KEYBOARD_FONT, 
                                        command= lambda letter=letter: self.update_word(letter))
            button.configure(height=BUTTON_HEIGHT)
            self.keyboard_frame.columnconfigure(column, weight=1)
            column += 1


    def create_side_buttons(self):
        new_game_button = self.create_button(self.side_frame, text="New Game", row=0, column=0, 
                                             font=KEYBOARD_FONT, command=self.play_game)
        new_game_button.configure(fg_color=GREEN, text_color=INNER_TEXT_COLOR, hover_color=GREEN_HOVER_COLOR)
        
        quit_button = self.create_button(self.side_frame, text="Quit", row=5, column=0, 
                                         font=KEYBOARD_FONT, command=self.window.quit)
        quit_button.configure(fg_color=RED, text_color=INNER_TEXT_COLOR, hover_color=RED_HOVER_COLOR)


    def create_labels(self):
        self.word_variable = ck.StringVar()
        self.lives_variable = ck.IntVar()
        self.lives_variable.set(NUMBER_OF_LIVES)

        word_label = ck.CTkLabel(self.word_frame, textvariable=self.word_variable, text_font=WORD_FONT)
        word_label.grid(row=0, column=0)
        word_label.place(relx=0.5, rely=0.5, anchor=ck.CENTER)

        lives_text_label = ck.CTkLabel(self.side_frame, width=1, text=f"Lives: ", text_font=KEYBOARD_FONT)
        lives_text_label.grid(row=1, column=0, padx=30, pady=20, sticky="w")
        
        lives_label = ck.CTkLabel(self.side_frame, width=1, textvariable=self.lives_variable, 
                                  text_font=KEYBOARD_FONT, anchor=ck.CENTER)
        lives_label.grid(row=1, column=0, padx=(0, 30), pady=20, sticky="e")


    def play_game(self):
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
        return


    def used_letters(self):
        pass


    def update_lives(self):
        pass


    def select_difficulty(self):
        pass


if __name__ == "__main__":
    hangman = Hangman()
    hangman.window.mainloop()
    