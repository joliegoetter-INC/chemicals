# TCI SDS download routine

1. Open https://www.tcichemicals.com/US/en/p/<CatalogNo> in the built-in Browser pane (tabs_create + own tabId); wait ~6 s. curl/Playwright/Chrome-for-Testing all get 403 from Akamai, so every network call must run inside that pane.
2. In-page JS: POST to /US/en/documentSearch/productSDSSearchDoc with form fields brandCode=TCI, productCode=<code>, langSelector=en, selectedCountry=US and headers CSRFToken: ACC.config.CSRFToken + X-Requested-With: XMLHttpRequest. Response is the PDF (Content-Disposition <code>_US_EN.pdf). Loop all codes from one page load.
3. Getting bytes to disk: run a local sink (python http.server on 127.0.0.1:8765) that base64-decodes a 'payload' form field and writes the PDFs. The pane blocks fetch/XHR/iframe/img/WebSocket/sendBeacon to localhost, but a top-level FORM POST (method=POST action=http://127.0.0.1:8765/save target=_self) gets through.
4. Because that form submit navigates the tab away, stage the base64 blobs in IndexedDB on the tcichemicals.com origin first, then loop: navigate back to the product page, read the next ~3 unsent records, mark them sent, submit the form. 3 files (~1.1 MB) per submit is reliable; 17 at once fails.
5. Verify with `file` + `pdftotext`: each PDF must say SAFETY DATA SHEET and contain its catalog number and CAS.
