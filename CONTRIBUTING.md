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

- `poetry run make`

If no errors were thrown, you are good to go.
