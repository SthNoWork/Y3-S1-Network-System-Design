# Lab 4: TCP and UDP Socket Applications

## 1. Observations Summary

| Activity | Command / Input | Local Endpoint | Target / Server | Result / Reply | Note |
|---|---|---|---|---|---|
| TCP Exchange | `py echo.py tcp client "hello class"` | `('127.0.0.1', 49848)` | `('127.0.0.1', 12000)` | `Reply: hello class` | Ephemeral client port assigned. |
| TCP Message Change | `py echo.py tcp client "Mixed CASE 123"` | `('127.0.0.1', 49864)` | `('127.0.0.1', 12000)` | `Reply: Mixed CASE 123` | New ephemeral port assigned by OS. |
| TCP Stopped Server | `py echo.py tcp client "Testing after ctrl + c server"` | `('127.0.0.1', 49866)` | `('127.0.0.1', 12000)` | `TimeoutError: timed out` | Connection could not be established; timed out after 2s. |
| UDP Exchange | `py echo.py udp client "hello class"` | `('0.0.0.0', 54378)` | `('127.0.0.1', 12000)` | `Reply: hello class` | Bound to wildcard address with ephemeral port. |
| UDP Absent Server | `py echo.py udp client "hello class"` | `('0.0.0.0', 54691)` | `('127.0.0.1', 12000)` | `ConnectionResetError: [WinError 10054]` | Windows loopback ICMP port unreachable notification delivered to socket. |

## 2. TCP Message Framing

TCP is a stream-oriented protocol with no built-in message boundaries; bytes sent in multiple calls may arrive together or fragmented across multiple `recv()` calls. To reconstruct discrete messages, a receive loop reads chunks of data until it detects an agreed delimiter. In `echo.py`, the newline character (`\n`) acts as the message framing boundary, indicating that the full message has arrived.

## 3. Transport Design

- **Fictional Application:** Real-time multiplayer game player-position telemetry.
- **User Requirements:** Low latency is critical. Recent player coordinates must arrive immediately; old coordinates are useless if delayed.
- **Transport Choice:** UDP is preferred because TCP's retransmissions and head-of-line blocking cause lag spikes.
- **Additions Needed over UDP:** The application must add sequence numbers (to discard out-of-order/stale position updates) and lightweight checksums/integrity checks.

## 4. Reflection

1. **Why is an IP address alone insufficient to identify the service?**
   An IP address only identifies a host on the network. Port numbers are required to multiplex and route traffic to a specific process or service running on that host.

2. **What supplies TCP message framing here?**
   The application layer supplies framing by appending a newline delimiter (`\n`) to each message and reading the byte stream in a loop until `\n` is encountered.

3. **Can a UDP application add acknowledgements/retries?**
   Yes. Reliability can be implemented at the application layer by tracking packet sequence numbers, returning acknowledgement packets, and retransmitting lost packets on timeout.

4. **Does TCP alone supply encryption or a minimum speed?**
   No. TCP provides reliable, ordered byte delivery, but it transmits data in plaintext without encryption and does not guarantee bandwidth or a minimum transfer speed.
