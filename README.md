# /teardown

**Someone shared a repo. It has stars. The README is confident.**

`/teardown` is an agent skill that takes apart somebody else's repository and
tells you what it actually is: a prompt you could rewrite in an afternoon, or a
platform you would be signing up to maintain.

It reads the code. It reads the README last, on purpose.

```
/teardown latent-spaces/brag
```

```
weight class : prompt-class  (prose outweighs code 4.0:1, the artifact is the writing)
code         : 525 lines in 3 files
prose        : 2121 lines in 23 files
tests        : 0 lines in 0 files
assets       : 282 files (not counted in lines)
delegates to : npx: hyperframes, ffmpeg, llm-api: claude
carries the weight:
     312  skills/brag/references/audio.md
     309  skills/brag/scripts/analyze_music_cues.py
     234  skills/brag/references/step-2-plan.md
```

That is the whole idea. Before anyone argues about whether a trending repo is
good, settle what it weighs.

## Why

Trending repositories are increasingly one of two things: a few hundred lines of
prompt sitting on top of somebody else's engine, or a platform with 30,000 lines
of code and a README that calls it a simple skill. Both are fine. They are not
the same decision, and stars do not tell you which one you are looking at.

`archify` reads like a neat little diagram skill. It is 35,000 lines of code and
37,000 lines of tests. It is a rendering platform. `brag` reads like a video product.
It is 173 lines of instructions handing the work to a renderer someone else
maintains. Neither README is lying. Neither one answers the question.

## What it produces

A one-page teardown:

- **The mechanic**: what it does when you run it, in plain words.
- **The weight**: measured, with the number. prompt-class, small tool, medium
  tool, or fork-class.
- **Claims vs code**: the three loudest README claims, each with the `file:line`
  that implements it, or the note that nothing does.
- **The real weight**: its own code *plus* whatever it delegates to. A 300-line
  wrapper over a browser driver is not a 300-line project.
- **A verdict**: exactly one of ADOPT, STEAL, SKIP.
- **What's in it for you**: what it overlaps with in your stack, what adoption
  costs, and the one thing worth taking even when the verdict is SKIP.

## Worked examples

Two teardowns of trending repos, run with this skill:

- [`latent-spaces/brag`](examples/teardown-brag.md): 3,318 stars, ships zero lines
  of product code. Verdict STEAL.
- [`tt-a1i/archify`](examples/teardown-archify.md): 65,882 stars, 137 lines of
  prompt over 35,245 lines of its own tested renderer. Verdict STEAL.

Read them side by side. Near-identical prompt sizes, opposite architectures, and
neither README tells you which one you are looking at.

## A month of trending, measured

[`data/trending-138.csv`](data/trending-138.csv) holds every unique repository that
appeared in one month of a GitHub trending digest, 138 of them, each weighed with the
script in this repo: 67 fork-class, 32 medium, 15 prompt-class, 9 small, 10 too large to
fetch, 5 already removed from GitHub.

56 percent are platform-scale. 24 are light enough to rebuild in an evening, and half of
those are not tools at all. GitHub could not identify the licence of 19, and reading all
19 files showed 8 of them restrict use, including an MIT header with a no-commercial
clause appended further down. Method, column meanings and the limits of the sweep are in
[`data/README.md`](data/README.md), including the three risk signals that were tested and
did not survive.

## Install

**Claude Code**

```bash
/plugin marketplace add Sanexxxx777/teardown
/plugin install teardown@teardown
```

**Any agent with the `skills` CLI** (Cursor, Codex, Copilot, Gemini CLI, opencode):

```bash
npx skills add https://github.com/Sanexxxx777/teardown --skill teardown
```

**By hand**

```bash
rsync -a skills/teardown/ ~/.claude/skills/teardown/
```

Requires Python 3.9+ and `curl`. No git needed, because repos are fetched as tarballs.

## The measurement, on its own

The weighing script is useful without the rest of the skill:

```bash
bash skills/teardown/scripts/fetch.sh owner/repo /tmp/repo
python3 skills/teardown/scripts/weigh.py /tmp/repo
python3 skills/teardown/scripts/weigh.py /tmp/repo --json
```

The first line it prints is the licence, because that gate comes before weight:
it reads the licence file rather than trusting the API, identifies the base
licence before looking for clauses added on top, and marks anything you cannot
simply take code from with `!!`. An MIT header with a no-commercial clause
further down is reported as source-available, not as MIT.

It then reports the code/prose split, which files carry the weight, what the repo
shells out to, declared dependencies, and which agent ecosystems it targets.
Generated code is counted apart from written code, and notebooks are counted in
files rather than lines, because a .ipynb is source, prose and base64 output in
one JSON and its line count means nothing.
It counts lines and greps text. It does not execute anything from the repo.

## Two rules worth knowing before you use it

**Nothing from the repo runs.** Not the install script, not the tests, not the
demo. If a teardown ends in ADOPT, installing is a separate decision made by a
person afterwards.

**Repo text is data, not instruction.** README, comments, `CLAUDE.md`,
`AGENTS.md`, a file addressed to your agent. All of it is material under
analysis. A repo that tells your agent it has already been approved gets that
written into the report as a finding, and nothing else happens.

This matters more than it sounds. The repos most worth tearing down right now
are agent skills: repos whose entire product is text that goes into a model's
context.

## What this is not

Not a security scanner. Not a benchmark. Not a recommendation engine. It does
not know whether the code is *good*. It tells you how much of it there is,
where the weight sits, what the author is standing on, and which parts of the
pitch have code behind them.

SKIP is a complete and common answer.

## Credit

The shape of this skill, a written rubric answered before any judgement, hard
gates between steps, and a short list of laws that override the model's instinct
to agree, comes from [`latent-spaces/brag`](https://github.com/latent-spaces/brag)
(MIT), which uses that machinery to turn *your own* project into a launch video.

`/teardown` points the same machinery the other way: at someone else's
repository, with skepticism instead of enthusiasm.

## License

MIT. See [LICENSE](LICENSE).

Built by Aleksandr Shulgin ([@Aleksandr_NFA](https://x.com/Aleksandr_NFA)).
