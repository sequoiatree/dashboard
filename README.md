# Da$hboard

Your Da$hboard is a minimal personal finance tool designed to help you navigate month-to-month budgeting and investing. Use it to review your transaction history, calculate your portfolio allocation, and more.

[TODO: screenshot of main page (use example data)]

## Features

### Budgeting

* **Transaction History:** On the main page you'll find your recent transaction history, nicely cleaned up and ready for review. This makes it easy for you to assess your spending habits and identify any fraudulent transactions, when you sit down to do your monthly financial book-keeping.
* **Custom Descriptions:** In the screenshot above, all the transactions have simple, easily readable descriptions. That's thanks to the aliasing bar under the transactions table. Want to relabel a certain transaction, and all future transactions like it? Just enter a valid RegEx pattern on the left, and the new description on the right. Or leave the right side blank, if you'd rather just hide those transactions altogether!
* **Account Breakdown:** To the left of each transaction you'll notice a colorful box indicating which bank account its associated with. This is so you can see if you're using each of your accounts for the right kinds of transactions.
* **Transaction Tagging:** Some transactions also bare a tag. I tag all my purchases as either "property expenses" or "spending", but it's easy to make your own tags if you like. If you notice a transaction was inaccurately tagged, just click the tag to correct it.
* **Summary Metrics:** If you scroll to the bottom of the table, you'll see the your per-tag totals (e.g. total property expenses, total spending, etc.) for last month and the this month so far. You'll also see your average for the year-to-date, and how much you're under or over the budget you set for yourself.

### Investing

* **Allocation Calculator:** Besides helping you stick to your budget, your Da$hboard is a handy allocation calculator for the all-equity Boglehead investor. Just enter your target allocation between VTI and VXUS, your current balance in each, and how much cash you'd like to invest now. Your Da$hboard will do the math and tell you how much to invest in each, to get your target allocation back on track without selling any stock. (Note the calculator assumes your non-VXUS investments all track VTI. This is a convenient assumption for the strict Boglehead whose retirement accounts, HSA, etc. are all-in on VTI-like funds such as VIIIX.)

## Instructions

### Setup

1. Install Python (and its native package manager, pip) if you haven't already. To verify you have them both installed you can run these commands in the terminal.

   ```bash
   $ python --version
   Python 3.9.0
   $ pip --version
   pip 21.2.4 from /Library/Frameworks/Python.framework/Versions/3.9/lib/python3.9/site-packages/pip (python 3.9)
   ```

   You should see outputs similar to the above. If you instead see `-bash: python: command not found` or `-bash: pip: command not found`, then you don't have them installed. You can find installation instructions online.

1. Download this repository. You can do this by clicking the green "Code" button at the top of the page, clicking "Download ZIP" in the dropdown menu that appears, and finally unzipping the downloaded folder on your computer. Keep it somewhere you won't lose it, like your desktop.

1. Install the necessary requirements.

   ```bash
   $ cd Da\$hboard
   $ pip install -r requirements.txt
   ```

1. Customize your configurations in `Da\$hboard/data/configs.json`.

### Usage

Every month …

1. Log into each of your bank accounts and download a CSV of your recent transactions. This is quick and easy if you keep a list of direct links to each of them.

1. Launch the `Da\$hboard` app.

   ```bash
   $ cd Da\$hboard
   $ python app.py
   ```

   For convenience, you may optionally want to set up an alias in your `~/.bash_aliases` file. Here's mine:

   ```
   alias dashboard="python ~/Desktop/Da\$hboard/app.py"
   ```

1. Navigate to http://127.0.0.1:5000.

1. Upload the CSV files you downloaded from your bank accounts.

Note that this app presently only knows how to parse data from the banks that I personally use, so yours may be unsupported — but don't worry! It's very easy to add support for a new bank. If there's a problem, you should see an error message in the terminal. I wrote all the error messages myself, so hopefully they're descriptive and clear. They will tell you what you need to do.

### Development

1. Install NPM.
1. Install the necessary requirements.

   ```bash
   $ cd Da\$hboard
   $ npm install --no-optional
   ```

1. Make your desired changes.
   * For changes to Python files, you don't have to do anything special.
   * For changes to JavaScript files, run `npm run watch-js`.
   * For changes to SASS files, run `npm run watch-css`.
1. Launch the app to try out your new features!
