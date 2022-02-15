# Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change. Please make sure to update tests as appropriate.

To set up a development environment:

- Install [Poetry](https://python-poetry.org/docs/master/#installation)
- Install `Make` (this will be removed in the future)
- Then, do `poetry config virtualenvs.in-project true` (Only once. This will be valid for all Poetry projects on your machine.)
- Clone this repository
- On the root of the repository, do `poetry install --no-root`
- Don't forget to activate the virtual environment (the `.venv` folder) on your IDE

After making your changes and writting the corresponding tests, run the following from the root of the repository:

- `poetry run make test`

If no errors were thrown, you are good to make a PR. Before doing so, run the more complete suite of checks:

- `poetry run make`

Fix the errors, if any, and then open the PR.

## Writing tests

Writing tests is simple.

- Create a file called `test_something.py` in the `tests`folder
- Inside the file, import `cadcad` and declare a `State` class as appropriate
- Write your tests as a series of functions with prototype:

  ```python
  def test_this_and_that() -> None
  ```

- Then run `poetry run make test`
