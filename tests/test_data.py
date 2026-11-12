"""Tests for tenniscareer.data. None of them contact tennisabstract.com."""

from pathlib import Path

import pandas as pd
import pytest

from tenniscareer import data

FEMALE_JS = (Path(__file__).parent / "data" / "FemalePlayerCareer.js").read_text()
MALE_JS = (Path(__file__).parent / "data" / "MalePlayerCareer.js").read_text()


class FakeResponse:
    """Stands in for the response that requests.get returns."""

    def __init__(self, text, status_code=200):
        self.text = text
        self.status_code = status_code

    def raise_for_status(self):
        pass


def fake_get(url, **kwargs):
    """Stands in for requests.get: only Serena Williams exists."""
    if url.endswith("SerenaWilliamsCareer.js"):
        return FakeResponse(FEMALE_JS)
    if url.endswith("p=SerenaWilliams"):
        return FakeResponse("var fullname = 'Serena Williams'; var dob = 19810926;")
    return FakeResponse("Not Found", status_code=404)


def test_female_opponent_age_comes_from_date_of_birth():
    matches = data.clean_career(FEMALE_JS, pd.Timestamp("1981-09-26"), "Serena Williams")
    assert matches["opponent_age"][0] == pytest.approx(18.789, abs=0.001)


def test_male_opponent_age_is_read_from_file():
    matches = data.clean_career(MALE_JS, pd.Timestamp("1986-06-03"), "Rafael Nadal")
    assert matches["opponent_age"].tolist() == pytest.approx([22.264, 24.290, 18.760], abs=0.001)


def test_player_age_and_age_diff():
    matches = data.clean_career(FEMALE_JS, pd.Timestamp("1981-09-26"), "Serena Williams")
    assert matches["player_age"][0] == pytest.approx(14.101, abs=0.001)
    assert matches["age_diff"][0] == pytest.approx(-4.688, abs=0.001)


def test_get_career_accepts_different_name_formats(monkeypatch):
    monkeypatch.setattr(data.requests, "get", fake_get)
    for name in ["serena williams", "Serena Williams", "SerenaWilliams"]:
        assert len(data.get_career(name)) == 3


def test_get_career_invalid_player_raises_value_error(monkeypatch):
    monkeypatch.setattr(data.requests, "get", fake_get)
    with pytest.raises(ValueError):
        data.get_career("GastonSanchez")
