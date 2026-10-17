"""Second-order autoregressive language model P(X_t | X_{t-2}, X_{t-1})."""
from __future__ import annotations
from collections import Counter, defaultdict
import random
from first_order import START, END, TRAINING_SENTENCES, tokenise_sentences


class SecondOrderLM:
    def __init__(self, tokenised_sentences):
        self.counts = defaultdict(Counter)
        for sentence in tokenised_sentences:
            # Add a second START context so the first generated word has two-token context.
            padded = [START, START, *sentence[1:]]
            for first, second, nxt in zip(padded, padded[1:], padded[2:]):
                self.counts[(first, second)][nxt] += 1
        self.probabilities = {
            context: {nxt: count / sum(next_counts.values())
                      for nxt, count in next_counts.items()}
            for context, next_counts in self.counts.items()
        }

    def distribution(self, context):
        return dict(self.probabilities.get(tuple(context), {}))

    def predict_greedy(self, context):
        dist = self.distribution(context)
        if not dist:
            return None
        return sorted(dist, key=lambda token: (-dist[token], token))[0]

    def sample_next(self, context, rng=None):
        dist = self.distribution(context)
        if not dist:
            return None
        rng = rng or random
        tokens = list(dist)
        return rng.choices(tokens, weights=[dist[t] for t in tokens], k=1)[0]

    def generate(self, mode="sample", max_tokens=30, rng=None):
        if mode not in {"sample", "greedy"}:
            raise ValueError("mode must be 'sample' or 'greedy'")
        rng = rng or random
        first, second = START, START
        output = []
        for _ in range(max_tokens):
            context = (first, second)
            nxt = self.sample_next(context, rng) if mode == "sample" else self.predict_greedy(context)
            if nxt is None or nxt == END:
                break
            output.append(nxt)
            first, second = second, nxt
        return " ".join(output)

    def probability_totals(self):
        return {context: sum(dist.values()) for context, dist in self.probabilities.items()}


def main():
    model = SecondOrderLM(tokenise_sentences(TRAINING_SENTENCES))
    print("SECOND-ORDER MODEL")
    print("Training sentences:", len(TRAINING_SENTENCES))
    print("\nSelected conditional distributions:")
    for context in [("the", "cat"), ("the", "dog"), ("cat", "sat"),
                    ("dog", "ran"), ("sat", "on")]:
        print(f"P(next | {context}) = {model.distribution(context)}")
    print("\nProbability normalisation:")
    for context, total in sorted(model.probability_totals().items()):
        print(f"{context}: {total:.6f}")
    print("\n10 sampled sentences:")
    rng = random.Random(7)
    for i in range(10):
        print(f"{i+1:02d}. {model.generate('sample', rng=rng)}")
    print("\n5 greedy sentences:")
    for i in range(5):
        print(f"{i+1:02d}. {model.generate('greedy')}")


if __name__ == "__main__":
    main()
