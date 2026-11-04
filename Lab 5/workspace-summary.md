# Workspace Summary

## Stack & Commands
- **Runtime:** Python 3 (standard library only: `socket`, `sys`, `argparse`, `csv`, `heapq`, `itertools`, `json`)
- **Echo TCP Server:** `py echo.py tcp server`
- **Echo TCP Client:** `py echo.py tcp client "<message>"`
- **Echo UDP Server:** `py echo.py udp server`
- **Echo UDP Client:** `py echo.py udp client "<message>"`
- **Simulation Run:** `py reliable_transfer.py --case <no-loss|data-loss|ack-loss|combined-loss|delayed-ack>`
- **Simulation CSV Export:** `py reliable_transfer.py --case <case> --csv <output.csv>`
- **Simulation JSON Output:** `py reliable_transfer.py --case <case> --json`

## Architecture & Boundaries
- `.`: Single-folder lab module containing network echo baseline tools, deterministic stop-and-wait RDT simulator, trace logs, calculation models, and design worksheets.

## File Map
- `calculations.csv`: Stop-and-wait transmission delay ($T_{\text{tx}}$), cycle time, and utilization ($U$, $U\%$) for Cases A & B.
- `design-worksheet.md`: Protocol design proposals (50 MB config file & 20 Hz sensor display), pipeline sketch, and conceptual RDT Q&A.
- `echo.py`: Local loopback TCP/UDP echo client/server socket implementation.
- `event-worksheet.csv`: Step-by-step state machine transition predictions for combined-loss simulation.
- `model-parameters.csv`: Input parameters ($L$, $R$, $RTT_A$, $RTT_B$) for link utilization modeling.
- `observations.csv`: Live TCP and UDP loopback socket test measurements and verification scope.
- `READING-TRACES.md`: Reference documentation for simulator event types, columns, and trace interpretation.
- `README.md`: Lab 5 instructions, requirements, workflows, and finishing questions.
- `reliability-events.csv`: Synthetic event sequence definitions for the combined-loss scenario.
- `reliable_transfer.py`: Deterministic event-driven alternating-bit protocol (rdt) simulator and CLI harness.
- `simulation-observations.csv`: Recorded metrics (transmissions, timeouts, duplicates, ignored ACKs) across 5 simulation cases.
- `trace-clean.csv`: Generated event trace log for `no-loss` simulation.
- `trace-combined.csv`: Generated event trace log for `combined-loss` simulation.

## Symbol Index
- `reliable_transfer.py`:
  - `simulate(case: str) -> dict` [L6-54]: Runs deterministic event-driven stop-and-wait alternating-bit simulation.
  - `main() -> None` [L56-70]: Parses CLI arguments, invokes simulator, and outputs/exports trace data.

