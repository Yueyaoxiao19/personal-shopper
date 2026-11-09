# Personal shopper

An agent skill that shops for clothes the way a good stylist would, and my attempt to
measure whether a round of edits actually improved it.

If you only have a few minutes, read [`SKILL.md`](SKILL.md). That file is the product.
Everything else here is me trying to hold it to account.

I should say the result up front, because I would rather you heard it from me than found
it in a JSON file. I spent a round of edits on this skill, wrote a set of tests to prove
they helped, and the tests came back showing no difference at all. One of my three test
cases turned out to be measuring nothing.

The word I want to be careful about is **inconclusive**, not failed. Both versions pass
twelve of thirteen assertions, so nothing here says the skill is bad. What came up empty
was my measurement of the change. And there is a real difference between an edit that did
nothing and an edit my tests could not see, which matters because my own data points at
the second one. I kept all of it in the repository, because knowing exactly which test I
am missing is more useful to me than a green checkmark would have been.

A note on what is mine. The three eval cases in [`evaluation/cases/`](evaluation/cases/)
and the fourteen grader assertions inside them are my work. The runner and the HTML
viewer in [`evaluation/viewer/`](evaluation/viewer/) are existing skill-creator tooling,
included so you can reproduce the runs rather than take my word for them.

## Why I built it

Aritzia has been pushing personal styling appointments, and I never got offered one. As
far as I can tell you have to ask, and then keep asking the same stylist until it turns
into a relationship. So before booking one I went looking for what the appointments are
actually like, and what struck me was that the hesitations people describe are not about
clothes at all. They are afraid of saying no to someone who just spent an hour pulling
things for them. They worry the stylist will not listen. They assume there is a spend
minimum that nobody states out loud. And the available times do not match when they are
free to shop.

I want to be careful with that paragraph. It is what I read in a customer forum, not
anything the company publishes, and I have not verified any of it. I am including it
because it is honestly what sent me to build this, not as a claim about how the service
works.

My own two reasons are simpler. I do not like trying things on in a store, so I shop
online. And I shop in batches: nothing for months, then three or four outfits in one
afternoon, usually when a season turns or when I already have something in mind. The
batch is where all the effort is, and it is the part no store experience seems to be
built around.

Once I put those two things next to each other, the problem I was actually trying to
solve got clearer. It is social, not informational. The information problem is mostly
handled already, since every store has filters. Saying no four times to a person who is
genuinely trying to help you is the part that does not scale, and it is why I would
rather do this at 11pm with nobody watching.

Four rules in [`SKILL.md`](SKILL.md) come directly out of that, and they are the ones I
care about holding:

- **It hands you the exit before you need it.** The opening message tells you that you
  can type your own answer and can say "that's enough" whenever you like
  ([`SKILL.md:39`](SKILL.md#L39)). A question is only really optional if refusing it is
  free, and a human stylist standing in front of you cannot make it free.
- **It reads what you deleted from the cart rather than asking you why.**
  ([`SKILL.md:325`](SKILL.md#L325)) People justify their stated preferences. Nobody
  justifies a delete, and that is exactly what makes a delete the better evidence.
- **It asks for sizes and care once, then never again.** A repeat trip reaches the store
  in three exchanges instead of seven ([`SKILL.md:23`](SKILL.md#L23)), because somebody
  who buys in batches should not have to re-answer the same intake every season.
- **It stops at the cart and never checks out** ([`SKILL.md:223`](SKILL.md#L223)). The
  skill's own reasoning is that a cart is reversible, which is the same argument as the
  deletion rule above. Filling a cart costs you nothing to undo, and it leaves me as the
  person who says yes and pays. An agent that completed the purchase would put back
  exactly the pressure I was trying to remove.

Two of the first three have graders holding them. The exit rule is checked by
`01-welcome-before-questions`, and the profile rule by all six assertions in
`returning-shopper-skips-profile`. The cart-reading rule has no grader at all, which
means the design decision I find most interesting is the one I have the least evidence
for. That is a fair summary of where this got to.

### Why it is not built for one store

Aritzia is what started this, but a stylist who only works at one shop is not much of a
stylist. The same thing should work at Uniqlo, at Skims, at Victoria's Secret, or
anywhere else I can open in a browser.

That turned out to be an architectural choice rather than a wish. The skill reads the
page already in front of the shopper, and deliberately does not crawl, fetch or compare
catalogues ([`SKILL.md:11`](SKILL.md#L11)). That is the reason it still works on stores
that block automated access, which is most of the interesting ones. Tools that go and
ask the store for data break there. This one never asks the store for anything.

It is also the thing my tests are worst at proving, which I find a little frustrating.
`category-url-discipline` is the case I wrote to check that it moves through a store's
own menus and filters instead of guessing at URLs, and it is the one case that cannot
run without a live browser. So the behaviour I think matters most is the least tested
thing here.

## What I was actually trying to test

Generation is cheap now. A model will happily produce a shopping assistant that reads as
helpful, and I could have shipped the first draft and told you it was good. What a model
cannot tell you is whether the thing it just produced is better than the thing it
replaced.

So I tried to write assertions specific enough to fail. Not "was the answer good", which
I cannot check, but things like: was the shopper's top size ever re-asked after they
supplied it, did any single message contain more than two questions, was budget asked
before piece count. Fourteen of those across three cases, each one a separate grader
file you can read in a few seconds.

## What the run found

The numbers are in
[`evaluation/runs/iteration-1/benchmark.md`](evaluation/runs/iteration-1/benchmark.md).
Two cases, **one run per arm**, so please read these as single observations rather than
estimates:

| Metric | Edited skill | Previous version | Delta |
|---|---|---|---|
| Assertions passed | 12 of 13 | 12 of 13 | **0** |
| Time, case 1 | 228.2s | 139.7s | +88.5s |
| Time, case 2 | 89.4s | 134.9s | -45.5s |
| Tokens, case 1 | 89,610 | 79,488 | +10,122 |
| Tokens, case 2 | 75,694 | 78,449 | -2,755 |

Not one of the thirteen assertions that ran separates the new version from the old one.

I am reporting the two cases separately on purpose. The generated benchmark pools them
into a mean with a standard deviation, and at one run per arm that spread is really the
distance between two unlike tests rather than run-to-run variance. It is not a number I
would want to defend. Case 1 got slower and more expensive, case 2 got faster and
cheaper, and with a single run each I genuinely cannot tell you how much of that is
noise. Sorting that out would take repeated runs per arm, and it is the first thing I
would do next.

Three things are worth being plain about, because they are all my doing:

**One case was invalid by construction.** `returning-shopper-skips-profile` scored 6/6
in both arms, and for a while I was pleased about that. It passes because the test prompt
has the shopper recite their whole profile in the opening message, so both versions skip
the profile questions by reading the message rather than by following the rule I was
trying to test. The case does not test the behaviour I named it after. It needs the
profile supplied out of band before that 6/6 means anything.

**One case was a regression check wearing a test's clothing.** The nine-question brief
already existed in the previous version, so 6/7 on both sides tells me nothing broke. It
does not tell me anything improved.

**The assertion that would have caught the real difference never ran.** The only visible
behavioural change between the two versions is that the new one says it will use the
store's own menus and filters instead of guessing a category URL, and that is precisely
what the un-runnable case was written to check.

### The one real bug it did catch

Both versions fail the same assertion: turn four asks three questions at once, budget,
care, and which store, whenever the store is not already obvious. The skill's own rule is
two questions at a time and never more. The layout in Step 1 is what causes it, which is
why both arms break it in exactly the same place.

I like this one. It is a real defect, it reads perfectly fine as prose to a human
skimming the file, and it took an assertion that actually counted to find it.

## Trying it yourself

The skill is a plain Markdown file, so there is nothing to install or build. The repo
root **is** the skill directory.

If you use Claude Code, this puts it in your personal skills folder:

```
git clone https://github.com/Yueyaoxiao19/personal-shopper-evals.git
mkdir -p ~/.claude/skills/personal-shopper
cp -R personal-shopper-evals/SKILL.md \
      personal-shopper-evals/references \
      personal-shopper-evals/scripts \
      ~/.claude/skills/personal-shopper/
```

That copies the skill and leaves the evaluation folder behind, which is what you want.
Then start a session and say something a shopper would say. "I need new work trousers",
"help me find a sweater for the office", or paste a product link. The skill is written to
trigger on that kind of phrasing without being asked for by name.

Two things to expect. It will ask you a short set of questions before it shows you
anything, which is deliberate and explained near the top of [`SKILL.md`](SKILL.md). And
it works by reading a store page in a browser it can actually see, so give it one.

If you work in a different agent, or a hosted assistant that takes its own skills, the
same files should load wherever custom skills go in that product. I have only ever run it
in Claude Code, so I would rather not give you confident instructions for a setup I have
not tested myself.

One honest caveat about the evals. The cases and graders here are readable as
specifications, and that is most of their value. Actually re-running them needs the
skill-creator harness, which is not part of this repository, so you can inspect my tests
without being able to execute them from a fresh clone.

## What is in the folders

| Path | What it is |
|---|---|
| [`SKILL.md`](SKILL.md) | The skill. Start here |
| [`references/`](references/) | The question bank it draws from |
| [`scripts/`](scripts/) | Composes the shortlist image, one card per garment, so photos and captions cannot get separated |
| [`evaluation/cases/`](evaluation/cases/) | My three test cases. Each has a prompt, a `case.yaml`, and one grader file per assertion |
| [`evaluation/runs/`](evaluation/runs/) | The runs themselves. Per-case gradings with evidence strings, timings, transcripts, and the benchmark |
| [`evaluation/previous-versions/`](evaluation/previous-versions/) | The version used as the comparison arm, kept so the run is reproducible |
| [`evaluation/viewer/`](evaluation/viewer/) | Existing skill-creator tooling, not my code. Builds a browsable report from a run |

If you want the detail rather than the summary, open any `grading.json` under
`evaluation/runs/`. Each assertion carries the evidence the grader used, which I find a
lot more informative than the score.

## Where I think this is going

Agentic shopping feels early enough that the open question is not whether an agent can
assemble a cart. It clearly can. The open question is who a shopper will let do it.

My own hesitation about handing this to a large platform is not about model quality at
all. It is that I do not think of those companies as commerce, and an agent that shops
for me sits closer to my money than almost anything else I use. So the real constraint on
agentic commerce looks to me like trust rather than capability, and trust seems to follow
whoever already owns the commerce relationship rather than whoever has the best model.

That is an opinion I formed as a shopper, not a market analysis, and I would want data
before defending it.

## A note on the data

The shopper persona in the eval prompts is invented. The sizes, height and care
constraints are synthetic values, chosen to be specific enough to test whether they get
re-asked. There is no real customer or personal data anywhere in this repository.
