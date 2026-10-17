# BN Lab — Solutions and Results

This solution follows `BN_lab.pdf`: it uses the six-sentence dataset from the handout, treats words as tokens, adds `<START>` and `<END>`, implements first- and second-order models using ordinary Python data structures, checks probability normalisation, generates text, and compares the models. Run the scripts and tests yourself before submitting. Edit the LLM reflection so it accurately describes your own process.

## Question 1 — Why is the chain-rule decomposition useful for generating text?

The chain rule writes the probability of a complete sequence as a product of conditional probabilities:
\[
P(x_1,\ldots,x_T)=\prod_{t=1}^{T}P(x_t\mid x_1,\ldots,x_{t-1}).
\]
This lets a model generate a sequence one token at a time. It first chooses a token, then predicts the next token conditioned on the previous context, and repeats until it produces `<END>`.

## Question 2 — What independence assumption does a first-order chain network make?

The first-order Markov assumption is
\[
P(X_t\mid X_1,\ldots,X_{t-1})=P(X_t\mid X_{t-1})
\]
for \(t\ge 2\). Given the immediately previous token, earlier tokens do not provide additional information in this model. Its joint distribution factors as
\[
P(X_1,\ldots,X_T)=P(X_1)\prod_{t=2}^{T}P(X_t\mid X_{t-1}).
\]

## Question 3 — Construct the conditional distributions

Using the handout's six sentences and counting adjacent word transitions (with `<START>` and `<END>` included in the implementation):

- After `the`: `cat` occurs 3 times and `dog` 2 times, so \(P(cat\mid the)=3/5=0.6\), \(P(dog\mid the)=2/5=0.4\).
- After `cat`: `sat` occurs twice and `ran` once, so \(P(sat\mid cat)=2/3\), \(P(ran\mid cat)=1/3\).
- After `dog`: `sat` occurs twice and `ran` once, so \(P(sat\mid dog)=2/3\), \(P(ran\mid dog)=1/3\).
- After `sat`: `on` occurs 3 times, so \(P(on\mid sat)=1\).
- After `ran`: `to` occurs twice, so \(P(to\mid ran)=1\).

Transitions not observed in the data have probability zero under this unsmoothed model. For example, `the → sat` and `cat → dog` have probability zero. These are empirical zeros, not proof that such word sequences are impossible in English.

## Questions 4–7 — Inspect the first-order implementation

**Q4. Where are transition counts stored?**  
In `FirstOrderLM.counts`, a dictionary-like structure maps each current token to a `Counter` of the next tokens observed after it.

**Q5. Where is \(P(X_t\mid X_{t-1})\) computed?**  
During `FirstOrderLM.__init__`, each next-token count is divided by the sum of all outgoing counts for the current token. This is maximum-likelihood estimation from transition frequencies.

**Q6. Greedy choice versus sampling:**  
`predict_greedy` chooses the most probable next token (with a deterministic tie-break). `sample_next` samples a token according to the conditional probabilities. Greedy generation is repeatable and can become repetitive; sampling can produce different valid continuations.

**Q7. What if a word has no observed outgoing transition?**  
The distribution is empty and the implementation returns `None`, causing generation to stop. In this dataset, `<END>` is a token with no outgoing transition and generation should stop before attempting another token. An unknown context also has no distribution; the model does not use smoothing or backoff.

## Question 8 — What does a probability total of 0.87 indicate?

For a context with observed outgoing transitions, the conditional probabilities should sum to 1. A total of 0.87 indicates an implementation or normalisation error, such as dividing counts by the wrong denominator or accidentally omitting possible next tokens. Small floating-point rounding differences are acceptable; a discrepancy of 0.13 is not.

## Question 9 — Do greedy predictions always match human expectations?

No. The model only learns transitions present in the tiny training dataset. For example, after `the`, `cat` is more likely than `dog` in this dataset because it occurs more often after `the`. This reflects training frequency rather than a complete model of language or human expectations.

## Question 10 — Greedy versus sampling

Greedy generation always selects the maximum-probability next token (using a fixed tie-break), so it tends to repeat the same sequence for the same start and model. Sampling draws from the conditional distribution, so different sentences can be generated. Sampling usually produces more variation, although the small dataset limits what either method can generate.

## Question 11 — First-order versus second-order

1. **Graph:** first-order has edges from \(X_{t-1}\) to \(X_t\); second-order has both \(X_{t-2}\to X_t\) and \(X_{t-1}\to X_t\).
2. **CPT:** first-order estimates \(P(X_t\mid X_{t-1})\); second-order estimates \(P(X_t\mid X_{t-2},X_{t-1})\).
3. **Context:** second-order uses the previous two tokens, so it can distinguish contexts sharing the same final word.
4. **Data:** second-order needs more data because there are more distinct contexts and many may occur rarely or not at all.

## Question 12 — Why can more context help and hurt?

More context can improve prediction because it distinguishes situations that a shorter context merges. But each additional context creates more conditional distributions to estimate. With limited training data, many contexts have few observations or none, producing unreliable estimates and zero-probability contexts. Thus a larger CPT can represent more detail but requires more data.

## Question 13 — Why is a precise LLM prompt preferable?

A precise prompt specifies the intended variables, representation, probability distribution, and observable behaviour. This makes the generated code easier to inspect against the model. The implementation must still be validated with test cases and probability invariants such as each observed context's conditional probabilities summing to one. A program that runs is not necessarily implementing the intended probabilistic model.

## Question 14 — What did thinking of the model as a Bayesian network add?

It made the dependencies between consecutive tokens explicit; provided a factorisation of the joint sequence probability into conditional probabilities; clarified the independence assumption of a first-order model; and gave a principled way to predict and generate the next token. It also made model limitations testable: conditional distributions should normalise, and unseen transitions have zero probability in the unsmoothed count model.

## Part XIII — Comparing first- and second-order models

Use the output from `first_order.py` and `second_order.py` to report examples from your run.

| Comparison | First-order | Second-order |
|---|---|---|
| Context | One previous token | Two previous tokens |
| Stored contexts | Distinct current tokens with outgoing transitions | Distinct token pairs with outgoing transitions |
| Conditional table | \(P(next\mid current)\) | \(P(next\mid previous,current)\) |
| Unseen context | Empty distribution | Empty pair-context distribution |
| Expected variation | Sampling can vary within observed transitions | Sampling can vary within observed pair-context transitions |
| Data requirement | Lower | Higher |

**Parameter-count convention:** the scripts report only observed transitions and do not store a dense table containing all possible vocabulary combinations. For a fair count, state your convention. One useful measure is the number of distinct observed contexts (`len(model.probabilities)`), alongside the number of distinct observed context-to-next-token entries (`sum(len(d) for d in model.probabilities.values())`). A dense theoretical table would have a much larger size and many zero entries.

## Reflection on LLM use

Use this as a structure, but personalise it to what you actually did:

1. **Specification:** I described a first-order model whose transition probabilities are estimated from adjacent-token counts.
2. **Inspection:** I checked where counts are stored, where normalisation occurs, how greedy prediction differs from sampling, and how unknown contexts are handled.
3. **Testing:** I checked that all observed-context probability totals are approximately 1, tested known transition probabilities, checked an unseen transition, and ran generation.
4. **Correction/validation example:** The code explicitly returns an empty distribution for an unknown context rather than silently inventing a next token. I verified this behaviour with a unit test. Replace this example if you inspect or correct a different part.
5. **Limitation:** The six-sentence dataset is tiny. The model memorises observed local transitions and cannot represent the full complexity of natural language.

## Deliverables checklist

- [x] First-order implementation: `first_order.py`
- [x] Second-order implementation: `second_order.py`
- [x] Conditional probability tables: printed by the scripts
- [x] Generated text examples: printed by the scripts
- [x] Probability-normalisation tests: `test_bn_models.py`
- [x] Answers to Questions 1–14: this file
- [x] LLM-use reflection structure: this file; personalise before submission
