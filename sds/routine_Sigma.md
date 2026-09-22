# Sigma-Aldrich SDS download routine

1. Open a dedicated browser tab (`tabs_create`) and navigate to `https://www.sigmaaldrich.com/US/en/product/<brand>/<ProductNo>` (brand is usually `aldrich`; `sial` for 74731). This clears the Akamai bot wall and mints session cookies.
2. Grab `document.cookie` and `navigator.userAgent` via the JS tool, and save the cookie string to a file (refresh the `bm_so`/`bm_sv` values from a fresh page load whenever requests start failing).
3. `curl -L --compressed -A "<Chrome UA>" -b "<cookie>" -H "Referer: .../product/<brand>/<ProductNo>" -H "Sec-Fetch-Mode: navigate" -H "Sec-Fetch-Site: same-origin" "https://www.sigmaaldrich.com/US/en/sds/<brand>/<ProductNo>"` returns the PDF directly (200, application/pdf).
4. Akamai rate-limits after roughly 7 SDS fetches with a rolling 403 "Access Denied" (global, not per-product). Sleep 60-90s and retry; it clears within a few minutes. Do not thrash, and do not use the browser's `navigate` on an SDS URL (it triggers a save dialog).
5. Verify with `file` plus `pdftotext <f> - | grep <ProductNo>`; the header block also gives Brand and CAS-No. Localhost relay from the browser page does not work (the browser pane cannot reach 127.0.0.1).
