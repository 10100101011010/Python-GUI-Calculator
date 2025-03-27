import tkinter as tk
from tkinter import Button, Entry
import re

root = tk.Tk()
root.title("Calculator")
root.geometry("350x500")
root.configure(bg="#f5f5f5")


def on_click(value):
    if entry_var.get() == "Error":
        entry_var.set("")
        enable_buttons()

    current_value = entry_var.get()

    if value == "*":
        value = "\u00D7"
    elif value == "/":
        value = "\u00F7"

    if current_value and current_value[-1] == ")" and value.isdigit():
        entry_var.set(current_value + "\u00D7" + value)
        return

    if value in "+-\u00D7\u00F7^%":
        handle_operator(value)
        return

    if value == ".":
        handle_decimal_point()
    elif value == "C":
        clear_entry()
    elif value == "=":
        evaluate_expression()
    elif value == "()":
        handle_parentheses()
    else:
        entry_var.set(current_value + value)


def handle_operator(value):
    current_value = entry_var.get()

    if value == "*":
        value = "\u00D7"
    elif value == "/":
        value = "\u00F7"

    if current_value and current_value[-1] == value:
        return

    if current_value and current_value[-1] in "+-\u00D7\u00F7^%":
        entry_var.set(current_value[:-1] + value)
    else:
        entry_var.set(current_value + value)


def handle_decimal_point():
    current_value = entry_var.get()
    number_segments = re.split(r'[\+\-\u00D7\u00F7\*/\^%\(\)]', current_value)
    last_segment = number_segments[-1] if number_segments else ""

    if "." in last_segment:
        return

    if last_segment == "":
        entry_var.set(current_value + "0.")
    else:
        entry_var.set(current_value + ".")


def clear_entry():
    entry_var.set("")


def evaluate_expression():
    try:
        expression = entry_var.get().replace("^", "**")
        expression = expression.replace("\u00F7", "/").replace("\u00D7", "*")
        expression = expression.replace("%", "/100")
        if expression.endswith('.'):
            expression = expression[:-1]
        result = eval(expression)
        if isinstance(result, float):
            result = round(result, 9)
        if isinstance(result, float) and result.is_integer():
            result = int(result)
        entry_var.set(result)
    except ZeroDivisionError:
        entry_var.set("Cannot divide by zero")
        disable_buttons()
        reset_after_delay()
    except Exception:
        entry_var.set("Error")
        disable_buttons()
        reset_after_delay()


def handle_parentheses():
    current_value = entry_var.get()
    open_parentheses = current_value.count('(')
    close_parentheses = current_value.count(')')

    if current_value and current_value[-1].isdigit():
        unmatched_open = current_value.rfind('(')
        unmatched_close = current_value.rfind(')')

        if unmatched_open > unmatched_close:
            entry_var.set(current_value + ")")
        else:
            entry_var.set(current_value + "\u00D7(")

    elif not current_value or current_value[-1] in "+-\u00D7\u00F7^%(":
        entry_var.set(current_value + "(")
    elif open_parentheses > close_parentheses:
        entry_var.set(current_value + ")")
    else:
        entry_var.set(current_value + "(")


def reset_after_delay():
    root.after(960, lambda: entry_var.set(""))
    root.after(960, enable_buttons)


def disable_buttons():
    for button in all_buttons:
        button.config(state="disabled")


def enable_buttons():
    for button in all_buttons:
        button.config(state="normal")


def delete_last_character():
    current_value = entry_var.get()
    if current_value:
        entry_var.set(current_value[:-1])


entry_var = tk.StringVar()
entry = Entry(root, textvariable=entry_var, font=("Arial", 24),
              bd=0, relief="flat", justify="right", bg="#f5f5f5")
entry.grid(row=0, column=0, columnspan=4, pady=20,
           padx=10, ipadx=8, ipady=10, sticky="ew")

delete_btn = Button(root, text="⌫", font=("Arial", 18), width=5, height=2, relief="flat",
                    bg="#fff", fg="black", command=delete_last_character)
delete_btn.grid(row=1, column=3, padx=5, pady=5, sticky="nsew")

buttons = [
    ["C", "()", "^", "\u00F7"],
    ["7", "8", "9", "\u00D7"],
    ["4", "5", "6", "-"],
    ["1", "2", "3", "+"],
    ["%", "0", ".", "="]
]

all_buttons = [delete_btn]

for i in range(5):
    root.grid_rowconfigure(i + 1, weight=1, minsize=60)
for i in range(4):
    root.grid_columnconfigure(i, weight=1, minsize=60)

for row_idx, row in enumerate(buttons, start=2):
    for col_idx, button in enumerate(row):
        if button == "⌫":
            btn = Button(root, text=button, font=("Arial", 18), width=5, height=2, relief="flat",
                         bg="#fff", fg="black", command=delete_last_character)
        else:
            btn = Button(root, text=button, font=("Arial", 18), width=5, height=2, relief="flat",
                         bg="#fff", fg="black" if button.isnumeric() else "green" if button in ["+", "-", "\u00D7", "\u00F7", "^", "()", "%"] else "red" if button == "C" else "black",
                         command=lambda b=button: root.after(1, lambda: on_click(b)))

        btn.grid(row=row_idx, column=col_idx, padx=5, pady=5, sticky="nsew")
        all_buttons.append(btn)

root.mainloop()
