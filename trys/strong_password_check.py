import re

# Chose any.. most beginer friendly is second one

# Note: regex usage here. re.search() returns None if not found (false  in boolean context)
# and returns a match object if found.
# all 5 criteria for strong password functions returns things other than fasle/none, then passes
# using 'and' operator for all 5 criteria, checks like : if 1st is true, then check 2nd, if 2nd is true, then check 3rd and so on
# so using 'and' is short form of using if else for each criteria like a tree.

# VERSION 1
# directly passing the boolean expression to return statement


def is_strong_password1(password):
    return (
        len(password) >= 8 and
        re.search(r'[A-Z]', password) and
        re.search(r'[a-z]', password) and
        re.search(r'[0-9]', password) and
        re.search(r'[!@#$%^&*(),.?":{}|<>]', password)
    )

# VERSION 2
# if all are true, return true, else return false (readablitly improves)


def is_strong_password2(password):

    if (
        len(password) >= 8 and
        re.search(r'[A-Z]', password) and
        re.search(r'[a-z]', password) and
        re.search(r'[0-9]', password) and
        re.search(r'[!@#$%^&*(),.?":{}|<>]', password)
    ):
        return True
    else:
        return False

# VERSION 3
# all() function is used to check if all elements in an iterable are true, then only true,
# eg. if all([True, True, True]) returns True, if any one is false, then returns false


def is_strong_password3(password):
    return all([
        len(password) >= 8,
        re.search(r'[A-Z]', password),
        re.search(r'[a-z]', password),
        re.search(r'[0-9]', password),
        re.search(r'[!@#$%^&*(),.?":{}|<>]', password)
    ])


password = "this is sss #This is 1234"

# print("ths is matching:... ", re.search(r'[a-z]', password))
# print("for check 'in': ", re.search(r'is', password))

result1 = is_strong_password1(password)
result2 = is_strong_password2(password)
result3 = is_strong_password3(password)


print("result1: ", result1)
print("result2: ", result2)
print("result3: ", result3)


if result1:
    print("Password is strong for version 1")
else:
    print("Password is weak for version 1")
if result2:
    print("Password is strong for version 2")
else:
    print("Password is weak for version 2")
if result3:
    print("Password is strong for version 3")
else:
    print("Password is weak for version 3")
