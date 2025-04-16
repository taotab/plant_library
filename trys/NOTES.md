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


## Next additions:

- Make logout page.. *(now works for manually add link)
- Edit options like remove users, edit user credentials
- More robustness, try error catches and comment prints for better Security and debug.