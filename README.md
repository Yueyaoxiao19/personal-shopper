# personal-shopper: a skill and the evals that failed to validate it

An agent skill that acts as a personal shopper for clothing, and the eval cases I
wrote to find out whether my edits to it actually made it better.

The short version of the result: they did not. The run found no improvement, cost went
up, and one of my three eval cases turned out to be measuring nothing. That finding is
the reason this repository exists.

The cases and the grader assertions in `skill/evals/` are mine. The runner and the
HTML viewer in `eval-viewer/` are existing skill-creator tooling, included so the runs
reproduce.

## Why I built it

Aritzia has been pushing personal styling appointments, and I never got offered one. As
far as I can tell you have to ask, and then keep asking the same stylist until it turns
into a relationship. So before booking one I went looking for what the appointments are
actually like, and the hesitations people describe are not about clothes at all. They
are afraid of saying no to someone who just spent an hour pulling things for them. They
worry the stylist will not listen. They assume there is a spend minimum that nobody
states out loud. And the available times do not match when they are free to shop.

That last paragraph is what I read in a customer forum, not anything the company
publishes, and I have not verified any of it. I am including it because it is what
actually sent me to build this, not as a claim about how the service works.

My own two reasons are simpler. I do not like trying things on in a store, so I shop
online. And I shop in batches: nothing for months, then three or four outfits in one
afternoon, usually when a season turns or when I already have something in mind. The
batch is where the effort is, and it is the part no store experience is built around.

So the friction I set out to remove is social rather than informational. The information
problem is mostly solved: every store has filters. Saying no four times to a person who
is trying to help you is the part that does not scale, and it is the reason I would
rather do this at 11pm with no one watching.

Three rules in `skill/SKILL.md` exist because of that, and they are the ones I care
about holding:

- **It gives you the exit before you need it.** The opening message tells you that you
  can type your own answer and can say "that's enough" at any point
  ([`SKILL.md:39`](skill/SKILL.md#L39)). A question is only optional if refusing it is
  free, and a human stylist cannot make it free.
- **It reads what you deleted from the cart instead of asking you why.**
  ([`SKILL.md:325`](skill/SKILL.md#L325)) People justify their stated preferences. They
  do not justify a delete, which is what makes a delete better evidence.
- **It asks for sizes and care once and never again.** A repeat trip reaches the store
  in three exchanges instead of seven ([`SKILL.md:23`](skill/SKILL.md#L23)), because
  somebody who buys in batches should not re-answer the same intake every season.
- **It stops at the cart and never checks out** ([`SKILL.md:223`](skill/SKILL.md#L223)).
  This is the same argument as the one above. A cart is reversible, so filling one costs
  the shopper nothing to undo, and I stay the person who says yes and pays. An agent
  that completes the purchase would reintroduce exactly the pressure I was trying to
  get rid of.

Two of the first three are held to graders. The exit rule is checked by
`01-welcome-before-questions`, and the profile rule by all six assertions in
`returning-shopper-skips-profile`. The cart-reading rule has no grader at all, which
means the design decision I find most interesting is the one I have no evidence for.
That gap is the honest summary of where this project got to.

### Why it is not built for one store

Aritzia started this, but a stylist who only works at one shop is not much of a
stylist. The same thing should work at Uniqlo, at Skims, at Victoria's Secret, or
anywhere else I can open in a browser.

That is an architectural choice rather than a wish. The skill reads the page already in
front of the shopper and deliberately does not crawl, fetch or compare catalogues
([`SKILL.md:11`](skill/SKILL.md#L11)), which is the reason it still works on stores
that block automated access. Most shopping tools break on exactly those stores. This
one does not have to, because it never asks the store for anything.

It is also the thing the eval harness is worst at proving. `category-url-discipline`
is the case written to check that it navigates by the store's own menus and filters
instead of guessing at URLs, and it is the case that cannot run without a live browser.
The most important behaviour is the least tested one.

### Where I think this is going

Agentic shopping is early enough that the open question is not whether an agent can
assemble a cart. It can. The open question is who a shopper will let do it.

My own hesitation about handing this task to a large platform is not about model
quality. It is that I do not think of those companies as commerce, and the agent that
shops for me sits closer to my money than almost anything else I use. So the
constraint on agentic commerce looks to me like trust rather than capability, and trust
seems to follow whoever already owns the commerce relationship rather than whoever has
the best model.

That is an opinion formed as a shopper, not a market analysis, and I would want data
before defending it.

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
