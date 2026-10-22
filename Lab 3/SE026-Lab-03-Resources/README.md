# SE026 Lab 3 resources

Extract this ZIP first. Open the extracted SE026-Lab-03-Resources folder.
It contains web/index.html and blank CSV worksheets. missing.txt is deliberately absent.

Windows: in File Explorer open this folder, click the address bar, type cmd and press Enter.
Run: py --version
Run: py -m http.server 8000 --bind 127.0.0.1 --directory web
If py is unavailable but python works, replace py with python in both commands.
macOS/Linux: open a terminal in this folder and use python3 instead of py.

Leave that terminal running. Open http://127.0.0.1:8000/index.html in a browser.
Open developer tools > Network, reload, and select index.html.
Open http://127.0.0.1:8000/missing.txt for a missing-resource response.
Stop the server using Ctrl+C in its terminal, then retry with browser cache disabled.
Restart with the same command and verify index.html loads again.

DNS, in a second terminal: nslookup moodle.ccun.edu.kh
Then visit https://moodle.ccun.edu.kh/ logged out. Do not enter credentials.
Keep lookup results separate from browser access results. Actual DNS results may change.

If port 8000 is occupied, use 8001 in the command and in every local URL.
Do not open index.html by double-clicking: a file:// page bypasses the HTTP server.
Do not change DNS, firewall or network settings for this lab.
CSV files are blank working templates, not answer keys. A text editor is also sufficient.
