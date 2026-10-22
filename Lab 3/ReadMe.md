# Lab 3: Application Requirements, HTTP and DNS
**Network System Design | SE026 | 2026-27**
**Name:** LOR HENG RITH

---

## 3. Inspect a successful HTTP request

| Record | Your observation |
|---|---|
| URL / request method | `http://127.0.0.1:8000/index.html` / `GET` |
| Status / Content-Type | `200 OK` / `text/html` |
| Response content / HTTP version | Page titled "Local networking lab", same as `web/index.html`. HTTP version: not displayed |

127.0.0.1 is my own computer (loopback), so this tests a local service only.

---

## 4. Compare three service outcomes

- **A. Missing resource:** `http://127.0.0.1:8000/missing.txt` returned `404 File not found`.
- **B. Stopped server:** after Ctrl+C, `http://127.0.0.1:8000/index.html?test=stopped` showed "This site can't be reached, localhost refused to connect" (`ERR_CONNECTION_REFUSED`). No HTTP status.
- **C. Restored:** re-ran the same server command, `...?test=restored` returned `200 OK` with the page.

| Case | Actual status or error | HTTP response received? |
|---|---|---|
| Working page | `200 OK` | Yes |
| Missing resource | `404 File not found` | Yes |
| Stopped server | `ERR_CONNECTION_REFUSED` | No |
| Restored service | `200 OK` | Yes |

**Differences**
- **Working:** server, port and file all fine (GET `/index.html` gave 200).
- **Missing:** server answered with 404, so only that file is absent.
- **Stopped:** no response, nothing listening on port 8000, so the failure is the service not running.
- **Restored:** same command brought back 200, so the server process was the only cause.

---

## 5. Separate DNS from application access

| DNS / application observation | Your result |
|---|---|
| Resolver / returned answer | Resolver `one.one.one.one` (`1.1.1.1`). Non-authoritative answer: `moodle.ccun.edu.kh` → `103.142.5.62`. Resolver IP = DNS server asked; returned IP = web server. |
| Public page outcome | `https://moodle.ccun.edu.kh/` loaded logged out: CCUN banner, Log in button, university tiles. No credentials entered. |
| What each test establishes | `nslookup` shows only that the name resolves. The browser shows that connectivity, TLS and the web app also work. |

**Why 127.0.0.1 works without DNS:** it is already an IP address, so there is no name to look up.

### Reflection

1. **Missing resource vs DNS failure:** a missing resource still gets an HTTP response (404). A DNS failure happens before any connection, so there is no HTTP response at all.
2. **Dev tools vs capture:** the browser is the endpoint and decrypts HTTPS. A capture on the wire only sees encrypted TLS data.
3. **Only one dependency changed:** 4B (stopped server). Restored by re-running `py -m http.server 8000 --bind 127.0.0.1 --directory web`.

---

## 6. Requirements and acceptance tests

*Numeric targets are proposed assumptions, not approved guarantees. Users and files are fictional.*

### Requirements

| ID | Application | User | Location | Task | Proposed target | Dependencies |
|---|---|---|---|---|---|---|
| R1 | Moodle | Student A | Student lab PC | Log in and download `week3-notes.pdf` | Page in ≤ 5 s, 2 MB file in ≤ 30 s, 30 students at once | DNS, Internet link, TLS, Moodle app, login |
| R2 | Video meeting | 10 participants | Classroom Wi-Fi | Join and talk with audio/video for 30 min | Join in ≤ 30 s, no audio drop > 2 s, ~720p video | DNS, Wi-Fi, bandwidth, meeting service, firewall |
| R3 | Local printing | Staff B (authorized) | Office, same building network | Print 5-page `test-print.pdf` | Printed in ≤ 60 s, unauthorized users refused | Printer name/address, switch/VLAN, print server, authorization |

### Acceptance tests

| ID | Req | Location | Action | Expected result | Evidence | Status |
|---|---|---|---|---|---|---|
| T1 | R1 | Student lab PC | Open Moodle, log in with test account, download `week3-notes.pdf` | File downloads fully, size/hash matches | Screenshot, download time, hash | Proposed |
| T2 | R2 | Classroom, 10 devices | Start test meeting, all join, 3 speak, 2 share video for 10 min | Join ≤ 30 s, clear speech, no freeze > 2 s | Join times, meeting stats, checklist | Proposed |
| T3 | R3 | Authorized PC, then unauthorized account | Print `test-print.pdf` from each | Authorized: 5 pages in ≤ 60 s. Unauthorized: refused | Printout, queue log, error message | Proposed |

### Failure scenario (one dependency)

**DNS stops working** for the student lab while everything else is fine. T1 fails ("server not found") and `nslookup moodle.ccun.edu.kh` errors out. Pinging the server's IP would still work, so ping alone would miss it.
