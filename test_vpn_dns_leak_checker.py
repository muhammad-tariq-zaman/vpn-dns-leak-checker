import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import unittest
from main import check

def row(workstation, connected, expected, actual):
    return {"workstation": workstation, "vpn_connected": connected,
            "expected_dns": expected, "actual_dns": actual}

class TestDnsLeakChecker(unittest.TestCase):
    def test_protected(self):
        r = check([row("WS-01", "yes", "10.8.0.1", "10.8.0.1")])
        self.assertEqual(r[0][1], "PROTECTED")

    def test_public_resolver_leak(self):
        r = check([row("WS-02", "yes", "10.8.0.1", "8.8.8.8")])
        self.assertEqual(r[0][1], "LEAK")
        self.assertIn("public resolver", r[0][2])

    def test_unexpected_resolver_leak(self):
        r = check([row("WS-04", "yes", "10.8.0.1", "10.8.0.2")])
        self.assertEqual(r[0][1], "LEAK")
        self.assertNotIn("public resolver", r[0][2])

    def test_not_on_vpn(self):
        r = check([row("WS-03", "no", "10.8.0.1", "192.168.1.1")])
        self.assertEqual(r[0][1], "NOT ON VPN")

    def test_leak_comes_first(self):
        r = check([row("WS-01", "yes", "10.8.0.1", "10.8.0.1"),
                   row("WS-02", "yes", "10.8.0.1", "8.8.8.8")])
        self.assertEqual(r[0][0], "WS-02")

    def test_empty_input(self):
        self.assertEqual(check([]), [])
