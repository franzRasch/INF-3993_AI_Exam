# Tools used in the project

## CSpell

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

## Black

We use black to format the python code. It is a code formatter that formats the code according to PEP 8.
Can be downloaded from [here](https://marketplace.visualstudio.com/items/?itemName=ms-python.black-formatter)

## Prettier

We use prettier to properly format the code of the project. Please install a prettier plugin for your editor.
For use with _Visual Studio Code_, the _format on save_ option should be turned on to continuously keep your files formatted.
The config for prettier can be changed in the `.prettierrc` file.

## Eslint

Eslint helps you discover errors in your code. This scan your code for readability, functionality errors and some small formatting hints.
The config can be found in `.eslintrc.json`
