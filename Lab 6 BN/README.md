# Lab 6: Bayesian Networks and Language Models

## Overview
This lab implements first-order and second-order probabilistic language models using plain Python.

## Files
- `first_order.py` — First-order model using \(P(X_t \mid X_{t-1})\), with greedy and sampling-based generation.
- `second_order.py` — Second-order model using \(P(X_t \mid X_{t-2}, X_{t-1})\).
- `test_bn_models.py` — Unit tests for probability normalization, known distributions, unknown contexts, and text generation.
- `lab_answers.md` — Written answers, model comparison, observations, and reflection.

## Requirements
Python 3. No external machine-learning libraries are required.

## Run
Run these commands from this directory:

```bash
python -m unittest -v
python first_order.py
python second_order.py
```

## Dataset
The models use the six sentences supplied in the lab handout. The text is lowercased and sentence boundaries are represented using `<START>` and `<END>` tokens.

## Observations
The first-order model uses only the previous word and may generate repetitive or less coherent sequences. The second-order model uses two previous words, generally preserving more local context. Both models are limited by the small training dataset.
