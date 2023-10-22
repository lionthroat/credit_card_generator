""" My adaptation of the algorithm has been expanded to be an interactive
    tool for generating a variety of test case input, not just valid
    credit card numbers. Whereas the original program had a hardcoded length
    with no ability to specify issuer prefixes, you can now choose lengths
    of 3 - 24 digits, as well as typing 1 or several prefix digits.

    While there is not specifically support for Bank Identification Numbers
    (BINs), if you know a BIN you can include it as part of the prefix. For
    example, Visa cards start with a 4 and use numbers 2 through 6 as the
    BIN. If your BIN is 1111 and you want to test a boundary case of 1110,
    you can specify prefix 41110.

    I have also added comments to the luhn_algorithm function itself, as
    there was little explanation about what it was doing at each step, or
    why.

    For card number length n, with prefix p, Luhn's Alogrithm will generate
    an list of random ints with length: n - p_length - 1.

    Example: You want to test a valid American Express card number. They have
    15 digits and a prefix of "34 or "37".
    Assume you input:
    n = 15,
    p = 37.
    Your p_length is then 2.

    The method will make a list of rand
    ints of 12 digits, because:
    15 - 2 - 1 = 12.

    Then your prefix is inserted at the beginning of the list. Now, Luhn's
    Algorithm can be used to calculate a check digit, which is inserted
    at the end of the list. Your final number of 15 digits is printed to
    std out

    This luhn_algorithm() function was originally built upon the gist here
    https://gist.github.com/sagaya/00149140a1681758fc2242e7af61dbcc
    that has a basic implementation of Luhn's Algorithm. However, upon later
    inspection it was not reversing the payload and then counting digits
    correctly. Then it was summing numbers individually using lists
    instead of as a single number. I don't believe a single line of code
    remains from that source, but it was nevertheless a great starting point
    and deserves the citation."""

import random

credit_card_number = ""


def make_random_ints(number_of_elements):
    random_numbers = []
    for i in range(number_of_elements):
        random_numbers.append(random.randint(0, 9))
    return random_numbers


def luhn_algorithm(n, prefix):
    # start by assuming user didn't specify prefix, i.e. length 0
    p_length = 0

    # then if it isn't 0, figure out how many digits
    if prefix != '':
        p_length = len(prefix)

    # Generate list of random ints for partial card list, aka the payload
    payload = make_random_ints(n - p_length - 1)

    # convert prefix to list of integers
    prefix_digits = [int(digit) for digit in prefix]

    # extend list by adding prefix digits into payload at the beginning
    payload[0:0] = prefix_digits

    sum_even = 0
    sum_odd = 0

    # Luhn's Algorithm
    for index, element in enumerate(reversed(payload)):
        if index % 2 == 0:
            r = element * 2
            if r > 9:
                r -= 9
            sum_even += r
        else:
            sum_odd += element

    total_sum = sum_even + sum_odd

    # Calculate the check digit & append to payload
    check_digit = (10 - (total_sum % 10)) % 10
    payload.append(check_digit)

    # Take payload list and join elements into final credit card string
    credit_card_number = ''.join(map(str, payload))

    # Double-check that our card is the intended length
    final_card_length = len(credit_card_number)
    if (final_card_length == n):
        check_len = True
    else:
        check_len = False

    print(f'\tCard is {n} digits? {check_len}')
    print(f'\tCredit card number: {credit_card_number}')


# Display program title and notes to std out
def show_title():
    print()
    print('\t------------------------------------------------')
    print('\t       CREDIT CARD NUMBER GENERATOR')
    print('\tUse Luhn\'s Algorithm to make valid card numbers')
    print('\t------------------------------------------------')
    print()
    print("""\tNote: For test cases in which you need wrong
              values for check digits, simply change the
              last digit of card number(s) generated.
          """)


# If user needs guidance on issuer prefixes, display common lengths
def prefix_help():
    print('\n\tCredit card prefixes are usually 1-4 digits,')
    print('\t            Visa: 4')
    print('\tAmerican Express: 34 and 37')
    print('\t      MasterCard: 51-55 and 2221-2720, inclusive')
    print('\tNote: MasterCard has 500+ prefixes, but they can')
    print('\tbe narrowed down to categories, like start digit,')
    print('\twhich must be either a 2 or 5')
    print()


# Ask the user if they'd like to specify a card issuer prefix
def get_prefix(n):
    print('\n\tISSUER PREFIX. \'h\' for help, enter to skip')

    if n == 15:
        print('\tHint: for n=15, valid Amex prefixes are 34 or 37\n')

    if n == 16:
        print('\t       Hint: for n=16, Visa prefix = 4,')
        print('\t          Mastercard prefix = 51-55, or')
        print('\t                     2221-2720, inclusive')

    while True:
        p = input('\t2. (Optional) Specify full or partial prefix: ')

        if p == 'h':
            prefix_help()
        elif p.isdigit():
            if len(p) <= n - 1:
                break
            else:
                print(f'Too long! Pref for n={n} cannot exceed {n - 1} digits')
        elif p == '':
            break
        else:
            print('\tInvalid input. Enter valid prefix')

    return (p)


# If user needs guidance on credit card length, display common lengths
def length_help():
    print('\n\tCredit cards usually have 10-19 digits, and')
    print('\tthis program allows 9-24 digit lengths.')
    print('\t            Visa: 16')
    print('\t      MasterCard: 16')
    print('\tAmerican Express: 15')


# User picks the number of digits in credit card
def get_length():
    while True:
        print('\n\tCARD LENGTH. \'h\' for help')
        n = input('\t1. Pick length: ')

        if (n == 'h'):
            length_help()
        elif (n.isdigit()):
            n = int(n)
            if (9 <= n <= 24):
                break
            elif n < 9:
                print('Too short. Card length must be 9-24 digits.')
            else:
                print('Too long. Card length must be 9-24 digits.')
        else:
            print('Invalid input. Enter valid integer between 9 and 24.')

    return (n)


def main():

    show_title()

    n = get_length()
    p = get_prefix(n)

    luhn_algorithm(int(n), p)


if __name__ == '__main__':
    main()
