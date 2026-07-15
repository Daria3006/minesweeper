import time
import threading
import sys

import pygame
from pynput import keyboard

from screen import screen

# ANSI escape codes for terminal coloring
RESET = "\033[0m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
CYAN = "\033[36m"


class MinesweeperTimer:
    def __init__(self, initial_time=30):
        self.time_budget = float(initial_time)
        self.is_running = False
        self.lock = threading.Lock()
        self.status_color = RESET
        self.listener = None

    def usage(self):
        print("\n=== MINESWEEPER TIME ATTACK ===")
        print(f"| Initial Time Budget: {self.time_budget}s")
        print(f"|-> {GREEN}Tap [Ctrl]{RESET} to clear a board (+10s)")
        print(f"|-> {RED}Tap [Spacebar]{RESET} to simulate a mistake (-5s)")
        print(f"|-> {CYAN}Tap [Shift]{RESET} to immediately exit the game")
        print("===============================\n")

    def reward(self, seconds=10):
        """Call this when a player successfully clears a table."""
        with self.lock:
            self.time_budget += seconds
            self.status_color = GREEN
        print(f"\n{GREEN}[+] Table Cleared! +{seconds}s{RESET}")

    def penalty(self, seconds=5):
        """Call this when a player triggers a mine/makes a mistake."""
        with self.lock:
            self.time_budget = max(0.0, self.time_budget - seconds)
            self.status_color = RED
        print(f"\n{RED}[-] Mistake! -{seconds}s{RESET}")

    def _timer_loop(self):
        """Background thread that decrements the timer and updates the console."""
        last_check = time.time()

        while self.is_running:
            now = time.time()
            elapsed = now - last_check
            last_check = now

            with self.lock:
                self.time_budget -= elapsed
                current_budget = self.time_budget
                current_color = self.status_color

                # Decay the visual flash color back to default
                if self.status_color != RESET:
                    self.status_color = RESET

            if current_budget <= 0:
                print(f"\r{RED}Elapsed time: 0.0s | GAME OVER!{RESET}")
                self.stop_game()
                break

            # Choose color based on remaining time or instant triggers
            color = RED if current_budget < 10 else (current_color if current_color != RESET else YELLOW)
            print(f"\rTime Remaining: {color}{current_budget:.1f}s{RESET}      ", end="", flush=True)

            time.sleep(0.1)  # Precise visual tick rate

    def on_press(self, key):
        """Processes raw keypresses instantly as they occur."""
        if not self.is_running:
            return False

        # 1. Press Shift to immediately exit
        if key in (keyboard.Key.shift, keyboard.Key.shift_r, keyboard.Key.shift_l):
            print(f"\n{CYAN}[!] Shift key pressed. Exiting...{RESET}")
            self.stop_game()
            return False

        # 2. Press Ctrl to gain time
        elif key in (keyboard.Key.ctrl, keyboard.Key.ctrl_l, keyboard.Key.ctrl_r):
            self.reward(10)

        # 3. Press Spacebar to lose time (representing a mistake)
        elif key == keyboard.Key.space:
            self.penalty(5)

    def stop_game(self):
        """Safely tears down background loops and listener threads."""
        self.is_running = False
        if self.listener:
            self.listener.stop()

    def start(self):
        self.is_running = True

        # Start the visual ticking loop
        self.timer_thread = threading.Thread(target=self._timer_loop, daemon=True)
        self.timer_thread.start()

        # Start the keyboard listener to catch Ctrl/Shift instantly
        self.listener = keyboard.Listener(on_press=self.on_press)
        self.listener.start()

    def run(self):
        self.usage()
        print("Press any key to start...")

        # Block until the first key is pressed to kick off the game
        with keyboard.Events() as events:
            events.get(timeout=None)

        self.start()

        # Keep main thread alive while game is running
        while self.is_running:
            try:
                time.sleep(0.5)
            except KeyboardInterrupt:
                break

        self.stop_game()
        print("\n--- Game Session Ended ---")


if __name__ == "__main__":
    # game_timer = MinesweeperTimer(initial_time=30)
    # game_timer.run()
    pass

def display_timer():
    screen.blit(pygame.image.load("asseturi\\timer\\white_bg.png"), (20, 20))
    screen.blit(pygame.image.load("asseturi\\timer\\1.png"), (20, 25))
    screen.blit(pygame.image.load("asseturi\\timer\\1.png"), (40, 25))
    screen.blit(pygame.image.load("asseturi\\timer\\1.png"), (80, 25))
    screen.blit(pygame.image.load("asseturi\\timer\\1.png"), (100, 25))

