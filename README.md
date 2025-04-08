# INF-3993_AI-Exam

## Contributors: Franz Ingebrigtsen, Marie Stenhaug and Skjalg Slubowski

## Pre-requisites

### Tools

#### CSpell

This repo uses CSpell as a spellchecker, being enforced in CI.
The CI will check the spelling of all `.md` and `.cs`
You can learn more about CSpell [here](https://cspell.org/docs/getting-started/)

You can install the `cspell` CLI globally with npm.

```bash
npm install -g cspell@latest
```

After installation spelling can be checked by running:

```bash
cspell "**/*.cs" "**/*.md"
```

Alternatively there is a VSCode extension available [here](https://marketplace.visualstudio.com/items?itemName=streetsidesoftware.code-spell-checker).

If CSpell incorrectly flags a word you can add it to `project-words.txt`.

#### Prettier

We use prettier to properly format the code of the project. Please install a prettier plugin for your editor.
For use with _Visual Studio Code_, the _format on save_ option should be turned on to continuously keep your files formatted.
The config for prettier can be changed in the `.prettierrc` file.

#### eslint

Eslint helps you discover errors in your code. This scan your code for readability, functionality errors and some small formatting hints.
The config can be found in `.eslintrc.json`

## For developing

1. Create a new venv

   ```bash
   python -m venv venv  # or 'python3' depending on the setup
   ```

2. Activate the new venv
   Windows:

   ```bash
   .\venv\Scripts\activate
   ```

   Mac/Linux:

   ```bash
   source venv/bin/activate
   ```

3. Install dependencies

   ```bash
   pip install -r requirements.txt
   ```

   4 Run "node -v" to check for node js, if you don't have node: install it

### Backend

#### Run backend

```bash
uvicorn main:app --reload
```

#### Access backend

```bash
    http://localhost:8000/
```

#### Access backend api endpoints

```bash
    http://localhost:8000/docs
```

### Frontend

#### Run frontend

```bash
npm start

```
