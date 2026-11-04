# SE026 Lab 5: Reliable Transfer and Transport Design

## Objectives
Trace how acknowledgements, sequence labels and timers handle loss; calculate ideal stop-and-wait utilisation; and choose transport behavior for two application requirements.
## 1. Prepare the resources
Extract SE026-Lab-05-Resources-2026-27.zip and open SE026-Lab-05-Resources. Use Python 3, a calculator and a text editor or spreadsheet. No extra Python packages are required.
Keep these files together: echo.py, reliable_transfer.py, reliability-events.csv, event-worksheet.csv, model-parameters.csv, calculations.csv, simulation-observations.csv, observations.csv, design-worksheet.md and READING-TRACES.md.
On Windows, click the File Explorer address bar, type cmd and press Enter. Run dir and py --version. Use python if py is absent but python works. On macOS/Linux use a terminal in the extracted folder and replace py in the commands below with python3.
## 2. Check the local TCP/UDP baseline
Open terminals A and B in this folder. Start TCP in A:
```cmd
py echo.py tcp server
```
Send one message from B:
```cmd
py echo.py tcp client "design test"
```
Record the endpoint and reply fields in observations.csv. Stop A with Ctrl+C. Then start UDP in A:
```cmd
py echo.py udp server
```
Send from B, then stop A after the reply:
```cmd
py echo.py udp client "design test"
```
Both servers bind to loopback port 12000. If it is busy, stop only your own earlier echo instance or record that the baseline is blocked. These successful local messages do not measure path-wide loss or demonstrate the simulator.


## 3. Understand the model before adding faults
rdt means reliable data transfer. This finite simulator uses an alternating-bit stop-and-wait model: ALPHA is the first payload and BETA the second. DATA0/DATA1 label whole messages; ACK0/ACK1 acknowledge those labels. These are not TCP byte numbers.
Sender: keep one DATA outstanding and start a timer. A matching ACK permits the next message and label. Timeout repeats the same label and payload. A wrong-label ACK does not advance the sender.
Receiver: initially expect 0. Accept an expected label, deliver once, send its ACK and switch expectation. A duplicate old label gets another ACK without another application delivery.
A clean one-message example uses the payload HELLO:
Clean example: send DATA0 carrying HELLO; receiver delivers HELLO once and expects 1; matching ACK0 permits sender to advance to DATA1.
Now run the clean model and read the events from top to bottom:
```cmd
py reliable_transfer.py --case no-loss --csv trace-clean.csv
```
Fill the no-loss row of simulation-observations.csv. Identify a send_DATA, deliver and accept_ACK event. More than one event can share a logical timestamp because local processing actions take no modeled travel time.
## 4. Predict before running combined loss
Open reliability-events.csv and event-worksheet.csv. Start with sender ready for DATA0, receiver expecting 0 and zero deliveries. The first DATA0 is lost; later the first ACK0 is lost too.
For each numbered input row, write the state AFTER that row. Use simple words such as waiting for ACK0, expects 1, no new delivery, or ready for the next message. For each DATA arrival, decide whether its payload is new or a duplicate, then update the total deliveries.
The input describes events visible to an outside observer. A waiting sender cannot know an ACK was lost; it only knows its matching ACK has not arrived. Do not advance it just because the receiver delivered DATA.


## 5. Run the combined-loss case
After completing the prediction, run:
```cmd
py reliable_transfer.py --case combined-loss --csv trace-combined.csv
```
Open the generated CSV beside your prediction. The nine input rows group events; the simulator logs each send, arrival and local action separately. Their row counts will differ. Match by label, payload and event name rather than row number.
Use READING-TRACES.md for the full field guide. The step column gives event order; time is a logical timestamp, not seconds. actor identifies sender, receiver or channel. sequence labels the DATA/ACK, and delivered_count counts accepted application messages so far.
Read these event groups as one story: send_DATA then receive_DATA then deliver; send_ACK then receive_ACK then accept_ACK. drop_DATA/drop_ACK record channel loss. timeout triggers retry. suppress_duplicate means the application list stays unchanged. ignore_ACK means a stale or wrong-label ACK did not advance the sender.
Compare your prediction to the observed trace and explain differences in your own words. If an output filename exists, choose a new filename; earlier traces are preserved.
## 6. Change one fault at a time
The clean and combined cases are already recorded. Run the remaining cases and complete the other rows of simulation-observations.csv:
```cmd
py reliable_transfer.py --case data-loss
py reliable_transfer.py --case ack-loss
py reliable_transfer.py --case delayed-ack
```
Use the printed summary for DATA transmissions, timeouts, duplicate DATA and ignored ACKs. Use the trace to identify the first application delivery, retries and any old ACK. Compare the final delivered-message list across all five cases.
Explain how an ACK can be lost or late after DATA was already delivered. In an ACK-loss case, separate the number of transmissions from the number of application deliveries.
This simulator sends no packets. Its logical times are not measured network delay, and it omits corruption and general reordering/restart behavior. The lecture's rdt2.x corruption examples are conceptual; these runs focus on loss, delay and duplicates.


## 7. Calculate ideal stop-and-wait utilisation
Open model-parameters.csv and calculations.csv. Packet length L = 8,000 bits; rate R = 10,000,000 bit/s. Case A uses 0.040 s round-trip propagation, and B uses 0.004 s. L is already in bits.
Use a no-loss model with one outstanding packet and negligible ACK transmission/processing. Here RTT excludes DATA transmission.
Work one step at a time:
1. Sending time: Ttx = L/R = ___ seconds. Convert to milliseconds as a check.
2. Cycle: add Ttx and the supplied RTT for each case, in the same unit.
3. Busy fraction: U = Ttx / cycle.
4. Busy percentage: U_percent = 100 x U.
A separate example shows the method: if sending takes 2 ms and propagation RTT is 18 ms, the cycle is 20 ms. U = 2/20 = 0.10, which is 10%. This example uses different inputs from your worksheet.
Keep several decimal places until the final percentage. A fraction must lie between 0 and 1; a percentage between 0 and 100. Explain which case leaves the sender waiting longer.
Use the supplied propagation times, not the simulator's logical timer or completion time. These are separate analyses.
## 8. Sketch a pipeline
Draw two endpoints and time moving downward. Show three different DATA packets leaving before the first ACK returns. Label which messages are sent but not yet acknowledged.
Explain why this can reduce idle time. State why a larger sequence range and buffering are needed. Keep this a sketch; the supplied one-bit simulator remains stop-and-wait.


## 9. Make two short design recommendations
Use design-worksheet.md. Each case needs a justified protocol choice, a definition of success/failure handling and one proposed test. You do not need to build either application.
Configuration file: deliver the intended 50 MB file to authorised staff. The connection can fail halfway through. Explain how to identify the intended version, distinguish complete from partial content, protect access and handle interruption. State what a test should observe to count as success.
Sensor display: 20 updates per second; readings older than 200 ms must not drive the display, and occasional missed readings are acceptable. Explain message identity and stale/duplicate handling. State an assumption for measuring age; comparing sender timestamps with receiver time requires a suitable shared-clock assumption. Include how sending should respond to congestion, then propose one observable test.
TCP supplies ordered reliable bytes while its connection operates. UDP alone supplies neither delivery nor congestion control. The application still needs completion/failure rules and suitable security. An established protocol above either transport may fit if justified.
## Explain and finish
1. Why can the sender time out after the receiver delivered DATA?
2. Why acknowledge a duplicate without delivering it again?
3. How do the receiver's expected label and sender's waiting state differ?
4. What assumptions make your utilisation calculation valid?
5. Why does an echo reply not prove a complete authorised file transfer?
Save your prediction, model observations, calculations, pipeline sketch and recommendations. Distinguish live echo evidence, simulated events and proposed designs. Stop your own echo server if still running.
## If a step fails
File not found: check extraction and current folder. Unknown case: run py reliable_transfer.py --help. Existing trace: choose a new filename. Odd spreadsheet display: import CSV as comma-separated UTF-8 or read it in a text editor. Record actual errors instead of filling in an invented result.

