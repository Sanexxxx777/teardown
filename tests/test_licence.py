#!/usr/bin/env python3
"""Tests for the licence classifier. Run: python3 tests/test_licence.py

The cases are real ones from measuring a month of a GitHub trending feed, where
the API returned NOASSERTION for 19 repositories and 8 of them turned out to
restrict use. The first test is the false positive that produced this file.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "skills" / "teardown" / "scripts"))
from weigh import classify_licence, find_licence  # noqa: E402

FAILED = []
RAN = 0


def check(name: str, text: str, family: str, added: int = 0) -> None:
    global RAN
    RAN += 1
    got = classify_licence(text)
    if got["family"] != family:
        FAILED.append(f"{name}: expected family={family}, got {got['family']} ({got['meaning']})")
    if len(got["added"]) != added:
        FAILED.append(f"{name}: expected {added} added clause(s), got {got['added']}")


# --- the false positive this file exists for -------------------------------
# The AGPL's own text says "noncommercially". A clause search that runs before
# the licence is identified calls every AGPL repo a custom non-commercial licence.
AGPL = """GNU AFFERO GENERAL PUBLIC LICENSE Version 3, 19 November 2007
 ... you may convey covered works to others ... whether gratis or for a fee ...
 Propagation includes copying, distribution (with or without modification).
 You may convey verbatim copies, and you may charge any price or no price,
 including conveying them noncommercially to any recipient."""
check("agpl text containing 'noncommercially'", AGPL, "copyleft")

# --- a permissive header with a restriction appended ------------------------
# The costly case: the first line reads MIT and the file is not MIT.
check("mit header, no-commercial clause appended",
      "MIT License\n\nCopyright (c) 2026 Someone\n\nPermission is hereby granted, free of "
      "charge, to any person obtaining a copy...\n\nThis software may not be used for "
      "commercial purposes without a separate agreement.\n",
      "source-available", added=1)
check("commons clause on top of mit",
      "MIT License\n\nPermission is hereby granted, free of charge, to any person...\n\n"
      '"Commons Clause" License Condition v1.0: the License does not grant you the right '
      "to Sell the Software.\n",
      "source-available", added=1)

# --- plain permissive -------------------------------------------------------
check("plain mit", "MIT License\n\nPermission is hereby granted, free of charge, to any "
                   "person obtaining a copy of this software...\n", "permissive")
check("apache", "Apache License\nVersion 2.0, January 2004\nhttp://www.apache.org/licenses/\n",
      "permissive")
check("bsd", "Redistribution and use in source and binary forms, with or without "
             "modification, are permitted provided that...\n", "permissive")
check("unlicense", "This is free and unencumbered software released into the public domain.\n",
      "public-domain")

# --- source-available families the API reports as "Other" -------------------
check("fair source", "# Fair Source License Agreement (Version 1.0)\nThis agreement limits "
                     "use until the change date...\n", "source-available")
check("polyform noncommercial", "# PolyForm Noncommercial License 1.0.0\n\nAcceptance...\n",
      "source-available")
check("elastic v2", "Elastic License 2.0\n\nYou may not provide the software to third "
                    "parties as a hosted or managed service...\n", "source-available")
check("busl", "Business Source License 1.1\n\nUse of the Licensed Work is not permitted in "
              "production until the Change Date.\n", "source-available")

# --- copyleft ---------------------------------------------------------------
check("gpl", "GNU GENERAL PUBLIC LICENSE Version 3\n", "copyleft")
check("lgpl", "GNU LESSER GENERAL PUBLIC LICENSE Version 2.1\n", "copyleft")
check("mpl", "Mozilla Public License Version 2.0\n", "weak-copyleft")

# --- nothing recognisable ---------------------------------------------------
check("custom text, no known licence", "Copyright (c) 2026 someone. All rights reserved.\n",
      "unknown")
check("custom text demanding permission",
      "Copyright 2026. Use of this code requires prior written permission of the author.\n",
      "source-available", added=1)

# --- no file at all ---------------------------------------------------------
import tempfile  # noqa: E402

with tempfile.TemporaryDirectory() as tmp:
    got = find_licence(Path(tmp))
    if got["family"] != "none":
        FAILED.append(f"empty dir: expected family=none, got {got['family']}")
    (Path(tmp) / "LICENSE").write_text("MIT License\n\nPermission is hereby granted, free of "
                                       "charge, to any person obtaining a copy\n")
    got = find_licence(Path(tmp))
    if got["family"] != "permissive" or got["file"] != "LICENSE":
        FAILED.append(f"LICENSE file: got {got}")

if FAILED:
    print("FAILED:")
    for f in FAILED:
        print("  -", f)
    raise SystemExit(1)
print(f"all tests passed ({RAN} licence cases + 2 file cases)")
