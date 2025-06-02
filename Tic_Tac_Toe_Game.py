import tkinter as tk
from tkinter import messagebox
import logging

# File handler and stream handler setup
logger = logging.getLogger("Tic_Tac_Toe_Logger")
logger.setLevel(logging.DEBUG)

if logger.hasHandlers():
    logger.handlers.clear()

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)  
stream_handler.setFormatter(formatter)

file_handler = logging.FileHandler("Tic_Tac_Toe.log")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

logger.addHandler(stream_handler)
logger.addHandler(file_handler)


# Global variables
buttons = []
current_player = "x"
winner = False
x_score = 0
o_score = 0


def check_viewer():
    global winner, x_score, o_score
    try:

        for combo in [[0, 1, 2], [3, 4, 5], [6, 7, 8],
                      [0, 3, 6], [1, 4, 7], [2, 5, 8],
                      [0, 4, 8], [2, 4, 6]]:
            if buttons[combo[0]]["text"] == buttons[combo[1]]["text"] == buttons[combo[2]]["text"] != "":
                for i in combo:
                    buttons[i].config(bg="green")
                winner = True
                player = buttons[combo[0]]["text"]
                logger.info(f"Player {player} wins the game!")

                if player == "x":
                    x_score += 1
                else:
                    o_score += 1
                update_score()
                messagebox.showinfo("Tic-Tac-Toe", f"Player {player.upper()} wins!")
                return
            
    except Exception as e:
        logger.error(f"Error checking for winner: {e}")

def button_click(index):
    try:

        if buttons[index]["text"] == "" and not winner:
            buttons[index]["text"] = current_player.upper()
            logger.info(f"Player {current_player.upper()} clicked button {index}")
            check_viewer()
            if not winner:
                toggle_player()

    except Exception as e:
        logger.error(f"Error during button click at index {index}: {e}")

def toggle_player():
    global current_player
    try:

        current_player = "x" if current_player == "o" else "o"
        label.config(text=f"Player {current_player.upper()}'s turn")

    except Exception as e:
        logger.exception(f"Error toggling player: {e}")

def restart_game():
    global winner, current_player
    try:

        for button in buttons:
            button.config(text="", bg="SystemButtonFace")
        winner = False
        current_player = "x"
        label.config(text=f"Player {current_player.upper()}'s turn")
        logger.info("Game restarted.")
        
    except Exception as e:
        logger.exception(f"Error restarting game: {e}")

def update_score():
    score_label.config(text=f"Score - X: {x_score} | O: {o_score}")


def main():
    global root, label, score_label, buttons, current_player, winner, x_score, o_score

    try:
        
        root = tk.Tk()
        root.title("Tic-Tac-Toe")
        logger.info("Tic-Tac-Toe game started.")

        buttons = [
            tk.Button(root, text="", font=("normal", 25), width=6, height=2,
                      command=lambda i=i: button_click(i)) for i in range(9)
        ]

        for i, button in enumerate(buttons):
            button.grid(row=i // 3, column=i % 3)

        label = tk.Label(root, text=f"Player {current_player.upper()}'s turn", font=("normal", 16))
        label.grid(row=3, column=0, columnspan=3)

        score_label = tk.Label(root, text=f"Score - X: {x_score} | O: {o_score}", font=("normal", 14))
        score_label.grid(row=4, column=0, columnspan=3)

        restart_button = tk.Button(root, text="Restart", font=("normal", 14), command=restart_game)
        restart_button.grid(row=5, column=0, columnspan=3, pady=10)

        root.mainloop()

    except Exception as e:
        logger.error(f"Failed to launch the game window: {e}")


if __name__ == "__main__":
    main()
