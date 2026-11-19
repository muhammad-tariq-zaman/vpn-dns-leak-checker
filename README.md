# vpn-dns-leak-checker

Check whether VPN-connected workstations leak DNS: the input CSV lists workstation, vpn_connected (yes/no), expected_dns and actual_dns — PROTECTED when the VPN is connected and the actual DNS server matches the expected VPN DNS server, LEAK when the VPN is connected but DNS goes elsewhere (a well-known public resolver such as 8.8.8.8 or 1.1.1.1 is called out), NOT ON VPN when the VPN is disconnected — LEAK first, then NOT ON VPN, then PROTECTED.

Sample input is included (sample.csv with four workstations).

## How to run

```sh
python3 main.py sample.csv
```

## Example output

```
WS-02: LEAK - DNS queries go to 8.8.8.8 (public resolver), expected 10.8.0.1
WS-04: LEAK - DNS queries go to 10.8.0.2, expected 10.8.0.1
WS-03: NOT ON VPN - VPN disconnected, DNS 192.168.1.1 is local
WS-01: PROTECTED - DNS 10.8.0.1 matches VPN DNS
2 leak(s), 1 not on VPN, 1 protected out of 4 workstation(s).
```

Standard library only. Run the tests with `python3 -m unittest discover`.
