# Transport design worksheet

## Case 1: Configuration file
Requirement: intended 50 MB file, authorised staff, interruption may occur.
Protocol choice and reason:
- Protocol: HTTPS / SFTP (application layer) over TCP (transport layer) with TLS encryption.
- Reason: TCP provides guaranteed in-order byte stream delivery, checksum error detection, flow control, and retransmission over lossy channels, ensuring no byte of the 50 MB configuration is silently corrupted or omitted.

How to identify the intended version and complete content:
- Version identity: Explicit version string and metadata header (e.g., `v2.4.1`, timestamp, target environment ID).
- Complete content vs partial: Provide the exact file byte size in the metadata header and append a cryptographic digest (e.g., SHA-256). The client stages the incoming payload in a temporary file (`.part`) and only verifies/commits it to active status once the final byte count and SHA-256 match.

Access protection and interruption/retry policy:
- Access protection: Mutual TLS (mTLS) or OAuth 2.0 Bearer tokens over TLS so only authenticated and authorized staff can initiate downloads.
- Interruption / retry policy: Support HTTP Range requests (`Range: bytes=offset-`) or chunk-based resumable transfers. On connection drops, the client performs exponential backoff and resumes from the last confirmed byte offset rather than restarting the entire 50 MB download.

One proposed test and observable success condition:
- Proposed test: Initiate a 50 MB configuration download over an emulated WAN link and sever the TCP connection at 25 MB.
- Observable success condition: The client detects socket disconnection, reconnects with `Range: bytes=26214400-`, receives the remaining 25 MB, computes the full SHA-256 hash matching the origin, and promotes the file into service.

---

## Case 2: Sensor display
Requirement: 20 updates/s, no reading older than 200 ms used, occasional gaps acceptable.
Protocol choice and reason:
- Protocol: UDP (transport layer) with custom lightweight application framing (or QUIC Datagrams).
- Reason: UDP avoids head-of-line blocking and retransmission delays inherent to TCP. For real-time telemetry, a dropped reading is superseded by the next incoming reading 50 ms later; retransmitting stale data wastes bandwidth and introduces latency.

Message identity, duplicate/stale handling and age-measurement assumption:
- Message identity: 64-bit monotonically increasing sequence number, sensor ID, and high-precision UTC millisecond timestamp ($T_{\text{send}}$).
- Duplicate / stale handling: The receiver maintains $Seq_{\text{max}}$. Any incoming packet with $Seq \le Seq_{\text{max}}$ is discarded as duplicate/reordered. The receiver computes latency $\Delta = T_{\text{receive}} - T_{\text{send}}$. If $\Delta > 200\text{ ms}$, the packet is dropped as stale.
- Age-measurement assumption: Sender and receiver clocks are tightly synchronized (e.g., via local PTP or NTP with jitter $< 10\text{ ms}$).

Congestion response and suitable security assumption:
- Congestion response: Receiver sends periodic coarse rate-feedback or RTCP-like telemetry (e.g., every 1 second). If loss rate exceeds a threshold (e.g., > 10%), sender dynamically throttles transmission rate (e.g., downsamples to 10 Hz or 5 Hz) to alleviate buffer bloat.
- Security assumption: Payloads include an HMAC (e.g., HMAC-SHA256) keyed with a pre-shared secret to authenticate sensor identity and prevent spoofing or tampering.

One proposed test and observable success condition:
- Proposed test: Stream 20 updates/s while injecting 15% random packet drops and occasional artificial delays spikes of 250 ms.
- Observable success condition: The dashboard display updates smoothly without freezing, logs show all packets with age > 200 ms are dropped without rendering, and zero stale readings ever overwrite newer readings.

---

## Section 8: Pipelined Transport Sketch

```text
Sender                                     Receiver
  |                                           |
  |--- DATA0 (ALPHA) ------------------------>| (Sent, unacknowledged)
  |                                           |
  |--- DATA1 (BETA)  ------------------------>| (Sent, unacknowledged)
  |                                           |
  |--- DATA2 (GAMMA) ------------------------>| (Sent, unacknowledged)
  |                                           |
  |<-- ACK0 ----------------------------------| (First ACK returns)
  |                                           |
  |--- DATA3 (DELTA) ------------------------>| (Window slides forward)
  |                                           |
  |<-- ACK1 ----------------------------------|
  |<-- ACK2 ----------------------------------|
  v                                           v
Time                                        Time
```

### Analysis
- **Idle time reduction:** In stop-and-wait, the sender must sit idle for an entire RTT after transmitting a single packet. Pipelining allows multiple packets (a window of size $N$) to be transmitted back-to-back, keeping the link continuously utilized and increasing effective throughput by up to a factor of $N$.
- **Sequence number range:** In stop-and-wait, a 1-bit sequence number (0 and 1) suffices. In pipelined protocols (such as Go-Back-N or Selective Repeat), sequence numbers must uniquely distinguish new packets from old duplicates across the maximum window size. For Selective Repeat with window size $N$, the sequence space must be at least $2N$.
- **Buffering requirements:** The sender must buffer all unacknowledged packets to allow retransmission if an ACK is lost or a timeout occurs. For Selective Repeat, the receiver must also buffer out-of-order packets until missing predecessor packets arrive to maintain in-order application delivery.

---

## Explain and Finish (Conceptual Q&A)

### 1. Why can the sender time out after the receiver delivered DATA?
The receiver delivers the payload immediately upon receiving the expected DATA packet and then dispatches an ACK. If that ACK packet is dropped, delayed, or corrupted in the reverse channel, the sender's timer expires without having received confirmation, triggering a timeout and retransmission despite successful delivery at the receiver.

### 2. Why acknowledge a duplicate without delivering it again?
If the receiver receives a duplicate DATA packet (e.g. because the previous ACK was dropped or delayed), the sender is still blocked waiting for confirmation of that sequence number. The receiver must re-send the ACK to allow the sender to advance its window, while suppressing duplicate delivery to prevent corrupting application data.

### 3. How do the receiver's expected label and sender's waiting state differ?
- **Sender's waiting state:** Identifies the specific sequence number label of the single packet currently in flight that the sender needs confirmed before it is permitted to advance to the next message.
- **Receiver's expected label:** Identifies the next sequence number label that the receiver will accept as new data for application delivery. The sender's state trails the receiver's state whenever a packet is delivered but the corresponding ACK is still in transit.

### 4. What assumptions make your utilisation calculation valid?
- Ideal error-free channel with zero packet or ACK loss.
- ACK packet transmission time and endpoint processing delays are negligible compared to propagation delay.
- Symmetrical round-trip propagation time ($RTT = 2 \times T_{\text{prop}}$).
- Fixed packet length $L$ and constant link transmission rate $R$.
- Strictly one packet outstanding at any time (pure stop-and-wait).

### 5. Why does an echo reply not prove a complete authorised file transfer?
An echo reply only confirms basic round-trip reachability and byte reflection on a local loopback socket. It does not verify authentication, authorization, end-to-end file integrity (hash verification), partial-transfer recovery/resumption, persistent disk storage, version tracking, or resilience across lossy, congested, or reordering wide-area network paths.
