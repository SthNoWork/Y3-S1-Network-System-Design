# Reading the generated trace

Each CSV row is one model event. Several rows may share a logical timestamp.
- step: consecutive event order, starting at 1.
- time: logical time units, not seconds or measured network delay.
- actor: sender, receiver or channel.
- event: action or observation, described below.
- sequence: DATA/ACK label 0 or 1. It is not a TCP byte number.
- payload: application text, where relevant.
- detail: explanation of that event.
- delivered_count: application messages accepted so far.

send_DATA: sender transmits a message or retry.
receive_DATA: receiver sees a DATA arrival.
deliver: receiver passes a new payload to the application.
suppress_duplicate: repeat DATA produces no new application delivery.
send_ACK / receive_ACK: acknowledgement leaves receiver / reaches sender.
accept_ACK: matching ACK permits sender advancement.
ignore_ACK: ACK does not match the outstanding message.
drop_DATA / drop_ACK: channel discards that message in this case.
delay_ACK: channel adds delay to an ACK.
timeout: matching ACK has not arrived by the sender deadline.

The nine rows in reliability-events.csv are grouped observations, not a 1:1 copy of the generated trace. Match actions by event type, sequence and payload after making your prediction. No-loss and faulted runs are synthetic models, separate from the live echo and ideal no-loss utilisation calculation.
