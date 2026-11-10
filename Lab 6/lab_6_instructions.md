# Lab 6: TCP Evidence and Performance Design
**SE026 Networks System Design. 2026-27**

By the end, you will read a TCP handshake, explain how a missing byte range affects cumulative ACKs, and design a file transfer test with measurable acceptance criteria.

---

## Before you start
Extract `SE026-Lab-06-Resources-2026-27.zip`. Open the CSV files in a spreadsheet or text editor. The trace and trial results are supplied teaching data. You can complete the lab without software installation, network access or a live capture.

---

## 1. Worked warm-up
A segment starts at sequence 41 and carries 4 bytes. Its byte numbers are 41, 42, 43 and 44. The last byte is $41 + 4 - 1 = 44$. If the receiver already has everything before 41, the next byte it expects is 45, so it can send ACK 45.

For any data row, calculate:
$$\text{last byte} = \text{sequence} + \text{payload bytes} - 1$$

The number immediately after that range is $\text{sequence} + \text{payload bytes}$. The receiver's ACK can stay earlier if it still has a gap.

> **Try a separate case:** A receiver expects byte 81. It receives 3 bytes beginning at 81, then receives two bytes beginning at 86 while bytes 84 and 85 are missing. Sketch the ranges and predict the next expected byte after each arrival.

---

## 2. Read the handshake
Read `SCENARIO.md` and rows 1–3 of `tcp-study.csv`. A sends data to B later, but both endpoints have their own sequence space. In a row sent by B, the sequence field belongs to B and a valid ACK field refers to A's sequence space.

Complete `handshake-worksheet.csv`. Identify each flag, who acknowledges whose SYN, and the next sequence number in each direction. A SYN uses one sequence number. The initial SYN has no valid ACK field. A pure ACK uses zero sequence numbers.

---

## The missing range

### 3. Follow A's data and B's ACKs
Treat the CSV as a timeline of modeled transmissions in both directions. For each data row, write the first and last bytes and the number after that range. Then use the scenario to track what B has actually received.

| Data row | What the scenario gives you | What to record |
| :--- | :--- | :--- |
| **4** | The first range arrives in order. | Byte range and B's next expected byte |
| **6** | This transmitted range is lost. | Byte range and why no ACK is shown for it |
| **7** | The later range arrives and B buffers it. | Byte range, gap and B's cumulative ACK |
| **9** | A sends the missing range again. | Repeated range and next expected byte |

Complete `tcp-worksheet.csv`. For each step, mark the received ranges and leave a blank where bytes are missing. Match B's ACK in rows 5, 8 and 10. In the lost row, record *no ACK shown*. A lost transmission does not add data to B's buffer.

---

### 4. Explain the recovery
- Which range does the repeated ACK point to? 
- Explain why the ACK can advance beyond the retransmitted range once it arrives. 
- State the buffering assumption that makes this possible.
- Count the duplicate ACKs actually shown. 
- Explain whether the trace identifies the retransmission trigger. 

Treat times as modeled transmission times. Avoid calculating an exact timeout or inferring a loss cause from the timestamp gap alone.

#### Partner check
Compare your row 7 predictions. One person points to the missing bytes. The other explains the difference between the byte immediately after row 7's payload and the receiver's next expected byte.

---

## Transfer time and useful throughput

### 5. Calculate an ideal lower bound
**Worked example:** A 2 MB file contains 16,000,000 bits. On an ideal $8\text{ Mb/s}$ link, transmitting those bits takes:
$$\frac{16{,}000{,}000\text{ bits}}{8{,}000{,}000\text{ bit/s}} = 2\text{ s}$$

Your case uses an 8 MB file and a $10\text{ Mb/s}$ bottleneck. Use decimal units, with $1\text{ MB} = 1{,}000{,}000\text{ bytes}$ and $1\text{ Mb/s} = 1{,}000{,}000\text{ bit/s}$. Show the conversion to bits and divide by the bottleneck bit rate. Record the ideal time in `performance-plan.csv`.

The model assumes the full bottleneck rate carries file bits continuously. Identify three reasons a measured transfer can take longer. Consider setup, protocol overhead, retransmissions, sender limits or other traffic.

---

### 6. Interpret the supplied trials
Open `sample-trials.csv`. These are fictional results for the same 8 MB file and path. The timer starts when the client begins the transfer request and stops when it finishes writing the received file. A separate hash comparison checks file identity.

For each verified trial, compute useful throughput:
$$\text{useful throughput (Mb/s)} = \frac{\text{file bytes} \times 8}{\text{elapsed seconds} \times 1{,}000{,}000}$$

Record it in `trial-analysis.csv`. Mark an invalid transfer and explain why its elapsed time cannot count as a successful transfer of the intended file.

Use the sample rule that every trial must deliver a verified copy within 9 s. Decide whether the sample run meets that rule. Explain how reporting only the fastest trial could change the conclusion.

#### Receiver and path
Describe one symptom you might investigate for a slow receiver and one for a congested path. Explain why elapsed time alone cannot tell you which limit applied.

---

## Performance test design

### 7. Write a test another team can repeat
Use `performance-plan.csv` to specify:
- File and byte count
- Source and destination
- Path
- Client count
- Exact timer start and stop

State how you would verify the received file and who would approve the target.

Propose an elapsed-time or useful-throughput target, the number of trials, and a rule for success across those trials. Specify which conditions stay fixed and what you would log. Explain how you will report a failed or incorrect transfer.

Compare your plan with another team's plan. Ask whether someone could run it without guessing the file, path or timer boundaries. Revise one ambiguous condition.

---

## Explain your findings
1. Which SYNs use sequence space, and which ACK fields confirm them?
2. Why does B's ACK stay at the gap even after later bytes arrive?
3. What does the table show about recovery, and what would you need to identify its trigger?
4. Why can an application's useful throughput be below the bottleneck bit rate?
5. How does the file verification rule affect the result of a timing test?

---

## Finish
Save your byte-range sketch, completed worksheets and performance test plan. Label the supplied trace and trial results as modeled data. Include any assumptions you used in your interpretation.