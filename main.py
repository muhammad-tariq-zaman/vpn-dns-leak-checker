"""Check whether VPN-connected workstations leak DNS.

Usage: python3 main.py dns.csv
CSV columns: workstation,vpn_connected,expected_dns,actual_dns.
vpn_connected is yes or no. Verdicts:
- PROTECTED: VPN connected and the actual DNS server matches
  the expected VPN DNS server.
- LEAK: VPN connected but DNS goes elsewhere; a well-known
  public resolver (8.8.8.8, 8.8.4.4, 1.1.1.1, 9.9.9.9,
  208.67.222.222) is called out as a public resolver.
- NOT ON VPN: VPN disconnected, so DNS is local by design.
LEAK first, then NOT ON VPN, then PROTECTED; within a verdict
by workstation.
"""
import argparse, csv, sys

PUBLIC_RESOLVERS = {"8.8.8.8", "8.8.4.4", "1.1.1.1", "9.9.9.9", "208.67.222.222"}
VERDICT_ORDER = {"LEAK": 0, "NOT ON VPN": 1, "PROTECTED": 2}

def check(rows):
    out = []
    for row in rows:
        workstation = row["workstation"].strip()
        connected = row["vpn_connected"].strip().lower() == "yes"
        expected = row["expected_dns"].strip()
        actual = row["actual_dns"].strip()
        if not connected:
            verdict = "NOT ON VPN"
            detail = f"VPN disconnected, DNS {actual} is local"
        elif actual == expected:
            verdict = "PROTECTED"
            detail = f"DNS {actual} matches VPN DNS"
        else:
            verdict = "LEAK"
            if actual in PUBLIC_RESOLVERS:
                detail = (f"DNS queries go to {actual} (public resolver), "
                          f"expected {expected}")
            else:
                detail = f"DNS queries go to {actual}, expected {expected}"
        out.append((workstation, verdict, detail))
    return sorted(out, key=lambda r: (VERDICT_ORDER[r[1]], r[0]))

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path")
    args = parser.parse_args(argv)
    with open(args.path, newline="", encoding="utf-8") as f:
        results = check(list(csv.DictReader(f)))
    for workstation, verdict, detail in results:
        print(f"{workstation}: {verdict} - {detail}")
    counts = {v: sum(1 for _, verdict, _ in results if verdict == v)
              for v in ("LEAK", "NOT ON VPN", "PROTECTED")}
    print(f"{counts['LEAK']} leak(s), {counts['NOT ON VPN']} not on VPN, "
          f"{counts['PROTECTED']} protected out of {len(results)} workstation(s).")
    return 0

if __name__ == "__main__":
    sys.exit(main())
