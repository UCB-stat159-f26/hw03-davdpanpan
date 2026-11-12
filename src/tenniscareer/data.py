"""Download and clean a tennis player's career matches from tennisabstract.com.

The career files are JavaScript arrays.
Each match is a list of strings. Women's files have 27 fields per match and
store the opponent's date of birth (YYYYMMDD) in field 16; men's files have
47 fields and store the opponent's age (in years) in field 16.
"""

import json
import re
import requests
import pandas as pd

BASE_URL = "https://www.tennisabstract.com"
HEADERS = {"User-Agent": "tenniscareer (Python package)"}
TIMEOUT_SECONDS = 30
DAYS_PER_YEAR = 365
FEMALE_ROW_LENGTH = 27

# Position in each match row -> column name
FIELDS = {
    0: "date",
    1: "tournament",
    2: "surface",
    3: "level",
    4: "result",
    8: "round",
    9: "score",
    11: "opponent",
    16: "opponent_info",  # date of birth for women, age for men
}


def get_career(player_name):
    """Return a data frame of a player's career matches.
    player_name can be written as "serena williams", "Serena Williams" or
    "SerenaWilliams". Raises ValueError if tennisabstract.com has no player
    with that name.
    """
    # Standardize the name format used in the URLs
    words = re.split(r"[\s\-]+", player_name.strip())
    name_param = "".join(word[0].upper() + word[1:] for word in words)

    url = f"{BASE_URL}/jsmatches/{name_param}Career.js"
    career = requests.get(url, headers=HEADERS, timeout=TIMEOUT_SECONDS)
    if career.status_code == 404:
        raise ValueError(f"No player named {player_name!r} found on tennisabstract.com. "
                         "Check the spelling and use the full name, e.g. 'Serena Williams'.")
    career.raise_for_status()

    # The player's profile page has their full name and date of birth
    url = f"{BASE_URL}/cgi-bin/player.cgi?p={name_param}"
    profile = requests.get(url, headers=HEADERS, timeout=TIMEOUT_SECONDS).text
    full_name = re.search(r"var fullname = '([^']*)'", profile).group(1)
    player_dob = pd.to_datetime(re.search(r"var dob = (\d{8})", profile).group(1), format="%Y%m%d")
    
    return clean_career(career.text, player_dob, full_name)


def clean_career(js_text, player_dob, player_name):
    """Turn the text of a career JS file into a data frame of matches."""

    rows = json.loads(js_text[js_text.find("[") : js_text.rfind("]") + 1])
    matches = pd.DataFrame([[row[i] for i in FIELDS] for row in rows], columns=list(FIELDS.values()))
    matches["date"] = pd.to_datetime(matches["date"], format="%Y%m%d")

    if len(rows[0]) > FEMALE_ROW_LENGTH:  # men's file: field 16 is the opponent's age
        matches["opponent_age"] = pd.to_numeric(matches["opponent_info"], errors="coerce")
    else:  # women's file: field 16 is the opponent's date of birth
        opponent_dob = pd.to_datetime(matches["opponent_info"], format="%Y%m%d", errors="coerce")
        matches["opponent_age"] = (matches["date"] - opponent_dob).dt.days / DAYS_PER_YEAR

    matches["player_age"] = (matches["date"] - player_dob).dt.days / DAYS_PER_YEAR
    matches["age_diff"] = matches["player_age"] - matches["opponent_age"]
    matches["won"] = matches["result"] == "W"
    matches["player"] = player_name

    return matches.drop(columns="opponent_info").sort_values("date", ignore_index=True)
