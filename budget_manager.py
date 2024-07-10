import json
import os
import matplotlib.pyplot as plt

class BudgetManager: # Class to manage income and expenses
    def __init__(self): # Initialize the list of entries
        self.entries = [] # List of income and expense entries

    def add_entry(self, amount, category, date, entry_type): # Add income or expense entry
        self.entries.append({ # Add a new entry to the list
            'amount': amount,
            'category': category,
            'date': date,
            'type': entry_type
        })

    def view_summary(self): # Get total income, total expense, and balance
        total_income = sum(e['amount'] for e in self.entries if e['type'] == 'income') # Sum of all incomes
        total_expense = sum(e['amount'] for e in self.entries if e['type'] == 'expense') # Sum of all expenses
        balance = total_income - total_expense # Balance = Total Income - Total Expense

        print(f"Total Income: {total_income}") # Print total income
        print(f"Total Expense: {total_expense}") # Print total expense
        print(f"Balance: {balance}") # Print balance

        return total_income, total_expense, balance # Return total income, total expense, and balance

    def category_summary(self): # Get total expenses and incomes by category
        category_totals = {} # Dictionary to store total expenses and incomes by category
        for entry in self.entries: # Loop through all entries
            category = entry['category'] # Get the category of the entry
            amount = entry['amount'] # Get the amount of the entry
            category_totals[category] = category_totals.get(category, 0) + amount # Add the amount to the category total

        for category, total in category_totals.items(): # Loop through all categories and totals
            print(f"{category}: {total}") # Print the category and total

        return category_totals # Return the dictionary of category totals
 
    def save_to_file(self, filename): # Save expenses to a file
        try:
            script_dir = os.path.dirname(__file__)  # Get the directory of the script
            file_path = os.path.join(script_dir, filename) # Get the full path of the file
            with open(file_path, 'w') as file: # Open the file for writing
                json.dump(self.entries, file, indent=4) # Write the entries to the file
            print(f"Expenses saved to {file_path}") # Print the path of the saved file
        except IOError as e: 
            print(f"Error saving expenses: {e}") # Print an error message if there is an error

    def load_from_file(self, filename): # Load expenses from a file
        try:
            script_dir = os.path.dirname(__file__)  # Get the directory of the script
            file_path = os.path.join(script_dir, filename) # Get the full path of the file
            with open(file_path, 'r') as file: # Open the file for reading
                self.entries = json.load(file) # Load the entries from the file
            print(f"Expenses loaded from {file_path}") # Print the path of the loaded file
        except FileNotFoundError:  # If the file is not found
            print(f"File {file_path} not found. No entries are loaded.") # Print a message that the file is not found
        except IOError as e: # If there is an error loading the file
            print(f"Error loading expenses: {e}") # Print an error message

    def plot_summary(self): # Plot total expenses and incomes by category
        category_totals = self.category_summary() # Get the total expenses and incomes by category
        categories = list(category_totals.keys()) # Get the categories
        amounts = list(category_totals.values()) # Get the amounts

        plt.figure(figsize=(10, 5)) # Set the size of the plot
        plt.bar(categories, amounts) # Create a bar plot
        plt.xlabel('Category') # Set the x-axis label
        plt.ylabel('Amount') # Set the y-axis label
        plt.title('Expenses and Incomes by Category') # Set the title of the plot
        plt.show() # Show the plot

def main(): # Main function to run the budget manager
    budget_manager = BudgetManager() # Create a budget manager object
    filename = 'budget.json'  # File to save and load expenses

    budget_manager.load_from_file(filename) # Load expenses from file

    while True: # Main loop to interact with the budget manager
        print("\nBudget Manager") # Print the menu
        print("1. Add Income")
        print("2. Add Expense")
        print("3. View Summary")
        print("4. View Category Summary")
        print("5. Save to File")
        print("6. Load from File")
        print("7. Plot Summary")
        print("8. Exit")
        choice = input("Choose an option: ") # Get the user's choice

        if choice == '1': # Add income
            amount = float(input("Enter income amount: "))
            category = input("Enter income category: ")
            date = input("Enter date (DD.MM.YYYY): ")
            budget_manager.add_entry(amount, category, date, 'income')
        elif choice == '2': # Add expense
            amount = float(input("Enter expense amount: "))
            category = input("Enter expense category: ")
            date = input("Enter date (DD.MM.YYYY): ")
            budget_manager.add_entry(amount, category, date, 'expense')
        elif choice == '3': # View summary
            budget_manager.view_summary()
        elif choice == '4': # View category summary
            budget_manager.category_summary()
        elif choice == '5': # Save to file
            budget_manager.save_to_file(filename)
        elif choice == '6': # Load from file
            budget_manager.load_from_file(filename)
        elif choice == '7': # Plot summary
            budget_manager.plot_summary()
        elif choice == '8': # Exit
            break
        else: # Invalid option
            print("Invalid option. Please try again.") # Print an error message

    print("Exiting Budget Manager.") # Print a message when exiting

if __name__ == "__main__": # Run the main function if the script is run directly
    main() # Run the main function
