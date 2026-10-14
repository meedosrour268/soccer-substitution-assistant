# Soccer Substitution Assistant

A Python decision-support project that ranks soccer substitutions using a utility score and explains the recommendation.

## What it demonstrates

- Object-oriented modeling of players and substitutes.
- Comparing every player/substitute pairing.
- Weighted rules for fatigue, performance, yellow cards, injury risk, match timing, and scoreline.
- Human-readable explanations for the highest-scoring option.

## Run

Requires Python 3; no third-party packages are needed.

```bash
python soccer_substitution_ai.py
```

Enter the match minute, score difference (positive means winning), and substitutions remaining. The included lineup is fictional example data.

Example inputs: `75`, `-1`, `3`.

## How it works

The program evaluates each pairing, rewards relevant factors, applies a penalty for a position mismatch, and returns the pairing with the highest utility score. When no substitutions remain, it returns a message instead.

## Limits

This is a rule-based academic prototype, not a trained machine-learning model. The weights are manually chosen; position mismatch is a penalty rather than a hard restriction. The demo uses a fixed lineup and has no live match-data integration. Numeric input is checked, but ranges and empty rosters are not fully validated.

## Background

Created for optional UMBC CMSC 471 coursework. The original program is preserved here; the repository documentation explains its behavior and limitations.
