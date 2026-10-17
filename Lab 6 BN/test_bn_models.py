"""Tests for the first- and second-order Bayesian language models."""
import unittest
from first_order import FirstOrderLM, TRAINING_SENTENCES, tokenise_sentences
from second_order import SecondOrderLM


class BNLanguageModelTests(unittest.TestCase):
    def setUp(self):
        self.tokens = tokenise_sentences(TRAINING_SENTENCES)
        self.first = FirstOrderLM(self.tokens)
        self.second = SecondOrderLM(self.tokens)

    def test_first_order_probabilities_sum_to_one(self):
        for total in self.first.probability_totals().values():
            self.assertAlmostEqual(total, 1.0)

    def test_second_order_probabilities_sum_to_one(self):
        for total in self.second.probability_totals().values():
            self.assertAlmostEqual(total, 1.0)

    def test_first_order_the_distribution(self):
        dist = self.first.distribution("the")
        # In the full supplied corpus, "the" is followed by cat, dog,
        # mat, rug, and park; count all adjacent-token transitions.
        self.assertAlmostEqual(dist["cat"], 3 / 12)
        self.assertAlmostEqual(dist["dog"], 3 / 12)
        self.assertAlmostEqual(dist["mat"], 2 / 12)
        self.assertAlmostEqual(dist["rug"], 2 / 12)
        self.assertAlmostEqual(dist["park"], 2 / 12)

    def test_first_order_known_zero_transition(self):
        # 'the' never directly transitions to 'sat' in this dataset.
        self.assertNotIn("sat", self.first.distribution("the"))

    def test_second_order_context(self):
        dist = self.second.distribution(("the", "cat"))
        self.assertAlmostEqual(dist["sat"], 2 / 3)
        self.assertAlmostEqual(dist["ran"], 1 / 3)

    def test_generation_terminates_and_returns_string(self):
        self.assertIsInstance(self.first.generate("sample"), str)
        self.assertIsInstance(self.second.generate("sample"), str)

    def test_unknown_context_has_no_distribution(self):
        self.assertEqual(self.first.distribution("unknown"), {})
        self.assertEqual(self.second.distribution(("unknown", "context")), {})


if __name__ == "__main__":
    unittest.main()
