# Dylons Advent of Code 2024 Adventures

The 2024 Advent of Code event can be found at <https://adventofcode.com/2024>.

## Local Development

### Prerequisites

* This project uses [Python 3.13](https://www.python.org/downloads/release/python-3130/).
* Dependencies are managed using [Poetry](https://python-poetry.org/docs/#installation). If you haven't installed it yet, use this command:

    ```shell
    pip install poetry
    ```

* [Pre-commit](https://pre-commit.com/) is used to enforce code quality. If you don't have pre-commit installed, you can install it using the following command:

    ```shell
    pip install pre-commit
    ```

### Setting up the Development environment

1. Initialize pre-commit:

    ```shell
    pre-commit install
    ```

2. Install dependencies and activate the virtual environment:

    ```shell
    poetry install
    poetry shell
    ```

### Running Tests

After activating the virtual environment with the command `poetry shell`, use the following command to run tests:

```shell
pytest
```

### Runing the Solutions

You can run any of the solutions with the following command:

```shell
python3 main.py <day>
```

Optionally, you can run the example inputs with the following command:

```shell
python3 main.py <day> --use-example
```
