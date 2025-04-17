# Purpose: Personal explanations, tips, observations, just for understanding

## Session using:

- Flask run on HTTP stateless. Flask forgets everything going to other pages. *(also usage in redirect() templates).
- No *global variables* reliably used to track across pages.
- Flask stores data safely and securely encrypted (using API SECRET KEY) in browser cookies


## Database SQlite3 integration:

- Why sqlite3 chosed? - Easy use, light, and pre-installed with python
- Add login and register features, along with credentials check using database enqure queries instead of previous hardcoded.
- **Note-** Use absolute path of files in python and flask in same code directory by default to save headache and errors and robustness of code consistency. 
- Issues occur with vscode working directory and script local directory.

    1. Use **url_for()** for absolute current templates and static files.
    2. For file paths in python scripts:
        ``` python
        import os
        print("👀 Current working dir:", os.getcwd())
        ```

## Added:

- Logout page added, link in header navbar

## Regex instead of for loops:

- for password conformation checks like similar, is capital or special characters, digits is there ,,, all functions check, usual method is the for loop or while,, check each character and flag...
- Why only use in flask? Javascript and html can be quick and ui/ux design.. but can be bypassed, flask check backend is better and secure.
- Why use regex? For character comparisions, its better, simple and less code..
- **What's the logic? idk, must do research. REGEX vs FOR LOOPs**
    1. for more info on regex use: https://www.w3schools.com/python/python_regex.asp
    2. (regular expression), like a pattern searching regex engine, to search in a given string.

## Next additions:

- Make password repeat confirmation check *(see my previous btech project)*
- Edit options like remove users, edit user credentials
- More robustness, try error catches and comment prints for better Security and debug.