import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkcalendar import DateEntry
import matplotlib.pyplot as plt
import os
import csv
import json

class BudgetManager:
    def __init__(self):
        self.entries = []

    def add_entry(self, amount, category, date, entry_type):
        self.entries.append({
            'amount': amount,
            'category': category,
            'date': date,
            'type': entry_type
        })

    def delete_entry(self, index):
        if index is not None:
            del self.entries[index]

    def view_summary(self):
        total_income = sum(e['amount'] for e in self.entries if e['type'] == 'income')
        total_expense = sum(e['amount'] for e in self.entries if e['type'] == 'expense')
        balance = total_income - total_expense
        return total_income, total_expense, balance

    def category_summary(self):
        category_totals = {}
        for entry in self.entries:
            category = entry['category']
            amount = entry['amount']
            if entry['type'] == 'expense':
                amount = -amount
            category_totals[category] = category_totals.get(category, 0) + amount
        return category_totals

    def plot_summary(self):
        category_totals = self.category_summary()
        categories = list(category_totals.keys())
        amounts = list(category_totals.values())

        colors = ['green' if amount >= 0 else 'red' for amount in amounts]

        plt.figure(figsize=(10, 6))
        plt.bar(categories, amounts, color=colors)
        plt.xlabel(translate("plot_category"))
        plt.ylabel(translate("plot_amount"))
        plt.title(translate("plot_title"))
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()

    def save_to_csv(self, filename):
        try:
            with open(filename, 'w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=['amount', 'category', 'date', 'type'])
                writer.writeheader()
                for entry in self.entries:
                    writer.writerow(entry)
        except IOError as e:
            print(f"Error saving data: {e}")

    def load_from_csv(self, filename):
        try:
            with open(filename, 'r') as file:
                reader = csv.DictReader(file)
                self.entries = list(reader)
                for entry in self.entries:
                    entry['amount'] = float(entry['amount'])
        except FileNotFoundError:
            print(f"File {filename} not found. No data loaded.")
        except IOError as e:
            print(f"Error loading data: {e}")

def load_translations(filename):
    try:
        filepath = os.path.join(os.path.dirname(__file__), 'translations', filename)
        with open(filepath, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Translation file {filepath} not found.")
        return {}
    except json.JSONDecodeError:
        print(f"Error decoding JSON from file {filepath}.")
        return {}

# Global variable to hold the translations
translations = {}

def translate(key):
    return translations.get(key, key)

def create_main_window(language_code='en.json'):
    global translations
    global root
    global budget_manager
    global entry_type_var
    global amount_entry
    global category_entry
    global date_entry
    global income_radio
    global expense_radio
    global summary_label
    global table

    root = tk.Tk()
    translations = load_translations(language_code)

    def update_texts():
        # Update texts in various parts of the GUI
        root.title(translate("app_title"))

        # Input Frame Labels and Buttons
        amount_label.config(text=translate("amount_label"))
        category_label.config(text=translate("category_label"))
        date_label.config(text=translate("date_label"))
        type_label.config(text=translate("type_label"))
        income_radio.config(text=translate("income_radio"))
        expense_radio.config(text=translate("expense_radio"))
        add_button.config(text=translate("add_button"))
        plot_button.config(text=translate("plot_button"))
        save_button.config(text=translate("save_button"))
        load_button.config(text=translate("load_button"))
        delete_button.config(text=translate("delete_button"))

        # Summary
        total_income, total_expense, balance = budget_manager.view_summary()
        summary_label.config(
            text=f"{translate('total_income')}: {total_income:.2f}\n{translate('total_expense')}: {total_expense:.2f}\n{translate('balance')}: {balance:.2f}"
        )

        # Menu Items
        file_menu.entryconfig(0, label=translate("exit"))
        help_menu.entryconfig(0, label=translate("help_title"))
        help_menu.entryconfig(1, label=translate("about_title"))
        language_menu.entryconfig(0, label=translate("english"))
        language_menu.entryconfig(1, label=translate("finnish"))

    def change_language(new_language_code):
        global translations
        translations = load_translations(new_language_code)
        update_texts()

    # Initialize BudgetManager
    budget_manager = BudgetManager()

    # Create frames for layout
    frame_input = ttk.Frame(root, padding="10")
    frame_input.grid(row=0, column=0, sticky=tk.W+tk.E)

    frame_buttons = ttk.Frame(root, padding="10")
    frame_buttons.grid(row=1, column=0, sticky=tk.W+tk.E)

    frame_table = ttk.Frame(root, padding="10")
    frame_table.grid(row=2, column=0, sticky=tk.W+tk.E+tk.N+tk.S)

    # Amount Entry
    amount_label = ttk.Label(frame_input, text=translate("amount_label"))
    amount_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
    amount_entry = ttk.Entry(frame_input, width=30)
    amount_entry.grid(row=0, column=1, padx=5, pady=5)

    # Category Entry
    category_label = ttk.Label(frame_input, text=translate("category_label"))
    category_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
    category_entry = ttk.Entry(frame_input, width=30)
    category_entry.grid(row=1, column=1, padx=5, pady=5)

    # Date Entry
    date_label = ttk.Label(frame_input, text=translate("date_label"))
    date_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
    date_entry = DateEntry(frame_input, width=27, background='darkblue', foreground='white', borderwidth=2)
    date_entry.grid(row=2, column=1, padx=5, pady=5)
    date_entry.set_date(date_entry.get_date())  # Set the current date by default

    # Type Radio Buttons
    type_label = ttk.Label(frame_input, text=translate("type_label"))
    type_label.grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
    entry_type_var = tk.StringVar(value="income")
    income_radio = ttk.Radiobutton(frame_input, text=translate("income_radio"), variable=entry_type_var, value="income")
    income_radio.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)
    expense_radio = ttk.Radiobutton(frame_input, text=translate("expense_radio"), variable=entry_type_var, value="expense")
    expense_radio.grid(row=3, column=1, padx=5, pady=5, sticky=tk.E)

    # Buttons
    add_button = ttk.Button(frame_buttons, text=translate("add_button"), command=add_entry_to_manager)
    add_button.grid(row=0, column=0, padx=5, pady=5)
    plot_button = ttk.Button(frame_buttons, text=translate("plot_button"), command=plot_summary)
    plot_button.grid(row=0, column=1, padx=5, pady=5)
    save_button = ttk.Button(frame_buttons, text=translate("save_button"), command=save_data)
    save_button.grid(row=0, column=2, padx=5, pady=5)
    load_button = ttk.Button(frame_buttons, text=translate("load_button"), command=load_data)
    load_button.grid(row=0, column=3, padx=5, pady=5)
    delete_button = ttk.Button(frame_buttons, text=translate("delete_button"), command=delete_selected)
    delete_button.grid(row=0, column=4, padx=5, pady=5)

    # Summary Label
    summary_label = ttk.Label(frame_input, text="", padding="5")
    summary_label.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

    # Table
    table = ttk.Treeview(frame_table, columns=("amount", "category", "date", "type"), show="headings")
    table.heading("amount", text=translate("amount_label"))
    table.heading("category", text=translate("category_label"))
    table.heading("date", text=translate("date_label"))
    table.heading("type", text=translate("type_label"))
    table.grid(row=0, column=0, padx=5, pady=5)

    # Menu
    menu_bar = tk.Menu(root)
    root.config(menu=menu_bar)

    file_menu = tk.Menu(menu_bar, tearoff=0)
    file_menu.add_command(label=translate("exit"), command=root.quit)
    menu_bar.add_cascade(label=translate("file_menu"), menu=file_menu)

    help_menu = tk.Menu(menu_bar, tearoff=0)
    help_menu.add_command(label=translate("help_title"), command=show_help)
    help_menu.add_command(label=translate("about_title"), command=show_about)
    menu_bar.add_cascade(label=translate("help_menu"), menu=help_menu)

    language_menu = tk.Menu(menu_bar, tearoff=0)
    language_menu.add_command(label=translate("english"), command=lambda: change_language('en.json'))
    language_menu.add_command(label=translate("finnish"), command=lambda: change_language('fi.json'))
    menu_bar.add_cascade(label=translate("language_menu"), menu=language_menu)

    update_texts()
    root.mainloop()

def add_entry_to_manager():
    try:
        amount = float(amount_entry.get())
        category = category_entry.get()
        date = date_entry.get_date()
        entry_type = entry_type_var.get()

        if not category:
            raise ValueError(translate("invalid_category"))

        budget_manager.add_entry(amount, category, date, entry_type)
        update_summary()
    except ValueError as e:
        messagebox.showerror(translate("error"), str(e))

def update_summary():
    total_income, total_expense, balance = budget_manager.view_summary()
    summary_label.config(
        text=f"{translate('total_income')}: {total_income:.2f}\n{translate('total_expense')}: {total_expense:.2f}\n{translate('balance')}: {balance:.2f}"
    )
    update_table()

def update_table():
    for item in table.get_children():
        table.delete(item)
    for entry in budget_manager.entries:
        table.insert("", "end", values=(entry['amount'], entry['category'], entry['date'], entry['type']))

def plot_summary():
    budget_manager.plot_summary()

def save_data():
    filename = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    if filename:
        budget_manager.save_to_csv(filename)

def load_data():
    filename = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if filename:
        budget_manager.load_from_csv(filename)
        update_table()
        update_summary()

def delete_selected():
    selected_item = table.selection()
    if selected_item:
        index = table.index(selected_item[0])
        budget_manager.delete_entry(index)
        update_table()
        update_summary()
    else:
        messagebox.showwarning(translate("warning"), translate("no_selection"))

def show_help():
    messagebox.showinfo(translate("help_title"), translate("help_message"))

def show_about():
    messagebox.showinfo(translate("about_title"), translate("about_message"))

if __name__ == "__main__":
    create_main_window('en.json')  # Default to English
