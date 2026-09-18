# Teardown: tt-a1i/archify

**Verdict: STEAL.** The architecture is the lesson. The tool itself is a platform,
and you should only install a platform you intend to use weekly.

Measured 18 Sep 2026 against `HEAD` (last push 17 Sep 2026). MIT, 65,882 stars,
repo created 15 Apr 2026.

## What it is

Archify turns a codebase or a written description into an interactive system
diagram: architecture, dataflow, sequence, workflow. The agent writes typed JSON,
and a Node compiler turns that JSON into self-contained HTML, SVG, PNG, WebM and a
share card. You can search nodes, trace what reaches what, and compare two
snapshots as before and after.

## Weight

- Class: **fork-class**
- Code: 35,245 lines in 76 files - Prose: 21,185 lines in 109 files
- Tests: **37,047 lines in 132 files**, more test code than product code
- Standing on: Node, ffmpeg, and whichever model the agent runs on
- Real weight: a real rendering platform. Forking means owning it.

## The number that matters

The `SKILL.md` the model actually reads is **137 lines**.

Everything else, all 35,245 lines, is a deterministic renderer with five JSON
schemas (`archify/schemas/*.schema.json`) that the model never touches. The model's
entire job is to emit typed JSON. Layout, routing, contrast, export: all of it is
code, all of it is tested, none of it is a prompt.

## Claims vs code

| README says | Code says | Where |
|---|---|---|
| "Agents produce typed JSON IR; Archify deterministically compiles it" | implemented, with schemas and generated validators | `archify/schemas/`, `archify/test/generate-validators.test.mjs` |
| "deterministic checks" | implemented; the test suite is larger than the product | 132 test files |
| "without inventing topology" | structurally enforced: the model cannot draw, only declare | `archify/renderers/workflow/workflow-compiler.mjs:1-4400` |

## The mechanic worth naming

Put this next to `latent-spaces/brag` and you get the most useful comparison in
this whole category of repos:

| | brag | archify |
|---|---|---|
| Prompt the model reads | 173 lines | 137 lines |
| Its own engine | 0 lines | 35,245 lines |
| Tests | 0 | 37,047 lines |
| Who renders | somebody else's `hyperframes` | its own compiler, five JSON schemas |

Two trending repos. Prompts of near-identical size. Opposite answers to the only
question that matters: **who owns the engine underneath the prompt.**

brag borrows an engine and spends its effort writing down what good looks like.
Archify built the engine, then gave the model a narrow typed hole to speak
through, so that "the diagram is wrong" becomes a schema violation instead of a
judgement call.

Neither is the right answer in general. The point is that the prompt is never the
product, and the size of the prompt tells you nothing at all.

## What's in it for us

- **Overlaps with:** our diagram guidance and native Mermaid rendering. Neither
  produces an interactive, source-linked map, so the overlap is partial.
- **Cost to adopt:** Node toolchain, a 137-line skill permanently in context, and
  a platform-sized dependency for an occasional need.
- **Worth taking regardless:** the shape. When output correctness matters, do not
  ask the model for the artifact. Ask it for typed data, and let tested code
  produce the artifact. That is portable to anything we generate.
- **Breaks if adopted:** nothing. The cost is attention, not risk.

## Verdict

STEAL. Take the typed-IR-plus-deterministic-compiler shape. Install it only if
architecture diagrams become a weekly need rather than an occasional one: a
fork-class dependency should earn its place by frequency, not by being impressive.

---

*Produced with [`/teardown`](https://github.com/Sanexxxx777/teardown). Numbers from
`weigh.py`; nothing in the repo was executed.*
