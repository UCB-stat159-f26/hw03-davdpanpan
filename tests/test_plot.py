"""Tests for tenniscareer.plot. None of them contact tennisabstract.com."""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import pandas as pd

from tenniscareer.data import clean_career
from tenniscareer.plot import plot_career

MALE_JS = (Path(__file__).parent / "data" / "MalePlayerCareer.js").read_text()
MATCHES = clean_career(MALE_JS, pd.Timestamp("1986-06-03"), "Rafael Nadal")  # 2 losses, 1 win


def test_plot_returns_a_figure():
    fig = plot_career(MATCHES)
    assert isinstance(fig, matplotlib.figure.Figure)


def test_title_has_player_name():
    ax = plot_career(MATCHES).axes[0]
    assert "Rafael Nadal" in ax.get_title()


def test_one_point_per_match():
    lost, won = plot_career(MATCHES).axes[0].collections
    assert len(lost.get_offsets()) == 2
    assert len(won.get_offsets()) == 1


def test_legend_labels():
    ax = plot_career(MATCHES).axes[0]
    labels = [text.get_text() for text in ax.get_legend().get_texts()]
    assert labels == ["Match lost", "Match won"]
