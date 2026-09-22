# To do

## Victor
- [ ] **Look into Japan's NITE hazard classifications and decide how to treat them.**
  - NITE is a Japanese government agency, not a vendor. PubChem shows its GHS classifications next to the EU (ECHA) ones.
  - NITE classifies on hazard: if any study shows an effect at any dose, it gets the code. It lists acetone as H361 (suspected reproductive hazard) from high-dose animal studies. The EU does not.
  - Bottles that are red from NITE alone: DAEMA (B0028, H360), benzoguanamine (B0011, H361), dibutyl adipate (B0039, B0043, H361).
  - Decision needed with Carl: keep NITE-only as RED, or move it to a new YELLOW tier ("one agency, suspected: gloves and hood, no Carl-only rule").
  - Start here: https://www.nite.go.jp/chem/english/ghs/ghs_index.html and compare with the ECHA entry for the same CAS.
- [ ] Count cabinets and shelves so the proposed zones (Z1 to Z7) can become real location codes.
- [ ] Run `gws auth login` if we want a shared Google Sheet later.

## Carl
- [ ] Drop invoices and packing slips in `invoices/`.
- [ ] Pull the gated SDSs (see the "Carl SDS list" tab): SOLESPHERE NP-30, Cabot TPX-5075, Nagase AOMA drum, VEEA jar, methyl cellulose.
- [ ] Get a current boric acid SDS (the one on file is from 1996).
- [ ] Confirm the categories in `readings/categories.json` and the storage zones.
- [ ] Decide whether acrylate and methacrylate monomers get an ORANGE (shelf life) flag.
- [ ] Identify the unlabeled "VEEA" jar (B0046) and the Lubrizol AG8451 sample.

## Open in the inventory
- [ ] 21 bottles marked Recheck (medium or low confidence reads, two possible duplicate pairs).
- [ ] Sartomer and Lubrizol SDSs still downloading.
- [ ] Prop 65 reproductive list not checked yet.
