import tkinter as tk
from tkinter import scrolledtext
from PIL import Image, ImageTk, ImageSequence


BG = "#0a0f1f"               # deep navy background
PANEL_BG = "#0f1629"         # terminal background
TEXT_CYAN = "#00d1ff"        # neon cyan text
TEXT_MAGENTA = "#ff00c8"     # neon pink header text
TEXT_PURPLE = "#a160ff"      # light purple footer text
BORDER_PURPLE = "#7a2bff"    # neon purple glowing border
INPUT_BG = "#11182f"         # input background
INPUT_FG = "#00faff"         # input text color
INSERT_COLOR = "#46e7ff"     # cursor

FONT_MAIN   = ("JetBrains Mono", 14)
FONT_HEADER = ("JetBrains Mono", 18, "bold")



awaiting_weight = True
awaiting_height = False
temp_weight = None

gif_frames = []
gif_label = None
gif_running = False
gif_index = 0



def load_gif():
    global gif_frames
    gif = Image.open(r"C:\Users\Shroy\OneDrive\Desktop\CODE\Jackfruit problem\motivation.gif")

    for frame in ImageSequence.Iterator(gif):
        frame = frame.resize((350, 350))
        gif_frames.append(ImageTk.PhotoImage(frame))


def play_gif():
    global gif_index, gif_running

    if not gif_running:
        return

    frame = gif_frames[gif_index]
    gif_label.config(image=frame)

    gif_index = (gif_index + 1) % len(gif_frames)
    root.after(50, play_gif)


def start_gif():
    global gif_running
    gif_running = True
    play_gif()



def calculate_bmi(weight, height):
    bmi = round(weight / (height ** 2), 1)

    if bmi < 16:
        status = "severely thin"
    elif bmi < 17:
        status = "moderately thin"
    elif bmi < 18.5:
        status = "mild thinness"
    elif bmi < 25:
        status = "normal"
    elif bmi < 30:
        status = "overweight"
    elif bmi < 35:
        status = "Obese class 1"
    elif bmi < 40:
        status = "Obese class 2"
    else:
        status = "Obese class 3"

    return bmi, status



def run_command(event=None):
    global awaiting_weight, awaiting_height, temp_weight, gif_running

    cmd = entry.get()
    terminal.insert(tk.END, f">> {cmd}\n")
    entry.delete(0, tk.END)
    # EXIT COMMAND
    if cmd.lower() in ["exit", "quit", "close"]:
     terminal.insert(tk.END, "Closing terminal...\n")
     root.after(300, root.destroy)  # slight delay for aesthetic
     return


    # Step 1: Get weight
    if awaiting_weight:
        try:
            temp_weight = float(cmd)
            awaiting_weight = False
            awaiting_height = True
            terminal.insert(tk.END, "Enter height (m):\n\n")
        except:
            terminal.insert(tk.END, "Invalid weight! Enter weight in kg:\n\n")
        terminal.see(tk.END)
        return

    # Step 2: Get height
    if awaiting_height:
        try:
            height = float(cmd)
            bmi, status = calculate_bmi(temp_weight, height)

            terminal.insert(tk.END, f"Your BMI is {bmi} and you are {status}\n\n")

            if bmi > 25:
                terminal.insert(tk.END, "BMI > 25! Playing motivation video...\n\n")
                start_gif()

        except:
            terminal.insert(tk.END, "Invalid height! Enter height in meters:\n\n")
            return

        awaiting_height = False
        terminal.see(tk.END)
        return



def build_cyberpunk_ui(root):
    root.title("BMI TERMINAL")
    root.geometry("750x820")
    root.configure(bg=BG)

    # Header
    header = tk.Label(
        root,
        text=" BMI TERMINAL ",
        font=FONT_HEADER,
        fg=TEXT_MAGENTA,
        bg=BG
    )
    header.pack(pady=15)

    # Terminal border glow
    glow_frame = tk.Frame(root, bg=BORDER_PURPLE, padx=3, pady=3)
    glow_frame.pack()

    # Terminal window
    terminal = scrolledtext.ScrolledText(
        glow_frame,
        font=FONT_MAIN,
        bg=PANEL_BG,
        fg=TEXT_CYAN,
        insertbackground=TEXT_CYAN,
        width=70,
        height=20,
        relief="flat",
        borderwidth=0
    )
    terminal.pack()

    # GIF Viewer Box
    gif_border = tk.Frame(root, bg=BORDER_PURPLE, padx=3, pady=3)
    gif_border.pack(pady=20)

    gif_label_widget = tk.Label(gif_border, bg=PANEL_BG)
    gif_label_widget.pack()

    # Input box
    input_frame = tk.Frame(root, bg=BORDER_PURPLE, padx=3, pady=3)
    input_frame.pack(pady=10)

    entry = tk.Entry(
        input_frame,
        font=FONT_MAIN,
        bg=INPUT_BG,
        fg=INPUT_FG,
        insertbackground=INSERT_COLOR,
        width=40,
        justify="center",
        relief="flat"
    )
    entry.pack()

    # Footer
    footer = tk.Label(
        root,
        fg=TEXT_PURPLE,
        bg=BG,
        font=("JetBrains Mono", 12)
    )
    footer.pack(pady=5)

    return terminal, entry, gif_label_widget



root = tk.Tk()

terminal, entry, gif_label = build_cyberpunk_ui(root)

# Load GIF frames AFTER gif_label exists
load_gif()

entry.bind("<Return>", run_command)
terminal.insert(tk.END, "Enter weight (kg):\n\n")
entry.focus()

root.mainloop()
