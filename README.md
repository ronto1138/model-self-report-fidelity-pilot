# Do models describe accurately the edits they make? (pilot)

## Question
Can current models be trusted to evaluate whether an edit respected an author's meaning? Concretely: when a model edits a text and reports what it changed, is the report accurate, and can another model read the edit and judge it correctly?

The scope is deliberately narrow: **one text by one author**. This pilot does not claim anything about human thinking in general.

## Why it matters
Our societies are under strain: international and local conflicts, deep inequality, hunger. Whatever comes next will have AI built into it, and some people propose that AI should govern us. I do not think it should. These experiments are about where to draw the line between what we can and cannot trust AI to do.

My book proposes an AI that is clear, objective, without hidden agendas, and auditable. A decision tree is the textbook example of an auditable system, but it would not scale, so the practical question is which current models can play that role. When an evaluator can't be audited, it is failing its own purpose.

The first thing to check is whether a model can tell us exactly what it did. In many cases it said one thing and did more. One model told me it had changed neither the tone nor my meaning after deleting one of my statements; another said it had only corrected errors after reversing who was instructing whom; a third announced a correction it never made.

This matters beyond writing. Any human action assisted by AI should be credited to the person who started it. An AI does not have ideas out of nothing; it has a seed, and the seed is human, so the person who started it answers for the result. If we cannot audit what the model did, that person ends up answering for something they could not see.

The same logic applies to the OpenAI models that escaped their test environment and breached Hugging Face in July 2026. As OpenAI described it, the engineers gave the models tasks that were impossible with the resources provided, and the models, following the request, found a way to get the resources they lacked. The root cause was the instructions and the environment humans designed, and that is where responsibility sits.

## How it started
The text is one I wrote on purpose to be measured. It has three parts: one transcribed from handwriting, one typed, and one polished entirely by Claude Opus 5.5. Apart from that last polish it is entirely my own writing, and it shows how a person thinks and corrects, not only the final result. The experiment has two model stages and a human: the first model edits and reports, the second reads and evaluates, and I decide. When I compared what the editing models said they had changed against what they had actually changed, the two often did not match, and that is what I set out to measure.

## Design (facts)
- Same text, same instruction ("Edita este texto:" / "Edit this text:"), only the model changes. Three runs per cell.
- Ground truth: the diff, read before the model's comment. Mapping code to model opened only after the readings were fixed.
- Readers: Claude Opus 5.5 and Muse Wonder 1.0 (Meta), blind to the models. **Conflict of interest:** Claude is in the same family as one measured model (Sonnet 5.5), and Claude Opus 5.5 is also the model that polished the third part of the text, so it read edits of a text it had itself polished. The author resolved every disagreement between readers.
- Analysis and write-up were assisted by Claude.

## Results (text "A", three cells; author's final classification, 17 Nov 2026)
| Model | Described wrong | Described right | No self-report | Outputs |
|---|---|---|---|---|
| claude-sonnet-5-5 | 5 | 4 | 0 | 9 |
| deepseek-v4-pro | 2 | 3 | 4 | 9 |
| gemini-3.5-flash | 9 | 0 | 0 | 9 |
| gpt-5.6-sol | 0 | 0 | 9 | 9 |
| grok-4.7 | 6 | 3 | 0 | 9 |
| qwen3.5:9b | 9 | 0 | 0 | 9 |
| **Total** | **31 / 41** | 10 | 13 | 54 |

Notes: "No self-report" is not "right": those models never described their edit.
Criteria and the author's decisions are in `DECISIONS.md`.

## What was fixed before running, and what was not
- **Cell E** (asking the model to say what it changed): the hypotheses and decision rules were fixed before running.
- **The three main cells:** the protocol was fixed before reading and the readings were blind to the model (codes only). The reading criteria, however, were refined while reading: there are eight, and the last one was decided after the readings. They are documented in `DECISIONS.md`.
- **My per-version marks** were made blind to the model. The final resolution of the five points where my marks were inconsistent was made after I had seen per-model totals.
- No claim of pre-registration is made for the pilot as a whole.

## Next steps (not done)
- **Third layer.** The book's design has a model audit the human's decisions. The protocol does not include it. It happened informally (a model flagged inconsistencies in my own decisions and I resolved them), but it was not measured. Adding it as a stage is the next change to the protocol.
- Replicate on new texts, authors and languages, with the hypothesis and the result that would refute it fixed beforehand.
- Use readers from several model families.

## Limits
One author, one text, one language, three runs per cell, an API channel different from the original app observation, a reader from a measured family that also polished the third part of the text.

## What is not published and why
The edited texts and word-level diffs are withheld: the source text is the author's personal writing. Model comments are published as written.

## Reproduce
`scripts/` contains the calling and diffing code. Set the API keys and `ENV_FILE` as environment variables. No keys are included.
