import re

def is_strong_password(password):
    return (
        len(password) >= 8 and
        re.search(r'[A-Z]', password) and
        re.search(r'[a-z]', password) and
        re.search(r'[0-9]', password) and
        re.search(r'[!@#$%^&*(),.?":{}|<>]', password)
    )


password = "this is sss"

result = is_strong_password(password)

print("this is result:  ", result)

print("ths is matching:... ", re.search(r'[a-z]', password))
print("for check 'in': ", re.search(r'is', password))