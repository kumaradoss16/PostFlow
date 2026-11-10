# PostFlow Security Tests

This directory contains automated negative security tests validating:
- Loopback isolation (non-loopback and wildcard bind rejection).
- Installation secret lifecycle and token isolation from frontend.
- Untrusted Origin and Host attack mitigation.
- Tauri WebView CSP and strict navigation policies.
- Secret canary scanning in logs, bundles, and database files.
