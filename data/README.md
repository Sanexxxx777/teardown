# 138 trending agent repos, measured by code

`trending-138.csv` is every unique repository that appeared in one month of a GitHub
trending digest, 15 August to 17 September 2026, with its weight measured from its
files by `skills/teardown/scripts/weigh.py`.

It exists because a repository's description does not tell you what you are picking up.
Before measuring, the first 40 of these were sorted by their digest lines alone. 25 of
those 40 turned out to be platform-scale while reading as "worth a look". One of them
presents a 137-line instruction file on top of 35,245 lines of its own code and 37,047
lines of tests.

## What is in it

| Weight class | Count | What it means |
|---|---|---|
| fork-class | 67 | someone else's codebase; adopting it means maintaining it |
| medium | 32 | too large to rebuild, small enough to read |
| prompt-class | 15 | the product is the writing; the code is glue |
| small | 9 | readable end to end in one sitting |
| not downloaded | 10 | over 250 MB, where the size is the answer |
| removed from GitHub | 5 | already 404 when the sweep reached them |

56 percent are platform-scale. 24 are light enough to rebuild in an evening, and half of
those are not tools at all: link lists, notes, one joke.

## Columns

`code_lines`, `prose_lines` and `test_lines` are counted separately because the ratio
between them is the classification. Prose beating code two to one, under 2,000 lines of
code, means the product is the instructions. Code beating prose three to one means the
product is the code and the README is marketing for it.

`generated_lines` is code no person wrote, detected by path and filename
(`zz_generated`, `*.gen.go`, `*.pb.go`, `_pb2.py` and friends). It is excluded from
`code_lines`. One repository here reads as 2.12 million lines until you subtract the
521,227 that came out of a code generator, one file of which is 136,419 lines on its own.
The fix landed mid-sweep and moved no repository between classes, which is how you know
it was about honesty rather than verdicts.

`license_spdx` is what the GitHub API reported. `license_family` is what the licence
actually permits, and the two disagree more than you would expect.

GitHub could not identify the licence of 19 of these repositories and returned
`NOASSERTION`. Reading all 19 files:

| What they turned out to be | Count |
|---|---|
| ordinary MIT or Apache under a modified header | 11 |
| source-available, with use restrictions | 5 |
| copyleft (AGPL) | 3 |

So "unidentified" is not a synonym for "probably fine": 8 of the 19 cannot be taken from.
Among them a Fair Source Agreement, the Elastic License 2.0, PolyForm Noncommercial, and
the one worth remembering. **An MIT header with a no-commercial clause appended further
down.** The first line says MIT. The file is not MIT. A licence scanner that reads only
the first line, or trusts the API, reports that repository as permissive.

Across all 138: 102 you can take code from, 14 copyleft, 5 source-available, 9 with no
licence file at all (the author keeps all rights by default), 1 weak-copyleft, 7 not
measured. `license_note` carries the reason where there is one. This is a pointer to go
and read the file, not legal advice.

`stars_at_measurement` is a snapshot and drifts. Treat it as evidence that promotion
reached people, nothing else.

## What did not survive measurement

Ten of these repositories were flagged by eye before being opened, from a three-part
pattern: a fresh account, a name borrowing a famous product, and stars appearing faster
than a repository can plausibly earn them. Five of the ten were gone from GitHub within a
day. Going by their names: a miner, "free" builds of Acrobat and Total Commander, an
"optimizer", and a panel whose purpose was never seen. Reading the code of the five still
up later cleared four of them as ordinary tools, so the eye was right about half the time.
The obvious next step was still to try to mechanise the pattern. It does not mechanise.
All three parts were tested against the repositories that are still up and the ones read
in full:

- **Stars per day: no separation.** 24 of 28 legitimate repositories grow faster than the
  slowest flagged one. The fastest riser in the whole set, at 3,243 stars a day, is a
  legitimate project from a known lab.
- **Account age: separates backwards.** The flagged repositories come from *older*
  accounts (median 2,340 days) than the legitimate ones (median 658). Several legitimate
  projects sit under organisations created after the repository itself.
- **A borrowed product name: 50% precision.** It fires on 12 of the 138 and is right
  about half the time. Among the ones it accuses are `openai/codex` and
  `deepseek-ai/deepseek-harness`, which are the products' actual owners.

So there is no check to ship here, and none is shipped. What survives is narrower and
worth stating plainly: removal is the only hard signal, it arrives a day late, and by
then the repository is gone along with the evidence. None of the five removed ones has
a star count in this dataset, because they were already 404 when the sweep reached them.

## Limits

- Ten repositories over 250 MB were not downloaded. They carry a recorded size instead of
  an invented measurement.
- Five were already removed from GitHub, so nothing about them was measured, including
  their star counts.
- Six changed owner or name during the month. GitHub redirects silently, so a link from
  the original digest still resolves and the move is invisible; `renamed_to` records it.
- Jupyter notebooks are counted as files, not lines. A `.ipynb` holds source, prose and
  base64 output in one JSON document, and its line count means nothing.
- Nothing from any measured repository was executed. `fetch.sh` pulls a tarball through
  the GitHub API and `weigh.py` counts lines. That is the whole method.

## Reproduce a row

```bash
bash skills/teardown/scripts/fetch.sh owner/repo /tmp/x
python3 skills/teardown/scripts/weigh.py /tmp/x
```

Line counts drift with the default branch. A row here is what the repository looked like
between 18 and 19 September 2026.
