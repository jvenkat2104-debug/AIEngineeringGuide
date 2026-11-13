# Workspace and free learning tools

**Level: Beginner | Learning draft | Resource pages checked: 13 November 2026**

Goal: run the canteen exercise without a paid database or cloud account. Use one route below. A laptop or desktop is preferable for editing; the guide itself is readable on a phone.

## Recommended route: Python with built-in SQLite

[Python is free and open source](https://www.python.org/about/). Install a stable Python 3 release from [python.org](https://www.python.org/downloads/), using its operating-system instructions. The starter supports Python 3.9 or newer and uses only the standard library. No pip packages, database server or API keys are needed.

1. Download and extract the [starter ZIP](../../../downloads/canteen-starter.zip).
2. Open a terminal in the extracted `canteen-starter` folder.
3. Run `python --version`, then `python lab.py`. On Windows try `py --version` and `py lab.py` if `python` is unavailable. On macOS/Linux the command may be `python3`.
4. Expect “Loaded: 3 products, 5 orders, 6 payments (synthetic data)” and order values 4000, 5000, 2000, 10000 and 3000 paise.
5. Open `lab.py` in a text editor. Edit only the `query` string for the SQL exercises. Keep straight quotes; use triple quotes for multi-line SQL.

The database exists only while the script runs. Each rerun loads a fresh copy; you do not need to delete or reset a database file. This is deliberate for the first lab.

## Optional browser route: Colab

[Google Colab](https://developers.google.com/colab) offers a hosted notebook environment and free compute, alongside paid options. The small lab needs only a CPU, not a paid tier or GPU. Google sign-in may be required; free resources have availability/session limits, so download your work. AI features are optional and their availability may vary.

Create a notebook, upload the starter ZIP through its file panel, then run these cells:

```python
import zipfile
with zipfile.ZipFile('canteen-starter.zip') as archive:
    archive.extractall('canteen-work')
```

```python
%run canteen-work/canteen-starter/lab.py
```

To experiment without editing a file, run:

```python
import sys
sys.path.insert(0, 'canteen-work/canteen-starter')
from lab import build_database
connection = build_database()
connection.execute('SELECT COUNT(*) FROM orders').fetchall()
```

Expected result: `[(5,)]`. Replace the SELECT with your exercise query. Close `connection` when finished. Session files can disappear; save your SQL in the notebook and download a copy. This notebook route is documented as an option; the reference script is tested locally and in CI, not through every hosted notebook configuration.

## Free practice and reference links

| Resource | Use it for | Access and limits |
| --- | --- | --- |
| [SQLBolt](https://sqlbolt.com/) | Browser lessons on SELECT, filtering, joins and aggregation | Public interactive lessons; no local database installation. Exercises use their own data, not our canteen files. The introductory page was accessible during checking; we did not audit every exercise. |
| [Python beginner resources](https://www.python.org/about/) | Find beginner and installation guidance | Public/free official resources; choose the non-programmer route if loops and functions are new. |
| [Python tutorial](https://docs.python.org/3/tutorial/) | Functions, collections, files and exceptions | Free reference, but explicitly assumes basic programming knowledge. Use after an introduction. |
| [Python sqlite3 documentation](https://docs.python.org/3/library/sqlite3.html) | Understand connections, queries and parameters | Public official reference; SQL dialect here is SQLite, with differences from other databases. |
| [Colab](https://developers.google.com/colab) | Run Python in a browser | Free compute option, optional paid tiers, sign-in and usage/session limits. No paid upgrade is needed for this exercise. |

These are learning links, not endorsements of every linked feature. Access conditions can change; no purchase or paid AI subscription is required by this pathway.

## If something fails

“Can't open file”: check the terminal folder and extraction location. “No module named sqlite3”: use an official Python installation with SQLite support. A CSV-not-found error usually means a file was moved out of the starter folder. A syntax error after editing often means broken quotes or indentation: restore the ZIP copy and change only the query.

Completion: run the lab, explain what is stored in memory, and save one changed SELECT query. Next: [Meet the data](canteen-data.md).
