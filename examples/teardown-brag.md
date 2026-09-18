# Teardown: latent-spaces/brag

**Verdict: STEAL.** The structure is excellent and portable. The product itself
is 173 lines of instructions standing on a video renderer somebody else maintains.

Measured 18 Sep 2026 against `HEAD` (last push 17 Aug 2026). MIT, 3318 stars,
repo created 16 Jun 2026.

## What it is

`/brag` is a Claude Code skill that turns the project in your working directory
into a 15-25 second launch video. It reads your `index.html` and `styles.css` to
pull your real headline, your real colours and your real fonts, decides on an
angle and a tone, writes a beat-by-beat storyboard, hands a brief to the
Hyperframes video engine, and renders an MP4 with a poster frame and a share
caption next to it.

It does none of the rendering. It does none of the encoding. It writes a plan
and a brief, and calls `npx hyperframes`.

## Weight

- Class: **prompt-class**, prose outweighs code 4.0 : 1
- Code: 525 lines in 3 files - Prose: 2121 lines in 23 files - Tests: 0
- Assets: 282 files
- Standing on: `npx hyperframes`, `ffmpeg`, Node 22+, a coding agent, and
  optionally Kokoro for narration
- Real weight: a 173-line skill **plus a full TypeScript video renderer** it
  does not own

Those 525 lines of "code" deserve a second look, because none of them are the
product:

| File | Lines | What it is |
|---|---|---|
| `skills/brag/scripts/analyze_music_cues.py` | 309 | optional librosa beat analysis; the skill works without it |
| `scripts/check-docs.mjs` | 101 | a linter for this repo's own documentation |
| `docs/main.js` | ~115 | the launch website |

**The tool ships zero lines of product code.** That is not a criticism. It is
the whole design, and it is the reason the repo is worth reading.

## Claims vs code

| README says | Code says | Where |
|---|---|---|
| "One command, powered by Hyperframes" | accurate, and load-bearing. Every render step is `npx hyperframes` | `references/step-4-deliver.md:7,15,21,31` |
| "music, motion, and share copy included" | share copy: implemented, one caption file | `references/step-4-deliver.md:75-85` |
| "music ... included" | 5 MP3s are bundled, and the repo itself says their licence is unverified | `assets/music/README.md` |
| "The looping video on the launch site was made by `/brag` on this very repo" | unverifiable from the repo | nowhere |

That music line is the honest finding. The repo's own asset README ends with:
"Before publishing or redistributing the skill, verify and document the exact
music license terms alongside these files." The author shipped first and wrote
the warning to themselves. If you adopt this, you inherit that.

The sound effects are cleaner: ~300 files from [Kenney](https://kenney.nl),
CC0, credited in `assets/sfx/sfx-analysis.md`.

## The mechanic worth naming

Three moves, and they transfer to any creative agent task:

1. **A rubric answered in writing before any creating.** Nine specific questions
   the agent must answer from the project's actual files. What is the funniest
   claim on the site, what exact hex is the accent colour, what are the three
   beats of a user actually using the thing. The video physically cannot come
   out generic, because generic answers to those questions are visibly empty.

2. **A clean split of ownership.** The skill owns the story: angle, tone, what to
   show, how long. The engine owns the render: timing, animation mechanics,
   linting, encoding. The file says this out loud, which stops the prompt from
   drifting into micromanaging keyframes.

3. **Gates, not suggestions.** Each step ends in a checkable condition: the plan
   file exists, scene durations sum to 15-25 seconds, `npx hyperframes check`
   returns zero errors. Plus a short list of laws that push against the model's
   instinct to be agreeable: show the real UI, ban "streamline your workflow",
   the first two seconds decide everything.

The measurement is the point: 2121 lines of prose and 0 lines of product code
means the author's real work was *writing down what good looks like* precisely
enough that a model can hit it without supervision.

## What's in it for us

- **Overlaps with:** our own `kadr` video engine, which is the same Hyperframes
  pack ported in-house, plus a CC0 music library, semantic music search, beat
  grid, quantise and verify. The music layer here is weaker than what we already
  run.
- **Cost to adopt:** Node 22, ffmpeg, the Hyperframes CLI, and an asset bundle
  with one unresolved licence question.
- **Worth taking regardless:** the SFX side. ~300 catalogued Kenney sounds with a
  "this moment to that sound family" table and a per-file measurement of
  brightness and listening fatigue. Source them from Kenney directly; no reason
  to copy someone's bundle.
- **Breaks if adopted:** nothing technically. The risk is duplication: a second
  video path next to the one we maintain.

## Verdict

STEAL. Take the rubric-before-creation shape, the ownership split, and the SFX
catalogue with its selection heuristics. Do not install it: we already own the
renderer it delegates to, and the part that is genuinely theirs is the writing,
which is exactly the part you cannot install anyway. You have to rewrite it for
your own work.

---

*Produced with [`/teardown`](https://github.com/Sanexxxx777/teardown). Numbers
from `weigh.py`; nothing in the repo was executed.*
