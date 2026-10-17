"""First-order autoregressive language model using transition counts only."""
from __future__ import annotations
from collections import Counter, defaultdict
import random

START = "<START>"
END = "<END>"

TRAINING_SENTENCES = [
    "the cat sat on the mat",
    "the cat sat on the rug",
    "the dog sat on the mat",
    "the dog ran to the park",
    "the cat ran to the park",
    "the dog sat on the rug",
]


def tokenise_sentences(sentences):
    """Lowercase and add explicit START/END tokens."""
    return [[START, *sentence.lower().split(), END] for sentence in sentences]


class FirstOrderLM:
    def __init__(self, tokenised_sentences):
        self.counts = defaultdict(Counter)
        for sentence in tokenised_sentences:
            for current, nxt in zip(sentence, sentence[1:]):
                self.counts[current][nxt] += 1
        self.probabilities = {
            current: {nxt: count / sum(next_counts.values())
                      for nxt, count in next_counts.items()}
            for current, next_counts in self.counts.items()
        }

    def distribution(self, current):
        """Return P(next token | current token); empty if unseen context."""
        return dict(self.probabilities.get(current, {}))

    def predict_greedy(self, current):
        dist = self.distribution(current)
        if not dist:
            return None
        # Stable tie-break: alphabetically smallest token among tied maxima.
        return sorted(dist, key=lambda token: (-dist[token], token))[0]

    def sample_next(self, current, rng=None):
        dist = self.distribution(current)
        if not dist:
            return None
        rng = rng or random
        tokens = list(dist)
        weights = [dist[token] for token in tokens]
        return rng.choices(tokens, weights=weights, k=1)[0]

    def generate(self, mode="sample", max_tokens=30, rng=None):
        if mode not in {"sample", "greedy"}:
            raise ValueError("mode must be 'sample' or 'greedy'")
        rng = rng or random
        current = START
        output = []
        for _ in range(max_tokens):
            nxt = self.sample_next(current, rng) if mode == "sample" else self.predict_greedy(current)
            if nxt is None:
                break
            if nxt == END:
                break
            output.append(nxt)
            current = nxt
        return " ".join(output)

    def probability_totals(self):
        return {current: sum(dist.values()) for current, dist in self.probabilities.items()}


def main():
    model = FirstOrderLM(tokenise_sentences(TRAINING_SENTENCES))
    print("FIRST-ORDER MODEL")
    print("Training sentences:", len(TRAINING_SENTENCES))
    print("\nConditional distributions:")
    for word in ["the", "cat", "dog", "sat", "ran"]:
        print(f"P(next | {word}) = {model.distribution(word)}")
    print("\nGreedy predictions:")
    for word in ["the", "cat", "dog", "sat", "ran"]:
        print(f"{word} -> {model.predict_greedy(word)}")
    print("\nProbability normalisation:")
    for word, total in sorted(model.probability_totals().items()):
        print(f"{word}: {total:.6f}")
    print("\n20 sampled sentences:")
    rng = random.Random(7)
    for i in range(20):
        print(f"{i+1:02d}. {model.generate('sample', rng=rng)}")
    print("\n5 greedy sentences:")
    for i in range(5):
        print(f"{i+1:02d}. {model.generate('greedy')}")
    print("\n5 sampled sentences for comparison:")
    rng = random.Random(21)
    for i in range(5):
        print(f"{i+1:02d}. {model.generate('sample', rng=rng)}")


if __name__ == "__main__":
    main()
