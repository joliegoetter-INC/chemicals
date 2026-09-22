# Chemical Inventory

## Response style
- Be concise. Lead with the answer, then only what is needed to act on it.
- Plain language. Users are not chemists.
- No long tables or background unless asked.

## Purpose
Chemical inventory (not an SDS library) built from bottle photos. Hundreds of bottles, mixed vendors.

## Storage
- Google Sheets is the source of truth. Tabs: Inventory (one row per bottle), Chemicals (one row per CAS: hazards, flags, SDS link), Needs review, Carl's SDS list.
- SDS PDFs: `sds/Vendor_CatNo_CAS.pdf`. Photos linked from rows.

## Pipeline
- Label readings live in `readings/*.json` (one object per bottle). Photos in `photos/`.
- `python3 tools/build_inventory.py readings Chemical_Inventory.xlsx` merges readings, looks up hazards on PubChem, sets flags, and rebuilds the workbook. Never hand-edit flags in the workbook: fix the reading and rebuild.
- Video intake: bottles must be picked up and held to the camera about 1 second each. Extract frames with ffmpeg, read the sharpest frame per bottle.
- For now the workbook is Excel. Move to Google Sheets once `gws auth login` is done.

## Categories and locations
- Group order everywhere: 1 TPU & polymers, 2 Additives, 3 Monomers & oligomers. Mapping lives in `readings/categories.json` (proposed, Carl confirms).
- "Proposed location" is a suggestion from `zone()` in the build script. "Location" is where the bottle really is. Never copy one into the other without a person confirming.
- RED overrides category: red bottles go to the Carl-only shelf. Photoinitiators are stored away from monomers.
- `python3 tools/build_html.py` rebuilds `inventory.html` (table and card views) from the workbook.

## Adding and editing
- `python3 tools/serve.py` runs the local app at http://localhost:8791/inventory.html with Add, Edit and "confirm accurate" buttons. Opening `inventory.html` as a file is read-only.
- Main way to edit: in `Chemical_Inventory.xlsx`, green-header columns on the Inventory tab. New bottle = new row with an empty Bottle ID. Recheck done = change YES to OK. Then double-click `Rebuild.command` (or run the two build scripts). The builder reads the changes back before it regenerates the file.
- Human edits are stored in `readings/edits.json` (keyed by Bottle ID) and manual bottles in `readings/manual.json`. They survive every rebuild. Grey-header columns (flags, SDS, proposed location) are recalculated and any edits there are discarded.
- Open tasks live in `TODO.md`.
- Bottle IDs are permanent (`readings/ids.json`). Never renumber.
- "Process the inbox" means: read every file in `inbox/` (see `inbox/README.md`), add readings as a new `readings/seg_*.json`, copy the best label image to `photos/`, rebuild, fetch SDSs, move the files to `inbox/processed/<date>/`, and report what was added, red flags first.

## Inventory columns
Bottle ID (QR sticker), name, common name, CAS, vendor, catalog no., size + unit, physical state, purity/grade, lot, location, signal word, pictograms, hazard codes, flags, SDS link, received (`YYYY-MM`), opened, expiration, photo link.
- Blank means unknown. Never guess.
- Expiration only if printed on the label.
- Do not add owner or quantity remaining. Deliberately excluded.
- Tag each value's source: label, handwritten, lookup, or invoice.

## Lookup rules
- Key: CAS + vendor catalog number.
- Hazard codes: PubChem (by CAS).
- SDS: vendor product page.
- AmBeed: open the product page by CAS in a real browser (plain scripted requests get 403), read the SDS PDF link from the SDS dialog, download it directly.
- Gatekept vendors go on Carl's SDS list. Never submit a vendor contact form.
- Sigma-Aldrich: load the product page in a real browser, reuse its cookies and user agent with curl on `/US/en/sds/<brand>/<ProductNo>`; pause a minute after about 7 files (see `sds/routine_Sigma.md`).
- Record new vendor routines here as they are learned.

## Flags
- Red dot (reproductive, Carl handles): H360, H361, H362, H340, H341, or on the Prop 65 reproductive list.
- Orange dot (time-sensitive): CAS on a peroxide-former list. Received and opened dates required.
- Flags come from the lookup, never from the label pictogram alone.
- Flag reason must name the source (ECHA, NITE Japan, etc.). Any one credible source is enough for RED.
- REVIEW means hazards unconfirmed (no CAS, trade product, polymer not in PubChem). It never means safe.

## Safety behavior
- Lookup fails or sources disagree: mark "needs review". Never mark safe.
- Crystals or crusted cap: tell the user not to open or shake it.
- This tool does not replace the SDS or Carl's judgment.

## Dates
- Backlog bottles with no received date stay blank.
- Check invoices only on request or for orange-dot bottles.

## People
- Carl: purchasing, vendor accounts, handles restricted chemicals.
- Nick: TODO role.

## Open questions
- Facility type and state/country (decides regulatory fields).
- Which vendors gatekeep SDSs (only AmBeed tested: open).
