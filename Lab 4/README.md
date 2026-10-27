# TCP and UDP Socket Applications

Objective
Run the supplied echo application, explain TCP framing and UDP datagrams, and justify a transport choice with clear limits.

Software and files
Use Python 3 and two terminals. Extract SE026-Lab-04-Resources-2026-27.zip. It contains echo.py, README.md and observations.csv. Open two terminals in the extracted SE026-Lab-04-Resources folder. On Windows type cmd in the File Explorer address bar. Confirm dir echo.py finds the script.

Python command
Run py --version. Use python instead if the Windows launcher is absent, or python3 on macOS/Linux. Both terminal commands must use the same interpreter and folder. This lab binds only 127.0.0.1:12000; a second computer is not required.

TCP exchange
Terminal A: py echo.py tcp server
Keep it running. Terminal B: py echo.py tcp client "hello class"
Record the returned message, server endpoint and displayed local endpoint. The program echoes the same text; it does not convert text to uppercase.

Change the message
In terminal B run: py echo.py tcp client "Mixed CASE 123". Record the reply and any changed client port. The OS chooses an ephemeral client port; do not require a fixed number.

Read the TCP code
Open echo.py in a text editor. Locate SOCK_STREAM, connect, listen, accept, sendall, recv and the loop checking for a newline. The script appends a newline to the encoded message and receives in a loop until the delimiter, close or size limit. It sets timeouts and limits message bytes.

Explain framing
TCP delivers an ordered byte stream, not preserved application messages. A single recv may return only part of a message. Explain why the receive loop is needed and how the newline marks completion in this program. Do not use embedded newlines or messages exceeding the stated 4096-byte limit.

Stopped TCP server
Stop terminal A with Ctrl+C, then repeat the TCP client. Record the actual timeout/refusal/connection error. Keep the output, even if its wording differs from another computer.

UDP exchange
Terminal A: py echo.py udp server
Terminal B: py echo.py udp client "hello class"
Repeat with "Mixed CASE 123". Record the messages and endpoints. UDP preserves datagram boundaries, but transport-level delivery and order are not guaranteed.

No UDP server
Stop terminal A with Ctrl+C and repeat the UDP client. Record the exact result. A receive timeout or OS-specific connection error is valid evidence; Windows may report ConnectionResetError. Do not claim that every absent-server run must time out.

Transport design
Choose a fictional application. State what its users need, whether it needs reliable delivery/order or low delay, and what the application would need to add if it used UDP. Successful local echo proves only the tested exchange. An absent-server error does not demonstrate random network packet loss.

Reflection and finish
1. Why is an IP address alone insufficient to identify the service?
2. What supplies TCP message framing here?
3. Can a UDP application add acknowledgements/retries?
4. Does TCP alone supply encryption or a minimum speed?
Save the observation table and stop all temporary echo servers.