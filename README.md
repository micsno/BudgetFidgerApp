# Budget Manager
This project is a practical work for the JAMK programming course by Tomi Kouvala - AD2307.

The Budget Manager is a Python script designed to help users manage their budget entries. It allows users to add income and expense entries, view summaries of their finances, save entries to a file (budget.json), load entries from a file, and plot a summary of expenses and incomes by category using matplotlib.

## Features

- Add Entry: Add income or expense entries with amount, category, and date.
- View Summary: View total income, total expense, and balance.
- Category Summary: View total amounts grouped by category.
- Save to File: Save all entries to a JSON file (budget.json).
- Load from File: Load entries from budget.json.
- Plot Summary: Plot a bar chart showing expenses and incomes by category.
- Command-Line Interface: Simple command-line interface for interaction.

## Installation

1. Clone Repository: Clone the repository to your local machine:

    ```bash
    git clone https://gitlab.labranet.jamk.fi/AD2307/harjoitustyoe_ad2307_ttc2030.git
    ```

2. Install Dependencies: Make sure you have Python 3 installed. Install matplotlib if not already installed:

    ```bash
    pip install matplotlib
    ```

## Usage

1. Run the Script: Run the script budget_manager.py using Python:

    ```bash
    python budget_manager.py
    ```

    Options Available:
    - Enter 1 to add income.
    - Enter 2 to add expense.
    - Enter 3 to view summary.
    - Enter 4 to view category summary.
    - Enter 5 to save entries to budget.json.
    - Enter 6 to load entries from budget.json.
    - Enter 7 to plot summary (requires matplotlib).
    - Enter 8 to exit the program.

2. File Operations:
    - Entries are saved to budget.json in the same directory as budget_manager.py.
    - Make sure you have write permissions for the directory where budget_manager.py resides.