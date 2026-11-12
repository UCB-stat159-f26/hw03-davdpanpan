# tenniscareer

A Python package that downloads a tennis player's career matches from
[tennisabstract.com](https://www.tennisabstract.com) and plots them in the style of the
New York Times graphic of Serena Williams' career: the player's age on the x-axis, and how
much older or younger they were than each opponent on the y-axis.

## Installation

```bash
pip install git+https://github.com/UCB-stat159-f26/hw03-davdpanpan.git
```

Requires Python 3.9 or newer. `pandas`, `requests` and `matplotlib` are installed automatically.

## Usage

```python
from tenniscareer import get_career, plot_career

# Serena Williams data and plot
serena = get_career("serena williams")
plot_career(serena)

# Rafael Nadal data and plot
rafa = get_career("Rafael Nadal")
plot_career(rafa)

# Save a plot to a file
fig = plot_career(serena)
fig.savefig("serena.png")

# An unknown player raises a ValueError
get_career("GastonSanchez")
# ValueError: No player named 'GastonSanchez' found on tennisabstract.com. ...
```

## Functions

### `get_career(player_name)`

Downloads a player's career matches and returns them as a pandas data frame, one row per match.

The name can be written as `"serena williams"`, `"Serena Williams"` or `"SerenaWilliams"`.
If tennisabstract.com has no player with that name, it raises a `ValueError`.

| Column | Description |
|---|---|
| `date` | Tournament start date |
| `tournament`, `surface`, `level`, `round` | Tournament name, court surface, tournament level and round |
| `result`, `won` | `"W"` or `"L"`, and the same result as `True`/`False` |
| `score` | Match score |
| `opponent` | Opponent's name |
| `opponent_age` | Opponent's age (years) at the match |
| `player_age` | Player's age (years) at the match |
| `age_diff` | `player_age - opponent_age`: positive when the player was older |
| `player` | Player's full name |

### `plot_career(career)`

Takes the data frame returned by `get_career()` and draws a scatter plot of `player_age`
vs. `age_diff`, with wins in blue and losses in purple. Returns the matplotlib figure.

## Running the tests

The tests use the mock career files in `tests/data/`.

```bash
git clone https://github.com/UCB-stat159-f26/hw03-davdpanpan.git
cd hw03-davdpanpan
pip install -e ".[test]"
pytest
```

## Project structure

```
src/tenniscareer/
    __init__.py      # exports get_career and plot_career
    data.py          # download and clean the career data
    plot.py          # draw the plot
tests/
    data/            # mock women's and men's career files
    test_data.py
    test_plot.py
```

## Notes

- Women's career files give each opponent's date of birth, from which their age is
  calculated. Men's files give the opponent's age directly.
- The data is only as current as tennisabstract.com's career files.
