import tkinter as tk
from tkinter import messagebox
import random

# Slot machine configuration
MAX_LINES = 3
MAX_BET = 100
MIN_BET = 1

ROWS = 3
COLS = 3

symbol_count = {
    "A": 2,
    "B": 4,
    "C": 6,
    "D": 8
}

symbol_value = {
    "A": 5,
    "B": 4,
    "C": 3,
    "D": 2
}

class SlotMachineApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Slot Machine")

        # Initialize balance
        self.balance = 100  # Starting balance

        # Labels and inputs
        self.balance_label = tk.Label(root, text=f"Balance: £{self.balance}", font=("Helvetica", 16))
        self.balance_label.pack(pady=10)

        # Deposit button
        self.deposit_button = tk.Button(root, text="Deposit", command=self.deposit, font=("Helvetica", 14))
        self.deposit_button.pack(pady=10)

        self.lines_label = tk.Label(root, text="Number of lines to bet on (1-3):", font=("Helvetica", 12))
        self.lines_label.pack()
        self.lines_var = tk.IntVar(value=1)
        self.lines_entry = tk.Entry(root, textvariable=self.lines_var, font=("Helvetica", 12), width=5)
        self.lines_entry.pack()

        self.bet_label = tk.Label(root, text="Bet amount per line (£1-£100):", font=("Helvetica", 12))
        self.bet_label.pack()
        self.bet_var = tk.IntVar(value=1)
        self.bet_entry = tk.Entry(root, textvariable=self.bet_var, font=("Helvetica", 12), width=5)
        self.bet_entry.pack()

        # Spin button
        self.spin_button = tk.Button(root, text="Spin", command=self.spin, font=("Helvetica", 14))
        self.spin_button.pack(pady=10)

        # Results label
        self.results_label = tk.Label(root, text="", font=("Courier", 14), justify="left")
        self.results_label.pack(pady=10)

    def update_balance(self):
        self.balance_label.config(text=f"Balance: £{self.balance}")

    def deposit(self):
        deposit_amount = self.ask_for_deposit()
        if deposit_amount is not None:
            self.balance += deposit_amount
            self.update_balance()

    def ask_for_deposit(self):
        deposit_window = tk.Toplevel(self.root)
        deposit_window.title("Deposit Amount")

        label = tk.Label(deposit_window, text="Enter deposit amount:", font=("Helvetica", 12))
        label.pack(pady=10)

        deposit_var = tk.StringVar()
        deposit_entry = tk.Entry(deposit_window, textvariable=deposit_var, font=("Helvetica", 12))
        deposit_entry.pack(pady=10)

        def on_submit():
            try:
                deposit_value = int(deposit_var.get())
                if deposit_value > 0:
                    deposit_window.destroy()  # Close the deposit window
                    self.deposit_value = deposit_value  # Store the deposit amount in an attribute
                else:
                    messagebox.showerror("Error", "Deposit must be greater than 0")
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid amount")
        
        submit_button = tk.Button(deposit_window, text="Deposit", command=on_submit)
        submit_button.pack(pady=10)

        deposit_window.grab_set()  # Make the window modal
        deposit_window.wait_window()  # Wait for the window to close

        return getattr(self, "deposit_value", None)  # Return the deposit value or None if not set

    def get_slot_machine_spin(self, rows, cols, symbols):
        all_symbols = []
        for symbol, symbol_count in symbols.items():
            all_symbols.extend([symbol] * symbol_count)

        columns = []
        for _ in range(cols):
            column = []
            current_symbols = all_symbols[:]
            for _ in range(rows):
                value = random.choice(current_symbols)
                current_symbols.remove(value)
                column.append(value)
            columns.append(column)

        return columns

    def check_winnings(self, columns, lines, bet, values):
        winnings = 0
        winning_lines = []
        for line in range(lines):
            symbol = columns[0][line]
            for column in columns:
                symbol_to_check = column[line]
                if symbol != symbol_to_check:
                    break
            else:
                winnings += values[symbol] * bet
                winning_lines.append(line + 1)

        return winnings, winning_lines

    def spin(self):
        lines = self.lines_var.get()
        bet = self.bet_var.get()
        total_bet = lines * bet

        if lines < 1 or lines > MAX_LINES:
            messagebox.showerror("Error", f"Number of lines must be between 1 and {MAX_LINES}.")
            return

        if bet < MIN_BET or bet > MAX_BET:
            messagebox.showerror("Error", f"Bet must be between £{MIN_BET} and £{MAX_BET}.")
            return

        if total_bet > self.balance:
            messagebox.showerror("Error", "Insufficient balance!")
            return

        self.balance -= total_bet

        # Get slot machine spin results
        slots = self.get_slot_machine_spin(ROWS, COLS, symbol_count)

        # Format the slot machine grid for display
        slot_display = "\n".join(
            [" | ".join(column[row] for column in slots) for row in range(len(slots[0]))]
        )

        # Check winnings
        winnings, winning_lines = self.check_winnings(slots, lines, bet, symbol_value)
        self.balance += winnings

        # Update UI
        self.update_balance()
        result_text = f"Spin Results:\n{slot_display}\n\nYou won £{winnings}.\nWinning lines: {', '.join(map(str, winning_lines)) if winning_lines else 'None'}"
        self.results_label.config(text=result_text)

# Run the application
root = tk.Tk()
app = SlotMachineApp(root)
root.mainloop()
