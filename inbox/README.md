# Inbox

Drop anything new here, then tell Claude: "process the inbox".

What you can drop:
- Bottle photos (one bottle per photo, label facing the camera; add a second photo if the label wraps).
- Videos (pick up each bottle and hold the label still for about a second).
- A text note or spreadsheet with details a photo cannot show: location, date opened, corrections ("B0034: 06/26 is the received date").
- Put a shelf's photos in a subfolder named after the location (for example `Z5-shelf2/`) and that location is recorded for every bottle in it.

What happens:
1. Each bottle is read, given the next Bottle ID, looked up for hazards, flagged, and added to the inventory.
2. SDS is fetched where the vendor allows it; the rest go on Carl's list.
3. Files are moved to `inbox/processed/<date>/`. Nothing is deleted.
4. You get a short summary: what was added, any red flags, anything that needs a recheck.

Invoices go in `invoices/`, not here.
