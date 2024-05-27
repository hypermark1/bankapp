def get_float_input(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print('Invalid input. Please enter a valid number.')


def create_account(account):
    print('- Create account -')
    while True:
        name = input('Enter name: ')
        if name:
            break
        else:
            print('Name cannot be empty. Please enter a valid name.')
    birth_year = int(input('Enter year of birth: '))
    print('Account created:', name, '(' + str(2024 - birth_year), 'years)')
    account['pwd'] = input('Create password: ')
    print('Password saved. Password:', account['pwd'])
    account['name'] = name
    account['balance'] = 0
    account['max_balance'] = float('inf')
    save(account, 'account.txt')


def check_password(account):
    attempts = 3
    for i in range(attempts):
        entered_password = input('Enter your password: ')
        if entered_password == account['pwd']:
            print('Password is correct. Proceeding with the operation...')
            break
        else:
            print('Incorrect password.')
            if i < attempts - 1:
                print('Please try again.')
            else:
                print('Denied.')
                exit()


def max_balance(account):
    print('- Limit the maximum amount of funds -')
    account['max_balance'] = get_float_input('Indicate the maximum amount of funds on the account: ')
    save(account, 'account.txt')


def deposit(account):
    print('- Deposit -')
    deposit = get_float_input('Enter deposit amount: ')
    account['balance'] = float(account['balance']) + deposit
    print('Account successfully top-uped. Current balance:', account['balance'])
    save(account, 'account.txt')


def withdraw(account):
    print('- Withdrawal -')
    print('Current balance:', account['balance'])
    withdraw = get_float_input('Enter withdrawal amount: ')
    if float(account['balance']) >= withdraw:
        account['balance'] = float(account['balance']) - withdraw
        print('Success. Current balance:', account['balance'])
    else:
        print('Not enough funds')
    save(account, 'account.txt')


def add_transaction(account):
    print('- Add new transaction -')
    comment = input('Enter comment for transaction: ')
    amount = get_float_input('Enter amount of transaction: ')
    transaction = {
        'comment': comment,
        'amount': amount
    }
    account['transactions'].append(transaction)
    print('Pending transactions:', len(account['transactions']))
    save(account, 'account.txt')


def apply_transactions(account):
    print('- Apply pending transactions -')
    rejected_transactions = []
    total_rejected_amount = 0
    for transaction in account['transactions']:
        max_balance = float(account['max_balance']) if account['max_balance'] else float('inf')
        if float(transaction['amount']) <= max_balance:
            if float(account['balance']) - float(transaction['amount']) >= 0:
                account['balance'] = str(float(account['balance']) - float(transaction['amount']))
                print('Accepted:', transaction['comment'] + '.', 'Current balance:', account['balance'])
            else:
                print('Rejected, not enough funds:', transaction['comment'])
                rejected_transactions.append(transaction)
                total_rejected_amount += float(transaction['amount'])
    account['transactions'] = rejected_transactions
    save(account, 'account.txt')
    if total_rejected_amount > 0:
        print('Total amount needed to apply all rejected transactions:', total_rejected_amount)


def save(account, file_name):
    with open(file_name, 'w') as fout:
        fout.write(account['name'] + '\n')
        fout.write(account['pwd'] + '\n')
        fout.write(str(account['balance']) + '\n')
        fout.write(str(account['max_balance']) + '\n')

        fout.write(str(len(account['transactions'])) + '\n')
        for transaction in account['transactions']:
            fout.write(transaction['comment'] + '\n')
            fout.write(str(transaction['amount']) + '\n')


def load(account, file_name):
    with open(file_name) as fin:
        account['name'] = fin.readline().strip()
        account['pwd'] = fin.readline().strip()
        account['balance'] = fin.readline().strip()
        account['max_balance'] = fin.readline().strip()

        account['transactions'] = []
        transactions_cnt_line = fin.readline().strip()
        transactions_cnt = int(transactions_cnt_line) if transactions_cnt_line else 0
        for i in range(transactions_cnt):
            comment = fin.readline().strip()
            amount_line = fin.readline().strip()
            amount = float(amount_line) if amount_line else 0.0  # Change this line
            transaction = {
                'comment': comment,
                'amount': amount
            }
            account['transactions'].append(transaction)
    save(account, 'account.txt')


def transaction_stat(account):
    if not account['transactions']:
        print('No transactions found.')
        return

    freq = {}
    for transaction in account['transactions']:
        freq[transaction['amount']] = freq.get(transaction['amount'], 0) + 1
    for amount, cnt in freq.items():
        print('Transactions in the sum of:', str(amount), '-', str(cnt), 'pc(s)')


def login(account):
    print('- Login -')
    try:
        load(account, 'account.txt')
    except FileNotFoundError:
        print('No account data found.')
        return
    name = input('Enter your name: ')
    pwd = input('Enter your password: ')
    if name == account['name'] and pwd == account['pwd']:
        print('Login successful.')
    else:
        print('Login failed. No account found with that name and password.')
        create_account_prompt = input('Do you want to create a new account? (yes/no): ')
        if create_account_prompt.lower() == 'yes':
            create_account(account)


def filter_transactions(account):
    threshold = get_float_input('Enter the minimum sum for transactions to display: ')
    print('---')

    def transaction_generator():
        for transaction in account['transactions']:
            if transaction['amount'] >= threshold:
                yield transaction

    generator = transaction_generator()
    for transaction in generator:
        print('Transaction comment:', transaction['comment'])
        print('Transaction amount:', transaction['amount'])
        print('---')


def run(account):
    recover_prompt = input('Do you want to recover data from the previous session? (yes/no): ')
    if recover_prompt.lower() == 'yes':
        try:
            login(account)
        except FileNotFoundError:
            print('No account data found.')


def main():
    account = {
        'name': '',
        'pwd': '',
        'balance': '',
        'max_balance': '',
        'transactions': []
    }
    run(account)

    while True:
        print('')
        print('Operations:')
        print('1. Create account')
        print('2. Deposit')
        print('3. Withdraw')
        print('4. Balance')
        print('5. Limit')
        print('6. Add transaction')
        print('7. Apply transaction(s)')
        print('8. Statistics of transaction(s)')
        print('9. Filtration of transaction(s)')
        print('10. Quit')

        op = int(input('Select operation number: '))

        if op == 1:
            create_account(account)

        elif op == 2:
            deposit(account)

        elif op == 3:
            check_password(account)
            withdraw(account)

        elif op == 4:
            check_password(account)
            print('Current balance:', str(account['balance']))

        elif op == 5:
            check_password(account)
            max_balance(account)

        elif op == 6:
            check_password(account)
            add_transaction(account)

        elif op == 7:
            check_password(account)
            apply_transactions(account)

        elif op == 8:
            check_password(account)
            transaction_stat(account)

        elif op == 9:
            check_password(account)
            filter_transactions(account)

        elif op == 10:
            print('Quitting...')
            break

        else:
            print('Unexisting operation')
        print('')


if __name__ == "__main__":
    main()
