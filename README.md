# personal-shopper: a skill and the evals that failed to validate it

An agent skill that acts as a personal shopper for clothing, and the eval cases I
wrote to find out whether my edits to it actually made it better.

The cases and the grader assertions in `skill/evals/` are mine. The runner and the
HTML viewer in `eval-viewer/` are existing skill-creator tooling, included so the runs
reproduce.

The short version of the result: they did not. The harness found no improvement, cost
went up, and one of my three eval cases turned out to be measuring nothing. That
finding is the reason this repository exists.

## The claim being tested

Generation is cheap. A model will happily produce a shopping assistant that sounds
helpful. What it cannot tell you is whether the thing it produced is better than the
thing it replaced.

So the skill is only half of this repo. The other half is an attempt to hold it to
assertions specific enough to fail: not "was the answer good" but "was the shopper's
top size ever re-asked after they supplied it", "did any single message contain more
than two questions", "was budget asked before piece count".

Fourteen assertions across three cases, each one a separate grader file you can read.

## What the harness found

From [`iteration-1/benchmark.md`](iteration-1/benchmark.md). Two cases, **one run per
arm**, so these are single observations and not estimates with error bars:

| Metric | Edited skill | Previous version | Delta |
|---|---|---|---|
| Assertions passed | 12 of 13 | 12 of 13 | **0** |
| Time, case 1 | 228.2s | 139.7s | +88.5s |
| Time, case 2 | 89.4s | 134.9s | -45.5s |
| Tokens, case 1 | 89,610 | 79,488 | +10,122 |
| Tokens, case 2 | 75,694 | 78,449 | -2,755 |

Not one of the thirteen assertions that ran separates the new version from the old one.

I am reporting the two cases separately on purpose. The generated benchmark pools them
into a mean with a standard deviation, which at n=1 per arm is a spread between two
unlike tests rather than run-to-run variance, and it is not a number I would defend.
Case 1 got slower and more expensive, case 2 got faster and cheaper, and with one run
each I cannot tell how much of that is noise. Establishing that would take repeated
runs per arm, which is the first thing I would do next.

Three things are worth saying plainly about why:

**One case was invalid by construction.** `returning-shopper-skips-profile` scored 6/6
in both arms. It passed because the test prompt has the shopper recite their whole
profile in the opening message, so both versions skip the profile questions by reading
the message rather than by following the rule I was trying to test. The eval tests
nothing about the behaviour it was named for. It needs the profile supplied out of
band before that 6/6 means anything.

**One case was a regression check, not a test of the change.** The nine-question brief
already existed in the previous version, so 6/7 on both sides shows nothing broke. It
does not show anything improved.

**The assertion that would have caught the real difference never ran.**
`category-url-discipline` needs a live browser. The only visible behavioural change
between the two versions is that the new one says it will use the store's own menu and
filters instead of guessing a category URL, and that is precisely the thing the
un-runnable case was written to check.

## The one real defect it did catch

Both versions fail the same assertion: turn four asks three questions at once (budget,
care, and which store) whenever the store is not already evident. The skill's own rule
is two questions at a time, never more. The layout in Step 1 causes it, which is why
both arms break it identically.

That is a genuine bug found by a cheap assertion, and it is the kind of thing that
reads fine to a human reviewer skimming the prose. It took a grader that counted.

## Reading the repo

| Path | What it is |
|---|---|
| [`skill/`](skill/) | The current skill. `SKILL.md`, the question bank it draws on, and the shortlist image composer |
| [`skill/evals/`](skill/evals/) | The three eval cases. Each has a prompt, a `case.yaml`, and one grader file per assertion |
| [`iteration-1/`](iteration-1/) | The two-arm run. Per-case gradings with evidence, timings, transcripts, and `benchmark.md` |
| [`iteration-2/`](iteration-2/) | A single-arm re-run of the first-trip case after the brief order changed |
| [`skill-snapshot/`](skill-snapshot/) | The version used as the `old_skill` arm, kept so the comparison is reproducible |
| [`prior-version/`](prior-version/) | An intermediate copy saved before a round of edits |
| [`eval-viewer/`](eval-viewer/) | Existing skill-creator tooling, not my code. Generates a browsable HTML report from a run, and `iteration-1/review.html` is its output |

Start with `iteration-1/benchmark.md` for the numbers, then open any
`grading.json` to see per-assertion evidence rather than a score.

## Running it

The graders and cases are plain files, so the harness is readable without running
anything. `iteration-1/review.html` is already generated and opens directly in a
browser.

To regenerate it, pass a run directory as the workspace. The script starts a small
local server and opens the page rather than only writing a file:

```
python3 eval-viewer/generate_review.py iteration-1 --skill-name personal-shopper
```

Python 3.9 or later, stdlib only. The one thing needing a dependency is
`skill/scripts/compose_shortlist.py`, which uses Pillow.

## A note on the data

The shopper persona in the eval prompts is invented. Sizes, height and care
constraints are synthetic values chosen to be specific enough to test whether they get
re-asked. No real customer or personal data is in this repository.
