# sem

[![pyqt6](https://img.shields.io/badge/PyQt6-FF0000)](https://pypi.org/project/PyQt6/)
[![sqlite](https://img.shields.io/badge/SQLite-FF0000)](https://www.sqlite.org/index.html)
[![pylint](https://img.shields.io/badge/linting-pylint-blue)](https://github.com/pylint-dev/pylint)
[![black](https://img.shields.io/badge/code%20style-black-black)](https://github.com/psf/black)
[![poetry](https://img.shields.io/badge/build-poetry-blue)](https://github.com/python-poetry/poetry)
[![mkdocs](https://img.shields.io/badge/documentation-mkdocs-blue)](https://github.com/mkdocs/mkdocs)




`sem` (Simple Expense Manager) is a simple Python utility for
the management of domestic expenses.

A streamlined Qt graphical interface allows straightforward
management and analysis of expense data stored in SQLite databases.




## Current capabilities

- Expense data management via SQLite database
- Manual addition of single expenses or bulk importing from CSV
  files
- Reviewing and summarizing of expenses by date and type
- Expense deletion via graphical interface
- Exporting and backup of user databases to CSV files




## Imported libraries

The following external libraries are imported in `sem`, and
required for its operation:

- [PyQt6](https://www.riverbankcomputing.com/software/pyqt/)
  (GUI toolkit and Model/View interfaces)




## Dependencies and Setup

`sem` is packaged with `poetry`: the command

```
$ poetry install
```

will setup a virtual environment will all required
dependencies. The command

```
$ poetry run python -m modules.sem
```

or a call to the launch bash script

```
$ ./sem-qt
```

will execute the program.




## To Do

- [ ] Documentation (and access to it)
- [ ] More ergonomic visualization and addition of new expenses
- [ ] Robust error management
