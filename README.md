# Personal shopper

An agent skill that shops for clothes like a stylist would, plus the tests I wrote to
check whether my edits to it actually helped.

**Read [`SKILL.md`](SKILL.md) first. That file is the product.**

**The result, up front:** the tests found no difference between my edited version and the
previous one. Both pass 12 of 13 assertions, so nothing says the skill is bad. What came
up empty was my measurement of the change, and the one test that would have caught the
real difference could not run. Inconclusive, not failed. I kept all of it here.

The three test cases in [`evaluation/cases/`](evaluation/cases/) and their 14 grader
assertions are mine. The runner and viewer in
[`evaluation/viewer/`](evaluation/viewer/) are existing skill-creator tooling.

## Why I built it

A Canadian womenswear brand has been promoting styling appointments all over my social
media. The idea is good: someone pulls the clothes for you and saves you working through
the store. However, when I looked into booking one, I read that
[other clients like me had genuine concerns](https://www.reddit.com/r/Aritzia/comments/1st3isn/personal_styling_appointment/),
and I found I did not want to go.

Three reasons, and two of them are just me.

The first is laziness. I like shopping online, but I do not like scrolling. I shop in
batches, and working through entire catalogues is an hour gone with nothing decided.

The second is what the product exists to fix. By the time you are in a fitting room, you
are not refusing the clothes. You are refusing the person who chose them for you. Those
are two different things to turn down. Refusing something they picked out for you feels
like a personal rejection rather than a judgement about the product.

The third is the hardest to admit. Someone has spent an afternoon on you, and the pull
runs towards spending more, not less. Nobody states a number, but you feel one. I do not
like being in that position, and I do not think most people do, which is exactly why it
is hard to say out loud.

So there are two frictions, and the social one is harder. Filters narrow the range, but
you still have to look through what survives them, which is the part a stylist was meant
to take off your hands. What does not scale is saying no four times to someone who is
trying to help. Information was never the bottleneck. Permission to change your mind was.

I cannot prove any of this with numbers. What I have is my own experience, threads of
strangers describing the same thing, and a mechanism that explains why the friction is
social rather than informational. That is enough to justify building it for myself. It is
not enough to claim it is a market. What I would argue is narrower: this is the shape
personalized shopping agents will eventually take. It knows your size and taste across
stores, hands you the exit first, and never makes you feel you owe it a purchase.

## What it does differently

Four rules follow from that, and they are the ones I care about holding:

- **Hands you the exit first.** You are told up front you can type your own answer or say
  "that's enough" ([`SKILL.md:39`](SKILL.md#L39)). A question is only optional if refusing
  it is free, and a person in front of you cannot make it free.
- **Reads what you deleted from the cart instead of asking why**
  ([`SKILL.md:325`](SKILL.md#L325)). People justify stated preferences. Nobody justifies a
  delete, which is what makes it better evidence.
- **Asks sizes and care once, never again.** Repeat trips reach the store in three
  exchanges instead of seven ([`SKILL.md:23`](SKILL.md#L23)).
- **Stops at the cart, never checks out** ([`SKILL.md:223`](SKILL.md#L223)). A cart is
  reversible, so it costs you nothing to undo and I stay the one who says yes and pays.

**It is not tied to one store.** It reads the page in front of you and deliberately does
not crawl or fetch ([`SKILL.md:11`](SKILL.md#L11)), which is why it still works on stores
that block automated access. Uniqlo, Skims, Victoria's Secret, anything I can open.

## What the tests found

Two cases, **one run per arm**, so read these as single observations and not estimates
([`benchmark.md`](evaluation/runs/iteration-1/benchmark.md)):

| Metric | Edited | Previous | Delta |
|---|---|---|---|
| Assertions passed | 12 of 13 | 12 of 13 | **0** |
| Time, case 1 | 228.2s | 139.7s | +88.5s |
| Time, case 2 | 89.4s | 134.9s | -45.5s |
| Tokens, case 1 | 89,610 | 79,488 | +10,122 |
| Tokens, case 2 | 75,694 | 78,449 | -2,755 |

I report the cases separately on purpose. The generated benchmark pools them into a mean
with a standard deviation, which at one run per arm is the gap between two unlike tests
rather than run-to-run variance. Not a number I would defend.

Why it came up empty, all three my own doing:

- **One case was invalid by construction.** `returning-shopper-skips-profile` scored 6/6
  on both arms because the prompt has the shopper recite their whole profile, so both
  versions skip the questions by reading the message rather than following the rule.
- **One case was a regression check.** The nine-question brief already existed, so 6/7 on
  both sides shows nothing broke, not that anything improved.
- **The deciding assertion never ran.** `category-url-discipline` tests the one visible
  change, navigating by the store's own menus instead of guessing URLs, and it needs a
  live browser.

**The one real bug it did catch:** both versions ask three questions in turn four (budget,
care, store) when the store is not obvious, breaking the skill's own two-question rule.
Step 1's layout causes it. It reads fine as prose and took a counting assertion to find.

## Trying it yourself

The repo root is the skill directory. For Claude Code:

```
git clone https://github.com/Yueyaoxiao19/personal-shopper-evals.git
mkdir -p ~/.claude/skills/personal-shopper
cp -R personal-shopper-evals/SKILL.md \
      personal-shopper-evals/references \
      personal-shopper-evals/scripts \
      ~/.claude/skills/personal-shopper/
```

Then say something a shopper would say: "I need new work trousers", or paste a product
link. It triggers without being named. It reads a store page in a browser it can see, so
give it one. I have only run it in Claude Code, so I would not give you confident
instructions for anything else.

## What is here

| Path | What it is |
|---|---|
| [`SKILL.md`](SKILL.md) | The skill. Start here |
| [`references/`](references/) | The question bank |
| [`scripts/`](scripts/) | Builds the shortlist image, one card per garment |
| [`evaluation/cases/`](evaluation/cases/) | My three test cases, one grader file per assertion |
| [`evaluation/runs/`](evaluation/runs/) | Gradings with evidence, timings, transcripts, benchmark |
| [`evaluation/previous-versions/`](evaluation/previous-versions/) | The comparison arm |
| [`evaluation/viewer/`](evaluation/viewer/) | Skill-creator tooling, not my code |

Open any `grading.json` for per-assertion evidence, which is more useful than the score.

## What I cannot claim

- **It works for me, and that is one person.** No users, no data that it scales, and I
  would rather say so than imply otherwise.
- **The rule I find most interesting is the one with no grader.** Nothing tests the
  cart-reading behaviour.
- **Re-running the evals needs the skill-creator harness**, which is not in this repo. You
  can read my tests but not execute them from a clean clone.
- **The eval persona is synthetic.** Sizes, height and care values are invented, chosen to
  be specific enough to test whether they get re-asked. No real personal data is here.

## Where I think this goes

An agent can already assemble a cart. The open question is who a shopper lets do it,
which makes trust the constraint rather than capability, and trust seems to follow
whoever owns the commerce relationship. That is a shopper's opinion, not
analysis, and I would want data before defending it.
