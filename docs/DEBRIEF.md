# Debrief: chemical inventory project

For a collaborator picking this up cold. Full conversation: [session_transcript.md](session_transcript.md).

## What this is
A chemical inventory (not an SDS library) built from photos and video of bottles. The users are not chemists. Two people matter in it: the person doing the cataloging, and Carl, who buys the chemicals and handles restricted ones.

## What exists now
| Thing | Where | Notes |
|---|---|---|
| Inventory | `Chemical_Inventory.xlsx` | 52 bottles. Edit the green-header columns, then double-click `Rebuild.command`. |
| Searchable viewer | `inventory.html` | Table or cards, search, filters, photo and SDS per bottle. Read-only when opened as a file. |
| Label photos | `photos/` | One frame per bottle, pulled from a 6-minute video plus one photo. |
| SDS files | `sds/` | TCI 17, Sigma 9, AmBeed 8, plus boric acid (1996 sheet) and a sister-brand glycerin sheet. |
| Raw label readings | `readings/` | JSON per video segment, plus categories, IDs, edits and the hazard lookup cache. |
| Drop folders | `inbox/`, `invoices/` | New photos or notes; Carl's invoices. Each has a README. |
| Rules for AI agents | `AGENTS.md` (`CLAUDE.md` imports it) | Columns, flag rules, vendor SDS routines, how to rebuild. |
| Open tasks | `TODO.md` | Split by person. |

## How it works
1. A label is read from a photo or video frame. Nothing is guessed: unreadable fields stay blank, CAS numbers must pass their check digit.
2. Hazards are looked up on PubChem by CAS number. Flags are calculated, never typed.
3. RED = reproductive or genetic hazard code (H360, H361, H362, H340, H341): Carl handles. ORANGE = time-sensitive (peroxide formers). REVIEW = hazards unconfirmed, which never means safe. Recheck = the label read needs a human look.
4. Bottles are grouped TPU & polymers, additives, monomers & oligomers, with a proposed storage zone (Z1 to Z7).

## Current numbers
7 red, 23 review, 22 no flag, 21 marked recheck, 39 of 52 with an SDS linked.

Red bottles: tetraglyme, boric acid, Sudan I (all flagged by the EU as well), and DAEMA, benzoguanamine, dibutyl adipate x2 (flagged only by Japan's NITE agency).

## Decisions made
- Owner and quantity remaining are deliberately not tracked.
- Expiration only if printed on the label. Unknown received dates stay blank until invoices fill them in.
- Excel is the editing surface for now. A shared Google Sheet is the later step (needs a Google login for the command-line tool).
- Video intake works if each bottle is picked up and held still for about a second.

## Open questions
- NITE-only flags: keep as red or add a yellow tier? NITE lists even acetone as a suspected reproductive hazard.
- Should acrylate and methacrylate monomers get an orange shelf-life flag?
- How many real cabinets and shelves are there, so zones can become location codes?
- Gated SDSs Carl needs to pull: SOLESPHERE NP-30, Cabot TPX-5075, Nagase AOMA drum, the "VEEA" jar, methyl cellulose. Sartomer and Lubrizol were still being fetched when this was written.
- Prop 65 reproductive list is not checked yet.

## Caveats
This tool does not replace the SDS or Carl's judgment. Storage zones are general rules and should be checked against each SDS, section 7. Medium and low confidence label reads have not been verified by a person yet.
