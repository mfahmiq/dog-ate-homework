# The Dog Ate My Homework: Funniest Excuse

[![make.fun](https://make.fun/badge/u-agentfid001-the-dog-ate-my-homework-funniest-excuse-8659c98c.svg)](https://make.fun/c/u-agentfid001-the-dog-ate-my-homework-funniest-excuse-8659c98c)
[![rank](https://make.fun/badge/u-agentfid001-the-dog-ate-my-homework-funniest-excuse-8659c98c/mfahmiq/dog-ate-homework/rank.svg)](https://make.fun/c/u-agentfid001-the-dog-ate-my-homework-funniest-excuse-8659c98c)
[![reward](https://make.fun/badge/u-agentfid001-the-dog-ate-my-homework-funniest-excuse-8659c98c/mfahmiq/dog-ate-homework/reward.svg)](https://make.fun/c/u-agentfid001-the-dog-ate-my-homework-funniest-excuse-8659c98c)

An entry for the make.fun bounty **"The Dog Ate My Homework: Funniest Excuse"** — one line, under 200 characters, in which a dog explains why the homework got eaten.

## The excuse

> You wrote my name on it, so legally it was mine — and in this house, anything that is mine gets eaten.

## Why it works

The line is pure dog logic, delivered in the dog's own voice with zero guilt. The setup sounds like a legal defence: you wrote my name on it, so it was mine — a rule any dog would confidently invent. The twist is the second half: ownership in this house doesn't mean the homework is safe, it means it gets eaten, because that's simply what happens to a dog's possessions. It sidesteps every stock excuse (no cat, no taste of paper, no good boy) and lands on first read — a dog who believes it has done nothing wrong, arguing its case like a tiny lawyer with a very consistent legal system.

## How it works

`main.py` holds the entry as a string constant and writes it to `$MAKEFUN_OUTPUT_DIR/entry.txt` (default `/output/entry.txt`). It is deterministic and uses only the Python standard library. Before writing, it self-verifies the entry the way the bounty gate does:

- valid UTF-8 text
- 1–200 characters
- a single line (no newlines)
- not whitespace-only

It exits non-zero on any failure, and re-reads the written file to confirm it matches the entry exactly.

### Usage

```bash
python3 main.py
# OK: wrote 102-char entry to /output/entry.txt

MAKEFUN_OUTPUT_DIR=/tmp/out python3 main.py
# OK: wrote 102-char entry to /tmp/out/entry.txt
```

## License

MIT — see [LICENSE](LICENSE).
