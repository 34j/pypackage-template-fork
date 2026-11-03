from cyclopts import App

from ._main import add

app = App()


@app.default
def main(n1: int, n2: int) -> None:
    """Add the arguments and print the result."""
    print(add(n1, n2))
