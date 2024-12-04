import tkinter as tk
from tkinter import Frame, Label, Button, Canvas
from PIL import Image, ImageTk, ImageSequence
import random
import os
from gtts import gTTS
import pygame
import uuid

class App:
    def __init__(self, root):
        self.root = root
        self.root.geometry("400x600")
        self.root.title("Alexa Joke Chatbot")
        self.root.configure(bg="#232f3e")
        self.root.resizable(False, False)
        
        pygame.mixer.init()
        
        # Setting the base directory for assets
        self.assets_dir = "C:/Users/giang/Documents/GitHub/skills-portfolio-giangoma/A1 - Skills Portfolio/Alexa Tell Me a Joke/Assets/"

        self.opening_frame = Frame(self.root, bg="#232f3e")
        self.chat_frame = Frame(self.root, bg="#232f3e")
        self.gif_frame = Frame(self.root, bg="#232f3e")
        self.instructions_frame = Frame(self.root, bg="#232f3e")
        
        for frame in (self.opening_frame, self.chat_frame, self.gif_frame, self.instructions_frame):
            frame.place(relwidth=1, relheight=1)
        
        self.create_opening_frame()
        self.create_chat_frame()
        self.create_instructions_frame()
        self.create_gif_frame()

        self.opening_frame.tkraise()

    def create_opening_frame(self):
        try:
            self.opening_gif = Image.open(os.path.join(self.assets_dir, "opening.gif"))
            self.gif_frames = ImageSequence.Iterator(self.opening_gif)
            self.gif_image = ImageTk.PhotoImage(next(self.gif_frames))

            self.label = Label(self.opening_frame, image=self.gif_image, bg="#232f3e")
            self.label.pack(fill="both", expand=True)
            
            self.play_opening_gif()
        except Exception as e:
            print(f"Error loading GIF: {e}")

    def play_opening_gif(self):
        try:
            next_frame = next(self.gif_frames)
            self.gif_image = ImageTk.PhotoImage(next_frame)
            self.label.config(image=self.gif_image)
            self.root.after(80, self.play_opening_gif)
        except StopIteration:
            self.chat_frame.tkraise()

    def create_chat_frame(self):
        self.display_area = Canvas(self.chat_frame, bg="#232f3e", bd=0, highlightthickness=0)
        self.display_area.pack(pady=20, fill="both", expand=True)

        self.joke_button = Button(self.chat_frame, text="ALEXA, TELL ME A JOKE", command=self.tell_joke, font=("Amazon Ember", 12), bg="#f89603", fg="black", padx=10, pady=5)
        self.joke_button.pack(side='left', padx=10, pady=10)

        self.instructions_button = Button(self.chat_frame, text="INSTRUCTIONS", command=self.show_instructions, font=("Amazon Ember", 12), bg="#f89603", fg="black", padx=10, pady=5)
        self.instructions_button.pack(side='right', padx=10, pady=10)

    def create_gif_frame(self):
        self.gif_label = Label(self.gif_frame, bg="#232f3e")
        self.gif_label.place(relwidth=1, relheight=1)

    def clear_chat(self):
        self.display_area.delete("all")

    def tell_joke(self):
        self.clear_chat()
        self.add_chat_bubble("👤 Alexa, tell me a joke", "#ffffff", "#000000", "right")
        joke = self.get_random_joke()
        setup, punchline = joke.split('?')
        self.root.after(1000, lambda: self.add_chat_bubble(f"🤖 {setup}?", "#828fa1", "#ffffff", "left"))
        self.root.after(1000, lambda: self.speak_text(setup))
        self.root.after(6000, lambda: self.add_chat_bubble(f"🤖 {punchline}", "#828fa1", "#ffffff", "left"))
        self.root.after(6000, lambda: self.speak_text(punchline))
        self.root.after(10000, self.play_random_sound) 
        self.root.after(12000, self.change_background_to_gif) 

    def speak_text(self, text):
        filename = os.path.join(self.assets_dir, f"alexa_tts_{uuid.uuid4()}.mp3")
        tts = gTTS(text=text, lang='en')
        tts.save(filename)
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()

    def play_random_sound(self):
        sounds = ["jokesound1.mp3", "jokesound2.mp3", "jokesound3.mp3"]
        sound_to_play = os.path.join(self.assets_dir, random.choice(sounds))
        pygame.mixer.music.load(sound_to_play)
        pygame.mixer.music.play()

    def change_background_to_gif(self):
        try:
            self.background_gif = Image.open(os.path.join(self.assets_dir, "background.gif"))
            self.bg_frames = ImageSequence.Iterator(self.background_gif)
            self.bg_image = ImageTk.PhotoImage(next(self.bg_frames))

            self.gif_label.config(image=self.bg_image)
            self.gif_frame.tkraise()

            self.play_background_gif()
        except Exception as e:
            print(f"Error loading GIF: {e}")

    def play_background_gif(self):
        try:
            next_frame = next(self.bg_frames)
            self.bg_image = ImageTk.PhotoImage(next_frame)
            self.gif_label.config(image=self.bg_image)
            self.root.after(80, self.play_background_gif)
        except StopIteration:
            self.chat_frame.tkraise()

    def show_instructions(self):
        self.instructions_frame.tkraise()

    def create_instructions_frame(self):
        instructions = "Press the 'Alexa, tell me a joke' button to hear a joke. Press 'Enter' to hear the punchline. Press 'Instructions' to read these instructions again."
        label = Label(self.instructions_frame, text=instructions, font=("Amazon Ember Light", 14), bg="#232f3e", fg="white", wraplength=350)
        label.pack(pady=20)

        #Graphic
        image_path = os.path.join(self.assets_dir, "alexa-graphic.png")
        self.instructions_image = Image.open(image_path)
        self.instructions_image = self.instructions_image.resize((200, 200), Image.LANCZOS)
        self.instructions_image = ImageTk.PhotoImage(self.instructions_image)
        image_label = Label(self.instructions_frame, image=self.instructions_image, bg="#232f3e")
        image_label.pack(pady=10)

        back_button = Button(self.instructions_frame, text="BACK TO CHAT", command=self.chat_frame.tkraise, font=("Amazon Ember", 12), bg="#f89603", fg="black", padx=10, pady=5)
        back_button.pack(pady=10)

    def add_chat_bubble(self, text, bg_color, text_color, align):
        bubble_width = 350
        x1, y1, x2, y2 = 10, 10, bubble_width, 60

        if align == "left":
            self.create_rounded_rectangle(x1, y1, x2, y2, radius=20, fill=bg_color)
            self.display_area.create_text((x1+10, y1+10), anchor='nw', text=text, font=("Amazon Ember Light", 12), fill=text_color, width=bubble_width-20)
        else:
            self.create_rounded_rectangle(x1 + bubble_width//2, y1, x2 + bubble_width//2, y2, radius=20, fill=bg_color)
            self.display_area.create_text((x1 + bubble_width//2 + 10, y1+10), anchor='nw', text=text, font=("Amazon Ember Light", 12), fill=text_color, width=bubble_width-20)

        self.display_area.move("all", 0, 80)

    def create_rounded_rectangle(self, x1, y1, x2, y2, radius=25, **kwargs):
        points = [x1+radius, y1, x1+radius, y1,
                  x2-radius, y1, x2-radius, y1,
                  x2, y1, x2, y1+radius,
                  x2, y1+radius, x2, y2-radius,
                  x2, y2-radius, x2, y2,
                  x2-radius, y2, x2-radius, y2,
                  x1+radius, y2, x1+radius, y2,
                  x1, y2, x1, y2-radius,
                  x1, y2-radius, x1, y1+radius,
                  x1, y1+radius, x1, y1]

        return self.display_area.create_polygon(points, **kwargs, smooth=True)

    def get_random_joke(self):
        with open(os.path.join(self.assets_dir, 'randomJokes.txt'), 'r') as file:
            jokes = [line.strip() for line in file if '?' in line]
        return random.choice(jokes)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()

#Resources used:
#> Amazon & Amazon Alexa Logos from Amazon. Opening GIF was developed in Canva. www.canva.com
#> All fonts also from Amazon - Amazon Developer at https://developer.amazon.com/en-US/alexa/branding/echo-guidelines/identity-guidelines/typography
#> Vector used in Instructions screen was from tagechos, at Pixabay - https://pixabay.com/vectors/amazon-echo-dot-amazon-alexa-3597986/
#> AI - Microsoft Copilot used in line 21. Prompt - "How do I make all of my code refer to a specific folder/specific directory for assets?"