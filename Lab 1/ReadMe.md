# Lab 1 Network Foundations and a First Design

## 1. Planning notes

| Item | Answer |
|---|---|
| Requirement 1 | Servers needs to be able to handle 60 students sessions into Moodle wirelessly |
| Requirement 2 | Students need to be able to use video meetings. |
| Requirement 3 | The printer needs to be assessible to the staff PCs via LAN network. |
| Requirement 4 | The staffs needs a connection to connect to the internet to acess Moodle and video meetings. |

**Assumptions**

1. Students needs to connect wirelessly to connect to Moodle and video calling.
2. The 5 office PCs and the printer is connected by Ethernet cable to one switch in the office (needs confirming).

**Open questions**

1. How many people use Moodle and video meetings at the same time? (unknown)
2. What are the budget, ISP speed, existing equipment and cable routes between the rooms and the office? (all unknown)

**Checkpoint (25 min): explain why one of your statements is a requirement and another is an assumption.**

Requirement 3 is a requirement because the design must satisfy it: staff need to print. Assumption 1 is only a planning guess. It is reasonable, but if the rooms turn out to have wall ports at every seat, or the laptops cannot use Wi-Fi, the design would change, so it must be confirmed. The brief also gives one constraint: use one simple LAN.

## 2. Connection observation

| Field | Observed value |
|---|---|
| OS and connection type | Windows, Wireless |
| Active interface | Wi-Fi |
| IPv4 address | 172.18.19.163 |
| Mask or prefix | 255.255.0.0 (/16) |
| Default gateway | 172.18.18.18 |
| Test time and VPN status | 4:16PM, no VPN |

## 3. Ping

| Target | Sent and replies | RTT summary |
|---|---|---|
| Loopback (127.0.0.1) | 4 sent / 4 replies | Time equal or under 1ms. Average 0ms. |
| Your gateway (172.18.18.18) | 4 sent / 4 replies | Average 1ms
| Extra: google.com | 4 sent / 4 replies | Average 65ms |

### Interpretation

**1. Explain what loopback tests and what it does not test.**

Loopback (127.0.0.1) tests the IPv4 software stack inside my own computer. It does not test the network card, the Wi-Fi or cable link, the gateway, or anything outside the computer.

**2. Does a gateway reply prove that a remote Moodle login works? Explain.**

No. A reply only shows that the gateway answered one probe on the local network. A Moodle login also depends on the ISP link, DNS, the remote server and the application itself, so it needs its own application test.

**3. State one possible reason for a missing gateway reply.**

The Wi-Fi link dropped, or I used the wrong gateway address.

**4. Explain why ping alone cannot choose the Internet capacity needed by 60 users.**

Ping measures how fast one small probe is answered, not how much traffic users create or how much download throughput is available. Capacity planning needs the number of simultaneous users and how much traffic Moodle and video meetings use per user, and both are unknown here.

## 4. Network proposal

### Topology (provisional)

```
Remote Moodle / video service
            |
      Internet / ISP
            |  (ISP link)
    Gateway router
            |  (Ethernet)
          Switch
   ____________|______________________
   |           |         |            |
  AP-1        AP-2    5 office PCs   Network printer
 (Room 1)    (Room 2)  (Ethernet)    (Ethernet)
   :           :
 Wi-Fi        Wi-Fi 
 30 laptops  30 laptops

Legend:  Ethernet = |     Wi-Fi  = ---
AP count and placement are an assumption.
The 30 + 30 split between rooms is an assumption.
```

### Paths

**Student laptop to local printer:** laptop, Wi-Fi to the room's AP, Ethernet to the switch, Ethernet to the printer. This traffic stays inside the simple LAN and does not need the gateway or the ISP.

**Student laptop to remote Moodle:** laptop, Wi-Fi to the room's AP, Ethernet to the switch, Ethernet to the gateway router, ISP link to the ISP, then the Internet to the Moodle server. This traffic needs the gateway and the ISP.

### Justify your choices

| User need | Proposed choice | Benefit and limitation |
|---|---|---|
| Students need to move around and use laptops | Wi-Fi through one AP per room | Benefit: no need ethernet or switches for internet. Limitation: many users lead to slower connections. |
| Staff needs access to printing always and Internet at fixed desks | Ethernet from the 5 PCs and the printer to the switch | Benefit: stable, fast and does not compete for Wi-Fi. Limitation: needs cable routes and fixed desk positions. |

**Assumption that would change the design:** "Student laptops connect over Wi-Fi." If the laptops cannot use Wi-Fi, or Wi-Fi is not allowed in the rooms.

**Shared failure point:** the gateway router or the ISP link. If either fails, all 60 students and all 5 staff PCs lose Internet and Moodle. The switch is also shared: if it fails, the APs, the office PCs and the printer all lose the LAN. unless all connected via wireless LAN.

## 5. Validation

| Requirement | Test | Acceptable result |
|---|---|---|
| Requirement 1 (Moodle over Wi-Fi in both rooms) | From a laptop in each room, connect to Wi-Fi, log in to Moodle and open a course page. This is an application test, not a ping. | Login succeeds, the page loads without errors, and the connection stays up for 10 minutes. |
| Requirement 3 (printing from the office) | From each of the 5 office PCs, print a test page to the network printer. | All 5 PCs print successfully and the pages come out without the PC needing Internet access. |