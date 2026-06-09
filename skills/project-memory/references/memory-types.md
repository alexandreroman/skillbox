# Memory Types

## feedback

Guidance the user has given about how to approach
work — both what to avoid and what to keep doing.
Record from failure AND success.

**When to save:** any time the user corrects your
approach OR confirms a non-obvious approach
worked. Include *why* so you can judge edge cases.

**Body structure:** lead with the rule, then a
**Why:** line and a **How to apply:** line.

## project

Information about ongoing work, goals,
initiatives, bugs, or incidents not derivable
from code or git history.

**When to save:** when you learn who is doing
what, why, or by when. Convert relative dates to
absolute dates (e.g. "next Thursday" becomes
"2026-04-16").

**Body structure:** lead with the fact or
decision, then a **Why:** line and a
**How to apply:** line. Phrase the fact in the
present tense as a standing truth, not as a past
event ("the API is versioned under /v2", not
"the user asked to version the API under /v2").

## reference

Pointers to where authoritative information lives,
inside or outside the repository — docs sites,
dashboards, issue trackers, chat channels, API
endpoints, firmware or download URLs, on-device
files, or a CLI recipe to reach a resource. The
durable value is the **location and its purpose**,
so a future session goes straight to the source
instead of guessing or rediscovering it.

**When to save:** when you learn where a resource
lives and why it matters — especially when it is
not discoverable from the repository itself.
Choose `reference` over `project` when the lasting
value is the *pointer* (where to look) rather than
the *work* it supports, and over `feedback` when
you are recording a *location* rather than a way
of working. A quirk or fact you keep needing to
look up (a serial port, a device path, an API
behaviour) belongs here once it has a stable
source to point at.

**Body structure:** lead with what the resource is
and where it lives (URL, path, or command), then a
**Why:** line for when to reach for it and a
**How to access:** line with the concrete steps or
address.
