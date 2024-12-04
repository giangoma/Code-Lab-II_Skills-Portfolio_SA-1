from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk, ImageSequence
import pygame
import random

# Pygame mixer for sound
pygame.mixer.init()
pygame.mixer.music.load("c:/Users/giang/Documents/GitHub/skills-portfolio-giangoma/A1 - Skills Portfolio/Math Quiz/Assets/bgm.mp3")
pygame.mixer.music.play(-1)  
button_sound = pygame.mixer.Sound("c:/Users/giang/Documents/GitHub/skills-portfolio-giangoma/A1 - Skills Portfolio/Math Quiz/Assets/button_press.mp3")

root = Tk()
root.title("Maths Quiz")
root.geometry("600x400")
root.resizable(False, False)

# Global variables
score = 0
attempts = 0
current_answer = 0
question_count = 0
max_questions = 10

# Function to switch frames
def switch_frame(frame):
    frame.tkraise()

# Function to start quiz
def start_quiz():
    global question_count, score
    question_count = 0
    score = 0
    submit_button.config(state=NORMAL)
    switch_frame(difficulty_frame)

# Function to exit application
def exit_app():
    root.quit()

# Function to set difficulty
def setDifficulty(level):
    global min_val, max_val
    if level == 1:  # Easy
        min_val, max_val = 1, 10
    elif level == 2:  # Moderate
        min_val, max_val = 10, 50
    else:  # Hard
        min_val, max_val = 50, 100
    switch_frame(quiz_frame)
    next_problem()

# Function to generate a random integer
def randomInt(min_val, max_val):
    return random.randint(min_val, max_val)

# Function to decide the operation
def decideOperation():
    return random.choice(['+', '-'])

# Function to display the problem and accept the user's answer
def displayProblem():
    global current_answer, attempts
    num1 = randomInt(min_val, max_val)
    num2 = randomInt(min_val, max_val)
    operation = decideOperation()

    if operation == '+':
        current_answer = num1 + num2
    else:
        current_answer = num1 - num2
    
    problem_label.config(text=f"{num1} {operation} {num2}")
    attempts = 0
    answer_entry.delete(0, END)

# Function to check if the user's answer is correct
def isCorrect():
    global score, attempts, question_count
    print(f"Question count before answer: {question_count}")  # Debug print statement
    user_answer = int(answer_entry.get())
    if user_answer == current_answer:
        if attempts == 0:
            score += 10
        else:
            score += 5
        score_label.config(text=f"{score}")
        pygame.mixer.Sound("c:/Users/giang/Documents/GitHub/skills-portfolio-giangoma/A1 - Skills Portfolio/Math Quiz/Assets/correct.mp3").play()  # Plays correct sound
    else:
        attempts += 1
        if attempts < 2:
            feedback_label.config(text="Wrong answer. Try again.")
            pygame.mixer.Sound("c:/Users/giang/Documents/GitHub/skills-portfolio-giangoma/A1 - Skills Portfolio/Math Quiz/Assets/wrong.mp3").play()  # Plays wrong sound
            return
        else:
            feedback_label.config(text=f"Wrong answer. The correct answer was {current_answer}.")
            pygame.mixer.Sound("c:/Users/giang/Documents/GitHub/skills-portfolio-giangoma/A1 - Skills Portfolio/Math Quiz/Assets/wrong.mp3").play() 

    question_count += 1
    print(f"Question count after answer: {question_count}")  # Debug print statement
    if question_count >= max_questions:
        displayResults()
    else:
        next_problem()

# Function to move to the next problem
def next_problem():
    feedback_label.config(text="")
    displayProblem()

# Function to display results at the end of the quiz
def displayResults():
    grade = ""
    if score > 90:
        grade = "A+!"
        switch_frame(above_d_frame)
        animate_gif(above_d_frame, bg_label_above_d, above_d_frames)
        pygame.mixer.Sound("c:/Users/giang/Documents/GitHub/skills-portfolio-giangoma/A1 - Skills Portfolio/Math Quiz/Assets/above_d.mp3").play()
    elif score > 80:
        grade = "A!"
        switch_frame(above_d_frame)
        animate_gif(above_d_frame, bg_label_above_d, above_d_frames)
        pygame.mixer.Sound("c:/Users/giang/Documents/GitHub/skills-portfolio-giangoma/A1 - Skills Portfolio/Math Quiz/Assets/above_d.mp3").play()
    elif score > 70:
        grade = "B!"
        switch_frame(above_d_frame)
        animate_gif(above_d_frame, bg_label_above_d, above_d_frames)
        pygame.mixer.Sound("c:/Users/giang/Documents/GitHub/skills-portfolio-giangoma/A1 - Skills Portfolio/Math Quiz/Assets/above_d.mp3").play()
    elif score > 60:
        grade = "C!"
        switch_frame(above_d_frame)
        animate_gif(above_d_frame, bg_label_above_d, above_d_frames)
        pygame.mixer.Sound("c:/Users/giang/Documents/GitHub/skills-portfolio-giangoma/A1 - Skills Portfolio/Math Quiz/Assets/above_d.mp3").play()
    elif score > 50:
        grade = "D!"
        switch_frame(above_d_frame)
        animate_gif(above_d_frame, bg_label_above_d, above_d_frames)
        pygame.mixer.Sound("c:/Users/giang/Documents/GitHub/skills-portfolio-giangoma/A1 - Skills Portfolio/Math Quiz/Assets/above_d.mp3").play()
    else:
        grade = "F"
        switch_frame(below_f_frame)
        animate_gif(below_f_frame, bg_label_below_f, below_f_frames)
        pygame.mixer.Sound("c:/Users/giang/Documents/GitHub/skills-portfolio-giangoma/A1 - Skills Portfolio/Math Quiz/Assets/below_f.mp3").play()
    
    print(f"Displaying results: Score = {score}, Grade = {grade}")  # Debug print statement

    score_label_above.config(text=f"{score}")
    grade_label_above.config(text=f"{grade}")
    score_label_below.config(text=f"{score}")
    grade_label_below.config(text=f"{grade}")

    # Disabling the submit button to prevent further inputs
    submit_button.config(state=DISABLED)

# Function to reset the quiz
def reset_quiz():
    global score, question_count
    score = 0
    question_count = 0
    score_label.config(text=f"{score}")
    submit_button.config(state=NORMAL) 
    switch_frame(title_frame)

# Warning message box when exiting the quiz
def confirm_exit():
    if messagebox.askyesno("Exit Quiz", "Are you sure you want to exit? You will lose all progress."):
        reset_quiz()

# Function to animate GIF
def animate_gif(frame, label, frames):
    try:
        frame_image = next(frames)
        photo_image = ImageTk.PhotoImage(frame_image)
        label.config(image=photo_image)
        label.image = photo_image
        frame.after(50, animate_gif, frame, label, frames)
    except StopIteration:
        frames = ImageSequence.Iterator(frame_image)
        animate_gif(frame, label, frames)

# Function to play button press sound
def play_button_sound():
    button_sound.play()

# Frames
title_frame = Frame(root)
instructions_frame = Frame(root)
difficulty_frame = Frame(root)
quiz_frame = Frame(root)
above_d_frame = Frame(root)
below_f_frame = Frame(root)

for frame in (title_frame, instructions_frame, difficulty_frame, quiz_frame, above_d_frame, below_f_frame):
    frame.place(relwidth=1, relheight=1)

# Title Frame
bg_image_title = Image.open("c:/Users/giang/Documents/GitHub/skills-portfolio-giangoma/A1 - Skills Portfolio/Math Quiz/Assets/title-screen.png")
bg_image_title = bg_image_title.resize((600, 400))
bg_photo_title = ImageTk.PhotoImage(bg_image_title)
bg_label_title = Label(title_frame, image=bg_photo_title)
bg_label_title.place(relwidth=1, relheight=1)

instructions_button = Button(
    title_frame,
    text="Instructions",
    compound="center",
    font=("Halo Dek", 11),  
    fg="#077a58",
    bg="#fff7c5",
    borderwidth=0,
    activebackground="#fff7c5",
    activeforeground="#176c53",
    command=lambda: [play_button_sound(), switch_frame(instructions_frame)]
)
instructions_button.place(x=150, y=325)

start_button = Button(
    title_frame,
    text="Start",
    compound="center",
    font=("Halo Dek", 11),  
    fg="#077a58",
    bg="#fff7c5",
    borderwidth=0,
    activebackground="#fff7c5",
    activeforeground="#176c53",
    command=lambda: [play_button_sound(), start_quiz()]
)
start_button.place(x=370, y=325)

# Instructions Frame
bg_image_instructions = Image.open("c:/Users/giang/Documents/GitHub/skills-portfolio-giangoma/A1 - Skills Portfolio/Math Quiz/Assets/instructions-screen.png")
bg_image_instructions = bg_image_instructions.resize((600, 400))
bg_photo_instructions = ImageTk.PhotoImage(bg_image_instructions)
bg_label_instructions = Label(instructions_frame, image=bg_photo_instructions)
bg_label_instructions.place(relwidth=1, relheight=1)

back_button_instructions = Button(
    instructions_frame,
    text="Back to Home",
    fg="#077a58",
    font=("Halo Dek", 11),
    borderwidth=0,
    bg="#fff7c5",
    activebackground="#fff7c5",
    activeforeground="#176c53",
    command=lambda: [play_button_sound(), switch_frame(title_frame)]
)
back_button_instructions.place(x=250, y=318)

# Difficulty Frame
bg_image_difficulty = Image.open("c:/Users/giang/Documents/GitHub/skills-portfolio-giangoma/A1 - Skills Portfolio/Math Quiz/Assets/difficulty-screen.png")
bg_image_difficulty = bg_image_difficulty.resize((600, 400))
bg_photo_difficulty = ImageTk.PhotoImage(bg_image_difficulty)
bg_label_difficulty = Label(difficulty_frame, image=bg_photo_difficulty)
bg_label_difficulty.place(relwidth=1, relheight=1)

easy_button = Button(difficulty_frame, text="EASY", font=("Halo Dek", 11), fg="#077a58", borderwidth=0, bg="#fff7c5", command=lambda: setDifficulty(1))
easy_button.place(x=200, y=150)

moderate_button = Button(difficulty_frame, text="MODERATE", font=("Halo Dek", 11), fg="#077a58", borderwidth=0, bg="#fff7c5", command=lambda: setDifficulty(2))
moderate_button.place(x=200, y=217)

advanced_button = Button(difficulty_frame, text="HARD", font=("Halo Dek", 11), fg="#077a58", borderwidth=0, bg="#fff7c5", command=lambda: setDifficulty(3))
advanced_button.place(x=200, y=283)

# Quiz Frame
bg_image_quiz = Image.open("c:/Users/giang/Documents/GitHub/skills-portfolio-giangoma/A1 - Skills Portfolio/Math Quiz/Assets/quiz-screen.png")
bg_image_quiz = bg_image_quiz.resize((600, 400))
bg_photo_quiz = ImageTk.PhotoImage(bg_image_quiz)
bg_label_quiz = Label(quiz_frame, image=bg_photo_quiz)
bg_label_quiz.place(relwidth=1, relheight=1)

problem_label = Label(quiz_frame, text="", font=("Halo Dek", 40), bg="#fff7c5")
problem_label.place(x=227, y=100)

answer_entry = Entry(quiz_frame, font=("Halo Dek", 16))
answer_entry.place(x=194, y=170)

submit_button = Button(quiz_frame, text="Submit", font=("Halo Dek", 11), fg="#077a58", bg="#fff7c5", borderwidth=0, command=isCorrect)
submit_button.place(x=275, y=200)

score_label = Label(quiz_frame, text="0", font=("Halo Dek", 20), bg="#fff7c5")
score_label.place(x=550, y=275)

feedback_label = Label(quiz_frame, text="", font=("Halo Dek", 12), bg="#fff7c5")
feedback_label.place(x=250, y=250)

exit_button = Button(quiz_frame, text="Exit", font=("Halo Dek", 11), fg="#ffffff", borderwidth=0, bg="#077a58", command=confirm_exit)
exit_button.place(x=60, y=18)

# Preparing GIF frames for Above D Frame
above_d_gif = Image.open("c:/Users/giang/Documents/GitHub/skills-portfolio-giangoma/A1 - Skills Portfolio/Math Quiz/Assets/above_d.gif")
above_d_frames = ImageSequence.Iterator(above_d_gif)
bg_image_above_d = next(above_d_frames)
bg_photo_above_d = ImageTk.PhotoImage(bg_image_above_d)
bg_label_above_d = Label(above_d_frame, image=bg_photo_above_d)
bg_label_above_d.place(relwidth=1, relheight=1)

score_label_above = Label(above_d_frame, text="", font=("Halo Dek", 20), bg="#fdf1c5")
score_label_above.place(x=500, y=158)

grade_label_above = Label(above_d_frame, text="", font=("Halo Dek", 50), fg="#077a58", bg="#fdf1c5")
grade_label_above.place(x=400, y=210)

home_button_above = Button(above_d_frame, text="Home", font=("Halo Dek", 10), fg="#077a58", borderwidth=0, bg="#fdf1c5", command=reset_quiz)
home_button_above.place(x=520, y=366)

# Preparing GIF frames for Below F Frame
below_f_gif = Image.open("c:/Users/giang/Documents/GitHub/skills-portfolio-giangoma/A1 - Skills Portfolio/Math Quiz/Assets/below_f.gif")
below_f_frames = ImageSequence.Iterator(below_f_gif)
bg_image_below_f = next(below_f_frames)
bg_photo_below_f = ImageTk.PhotoImage(bg_image_below_f)
bg_label_below_f = Label(below_f_frame, image=bg_photo_below_f)
bg_label_below_f.place(relwidth=1, relheight=1)

score_label_below = Label(below_f_frame, text="", font=("Halo Dek", 20), bg="#fdf1c5")
score_label_below.place(x=500, y=158)

grade_label_below = Label(below_f_frame, text="", font=("Halo Dek", 50), fg="#077a58", bg="#fdf1c5")
grade_label_below.place(x=400, y=210)

home_button_below = Button(below_f_frame, text="Home", font=("Halo Dek", 10), fg="#022c5e", borderwidth=0, bg="#fdf1c5", command=reset_quiz)
home_button_below.place(x=520, y=366)

# Initializing first frame
switch_frame(title_frame)

root.mainloop()


#Resources used:
#> All visual assets were taken from Canva. www.canva.com
#> All audio taken from YouTube. The BGM's name is Relaxed Scene by James Clarke. - https://www.youtube.com/watch?v=DmLRQryHkVA
#> Click sound effect taken from Mojang - "Minecraft". - https://www.youtube.com/watch?v=h8y0JMVwdmM
#> AI - Microsoft Copilot used in line 11. Prompt - "How do I add a sound effect each time a button is pressed?"
