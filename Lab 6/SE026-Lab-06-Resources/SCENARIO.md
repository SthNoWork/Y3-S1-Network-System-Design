# Modeled TCP exchange

A and B use absolute sequence numbers. Each direction has its own sequence space. The ACK field in row 1 is 0 in the CSV and has no meaning because the ACK flag is clear. SYN and SYN_ACK rows have no payload here. SYN consumes one sequence number. A pure ACK consumes zero.

The table lists modeled sends in both directions. Row 4 arrives at B. Row 6 is transmitted but lost before reaching B. Row 7 arrives and B buffers it. Row 9 retransmits the missing payload and arrives at B. Rows 5, 8 and 10 are ACK transmissions from B. Assume each listed data ACK reaches A. A's data segments also carry an ACK for B's sequence space.

The times provide event order. The model leaves the cause of loss and the retransmission trigger unspecified. There is one duplicate ACK shown. Keep the worksheet's number after a segment separate from B's next expected byte when a gap exists.
