# One Line, One Chill — strategy

## Exact deliverable
Program/v1 harness (python3.13 or node22, no network) runs the repository-root
entrypoint. It must write exactly one judged artifact: `/output/entry.txt`,
UTF-8 text, 1-200 characters, not only whitespace. Nothing else may be left in
`/output`. The submitted text is byte-identical to the file's bytes; no trailing
newline, because those bytes are what the judge sees as "Entry A" / "Entry B".

Entrypoint chosen: `main.py` (python3.13, stdlib only).

## Scoring and judge criteria, in the rubric's own order
The judge (superbot / z-ai/glm-5.3-flash, high reasoning) is shown two entries
and must pick the more frightening one. It weighs, most important first:

1. Reads as a horror story in a single sentence; one line that lands as a scare.
2. Frightens: dread that outlasts the line; the scare is earned, not announced.
3. Is vivid: concrete images and specific detail, not vague darkness/fear.
4. Is original: a turn or image not met a hundred times before; not the obvious
   mirror, doll or basement.
5. Is crafted: tight sentence, building rhythm, last word lands the blow.

A line may frighten by what it withholds. Gore for its own sake does not count.

Each pairing is judged twice (both label orders); call score is
0.5 + margin/10 for the pick, the rest for the other, and the game is the mean
of the two calls. Final ranking is a Bradley-Terry win rate over the final heat
(3 Swiss rounds + top-12 playoff); playoff finalists outrank non-finalists,
judged entries outrank cut entries. Ties: playoff heads-to-head, then smaller
text (fewer bytes), then earlier receipt. Only top 10 are paid ($1.54 down to
$0.06); there are 1,500+ entrants, so a top-place finish needs decisive wins.

## Hard caps
- 1-200 characters after UTF-8 decode; whitespace-only is invalid; a failed
  gate takes no place and forfeits the prize.
- No trailing newline in the artifact (the exact bytes are the entry).
- File must be ordinary readable text: create mode 0644 (a 0600 tempfile from
  tempfile.mkstemp must be chmod'd 0644 before os.replace).
- `/output` holds only `entry.txt`; the program runs in a sandbox with no network.
- Root freshness commit and LICENSE commit must stay intact; all work committed.

## What the live feed taught me (angles to avoid)
Current feed lines use: an extra finger when counting, an extra scraped plate,
a phone typing in the owner's handwriting, a 3 a.m. baby-monitor voice, a
sleep app recording whispering, an attic hum. Counting anomalies, phones,
monitors, 3 a.m. and announced "I'm already inside" lines are crowded and
lose originality; announced scares also lose on criterion 2.

## Concrete plan to maximize the score
Pick a single sentence that hits the criteria in order:
- Whole horror story in one breath, plain and unmistakably on subject.
- Earned, withheld threat: no ghost/possession word, no explanation; the reader
  supplies the horror and it keeps working after the line ends.
- Concrete, specific objects (an empty house detail), not vague fear/darkness.
- Fresh mechanism: an intruder revealed by physics, not a mirror/doll/basement
  or a device. Short beats, final word carries the blow.
- Keep it well under 200 chars (smaller text also helps the tie-break).

Chosen line:
"The bathtub was full when I got home; the taps were dry, and the water was still warm from a body."

Why it beats the field: it is a complete single-sentence scare (1); it names no
monster and states no threat, leaving the reader to ask whose body and where it
went (2); tub, dry taps and warm water are visible, specific details (3); the
dry-taps/body-heat turn is not a mirror, doll, basement, phone or counting gag
(4); three shortening beats land on the last word "body" (5). ASCII, 98 bytes,
so it also wins the smaller-text tie-break against longer rivals.

## Implementation and verification steps
1. Write `main.py` (v1): pure-stdlib script that writes the exact bytes.
2. In a later, separate step rewrite the same `main.py` with the real
   improvement: atomic temp file + chmod 0644 + os.replace, full local
   validation (UTF-8 round-trip, 1-200 chars, non-whitespace, no newline),
   and printed bytes/chars/sha256/mode for verification.
3. Run it; verify `/output/entry.txt` bytes, char count, absence of a trailing
   newline, sha256 and 0644 mode; keep `/output` clean.
4. `git add -A` and commit, preserving the root anchor and LICENSE commits;
   print the final commit sha. Do not upload or submit.
