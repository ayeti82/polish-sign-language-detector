import tkinter as tk
import os
import cv2
import sys
import math
from PIL import Image, ImageTk
from tkinter import messagebox

# Configure
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 498
LEFT_PANEL_WIDTH = 648
RIGHT_PANEL_WIDTH = 452
WEBCAM_DIM = 800
SCALE_FACTOR = 1.5
CONTRAST_COLOR = "#104cf4"
BACKGROUND_COLOR = "#b1c5fc"
FONT_COLOR = "black"
HEADING_FONT = ('Courier New', 36)
BODY_FONT = ('Courier New', 14)
BUTTON_FONT = ('Courier New', 10)
PLACEHOLDER_WIDTH = 27
HEIGHT_GAP = 2

cancel = False


# Handle correctly recognized letter
def handle_proceed():
    messagebox.showinfo("Handle Proceed", "Proceed")


# Handle wrongly recognized letter
def handle_retry():
    messagebox.showinfo("Handle Retry", "Retry")


root = tk.Tk()
root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
root.resizable(width=False, height=False)
root.bind('<Escape>', lambda e: root.quit())
root.title("Polish Sign Language Detection App")
root.iconbitmap("images/icon.ico")

# Create panedWindow  
mainPanel = tk.PanedWindow(root, orient=tk.HORIZONTAL, bg=BACKGROUND_COLOR, borderwidth=5)
mainPanel.pack(fill=tk.BOTH, expand=True)

# Left Panel
leftPanel = tk.Label(mainPanel, anchor=tk.N)

mainPanel.paneconfigure(leftPanel, minsize=LEFT_PANEL_WIDTH)
mainPanel.add(leftPanel)

# Webcam video display
label = tk.Label(leftPanel, anchor=tk.CENTER, bg=CONTRAST_COLOR)
label.grid(row=0, column=0)
cap = cv2.VideoCapture(0)

# Right Panel
rightPanel = tk.PanedWindow(mainPanel, orient=tk.VERTICAL)
mainPanel.paneconfigure(rightPanel, minsize=RIGHT_PANEL_WIDTH)
mainPanel.add(rightPanel)

rightPanelTopFrame = tk.Frame(rightPanel, bg=BACKGROUND_COLOR)
tk.Label(rightPanelTopFrame, text="OUTPUT", anchor=tk.N, bg=BACKGROUND_COLOR, fg=FONT_COLOR, font=HEADING_FONT).pack()
tk.Label(rightPanelTopFrame, text="", anchor=tk.N, bg=BACKGROUND_COLOR, height=HEIGHT_GAP).pack()
tk.Label(rightPanelTopFrame, text="RECOGNIZED LETTER", anchor=tk.N, bg=BACKGROUND_COLOR, fg=FONT_COLOR,
         font=BODY_FONT).pack()
letterText = tk.Text(rightPanelTopFrame, state=tk.DISABLED, relief=tk.RAISED, fg=FONT_COLOR,
                     font=BODY_FONT, width=PLACEHOLDER_WIDTH, height=1)
letterText.pack()
tk.Button(rightPanelTopFrame, text="Retry", command=handle_retry, width=10,
          font=BUTTON_FONT).pack(side=tk.LEFT, padx = 20)
tk.Button(rightPanelTopFrame, text="Proceed", command=handle_proceed, width=10,
          font=BUTTON_FONT).pack(side=tk.RIGHT, padx=20)
rightPanel.paneconfigure(rightPanelTopFrame, minsize=248)
rightPanel.add(rightPanelTopFrame)


rightPanelBottomFrame = tk.Frame(rightPanel, bg=BACKGROUND_COLOR)
tk.Label(rightPanelBottomFrame, text="", bg=BACKGROUND_COLOR, height=HEIGHT_GAP).pack()
tk.Label(rightPanelBottomFrame, text="WORD FORMED", bg=BACKGROUND_COLOR, fg=FONT_COLOR,
         font=BODY_FONT).pack()
wordText = tk.Text(rightPanelBottomFrame, state=tk.DISABLED, relief=tk.RAISED, fg=FONT_COLOR,
                   font=BODY_FONT, width=PLACEHOLDER_WIDTH, height=6)
wordText.pack()
rightPanel.paneconfigure(rightPanelBottomFrame, minsize=250)
rightPanel.add(rightPanelBottomFrame)


# Define function to show frame
def show_frames():
    # Get the latest frame and convert into Image
    cv2image = cv2.cvtColor(cap.read()[1], cv2.COLOR_BGR2RGB)
    img = Image.fromarray(cv2image)
    # Convert image to PhotoImage
    photoImage = ImageTk.PhotoImage(image=img)
    label.photoImage = photoImage
    label.configure(image=photoImage)
    # Repeat after an interval to capture continuously
    label.after(20, show_frames)


show_frames()
root.mainloop()
