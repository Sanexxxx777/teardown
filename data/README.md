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

`license_spdx` comes from the GitHub API at measurement time. `none` means no licence
file at all, so the rights stay with the author. `NOASSERTION` means GitHub could not
identify the file, which is not the same as permissive: one repository here carries the
Fair Source License 1.0, which is not an open-source licence. 35 of the 138 have no
licence you can rely on, and 9 more are AGPL or GPL. This column is a pointer to go and
read the file, not legal advice.

`stars_at_measurement` is a snapshot and drifts. Treat it as evidence that promotion
reached people, nothing else.

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
