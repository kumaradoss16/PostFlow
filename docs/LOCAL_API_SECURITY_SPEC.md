# PostFlow — Local API Security Specification

**Status:** Proposed; release-blocking security contract  
**Security objective:** prevent unintended network exposure, unauthorized local API use and secret disclosure.

## 1. Threat model and trust boundaries

PostFlow runs on a user's workstation. Localhost is not a trusted boundary: other local processes, browser tabs, malicious websites, malware and same-user processes may attempt to reach the backend.

Protected assets:
- per-installation API authentication secret;
- user content and local database;
- OS-stored credentials and future provider/social tokens;
- integrity of workspace/brand operations;
- diagnostic and backup data.

Adversaries considered: remote network clients, malicious web origins, untrusted local web content, opportunistic local processes and accidental disclosure through logs/crash reports. A fully compromised Windows user account can generally access that user's processes and data; this architecture does not claim protection against local administrator/kernel compromise.

## 2. Network binding — fail closed

- Bind only to `127.0.0.1` on an OS-assigned ephemeral port.
- Reject `0.0.0.0`, `::`, `[::]`, LAN addresses, wildcard hosts and hostname-based ambiguity.
- Verify the actual socket address after binding.
- Never expose the service through Cloudflare Tunnel, reverse proxy, port forwarding, LAN discovery or public relay.
- Firewall configuration is defense in depth, not the primary access control.
- The backend must fail startup if a secure bind cannot be established.
- CORS is not authentication and must not be relied upon to protect the API.

Automated negative tests must attempt IPv4/IPv6 wildcard and non-loopback configuration and assert startup failure. Verify from another device on the same LAN that the service is unreachable.

## 3. Authentication and secret lifecycle

### 3.1 Installation secret

- Generate a cryptographically random secret with at least 256 bits of entropy using the OS CSPRNG.
- Scope one secret to one installation/profile; do not hardcode, derive from username, embed in source or ship in installer.
- Store it using Windows Credential Manager or a DPAPI-backed secure credential abstraction.
- SQLite stores only an opaque credential identifier/reference, never the value.
- React, browser storage, frontend environment variables, HTML, source maps, crash reports and normal logs must never contain the secret.
- Secret rotation must invalidate prior credentials and update the supervised backend atomically.

### 3.2 Provisioning

Rust is the credential authority. It retrieves/creates the secret and provisions it to the backend through a protected one-time bootstrap channel such as an inherited anonymous pipe. Do not pass the secret in command-line arguments, URL query strings, persistent environment variables, files or standard output.

The backend receives the secret in process memory and must:
- keep it only for process lifetime;
- compare authentication tokens in constant time;
- reject missing, malformed or invalid credentials;
- avoid logging request headers;
- clear references on shutdown where practical.

The React frontend never receives the secret. Rust attaches it to fixed, allowlisted backend requests.

### 3.3 Authentication protocol

Use a dedicated header such as `X-PostFlow-Local-Auth`; reject credentials in query strings, cookies or request bodies. Require authentication on every HTTP endpoint, including health and operational status. The process-readiness handshake occurs over the protected bootstrap pipe, not an unauthenticated HTTP endpoint. If an unauthenticated liveness endpoint is ever proposed, it requires a documented threat review and must disclose no state beyond a fixed liveness response.

Rotate the installation secret on explicit security reset, credential-store loss/recreation or suspected compromise. If secure storage is unavailable, fail closed; do not fall back to plaintext.

## 4. Origin, Host and browser protections

- Validate `Host` against the exact loopback address and selected port.
- For browser-originated requests, allow only the exact Tauri application origin(s) required by the packaged runtime; reject `null`, arbitrary `http://localhost`, arbitrary ports, `file://` and untrusted web origins unless a documented Tauri runtime requires a specific exception.
- Rust proxy requests are the only supported production frontend path.
- Production browser-originated HTTP calls to the local API are unsupported; the React WebView must use typed Tauri IPC only.
- Configure a restrictive Tauri v2-compatible Content Security Policy: no remote scripts, no `unsafe-eval`, and no broad `connect-src` or wildcard sources. Deny untrusted top-level navigation and unapproved new windows; external links must open through an explicit native allowlisted action.
- Disable or restrict production developer tools and remote debugging according to the Tauri release configuration.
- Disable permissive CORS (`*`) and credentialed cross-origin access.
- Validate `Origin` and `Sec-Fetch-Site` where available, but do not treat them as authentication.
- Reject DNS rebinding patterns and unexpected hostnames by validating numeric socket destination and Host.
- No backend endpoint may mutate state through GET.

## 5. Request hardening

- Enforce request body size limits per route; initial default 1 MiB for JSON control requests, with explicit smaller limits for simple commands.
- Enforce connection, read and application timeouts.
- Apply per-process request concurrency limits and bounded queues.
- Rate-limit authentication failures and expensive operations.
- Validate content type, schema, string lengths, enum values and UUID formats.
- Reject unknown fields for security-sensitive DTOs where practical.
- Use parameterized SQL exclusively through SQLAlchemy.
- Return generic authentication errors; do not reveal whether a credential identifier or account exists.
- Do not expose stack traces, absolute paths, SQL statements or internal exception text to the UI.

## 6. IPC/proxy authorization

Rust exposes named, typed commands, not arbitrary HTTP forwarding. Each command has:
- explicit DTO schema and maximum payload size;
- fixed HTTP method and backend route;
- allowed response DTO;
- authorization and rate-limit policy;
- test for invalid arguments and backend failure.

No frontend-provided URL, header, method, credential reference or arbitrary proxy path is accepted. Tauri capabilities and plugin permissions follow least privilege; deny shell, filesystem and HTTP permissions unless required and reviewed.

## 7. Logging, diagnostics and data handling

Redact at source:
- installation secret and auth headers;
- API keys, OAuth access/refresh tokens and client secrets;
- passwords, authorization codes and PKCE verifiers;
- sensitive content payloads and personal data unless explicitly required.

Logs use structured fields and correlation IDs. Diagnostic bundles are opt-in, bounded, previewable and redacted. Backups must not contain credential values; credential restoration is handled separately through the OS store or reauthorization. Never upload diagnostics automatically.

## 8. Future OAuth/AI credential rule

M1 does not implement provider or social credentials. When later approved:
- use system browser and PKCE for public/native clients where supported;
- never embed a confidential client secret in the desktop binary;
- keep access/refresh tokens in OS-backed storage;
- use least-privilege scopes;
- protect state/nonce and callback handling;
- do not expose tokens to React;
- obtain explicit consent before external data transmission.

If a provider requires confidential client authentication, defer integration or approve a separately operated broker with its own threat model. Do not silently introduce one.

## 9. Security verification matrix

| Control | Required negative/positive evidence |
|---|---|
| Loopback-only | Wildcard/LAN bind attempts fail; LAN probe cannot connect |
| Authentication | Missing, malformed and wrong secret return generic 401/403 |
| Secret isolation | Secret absent from bundle, React runtime, SQLite, args, env, logs |
| Origin/Host | Untrusted browser Origin, null origin and Host mismatch rejected; Rust-native proxy follows the documented no-Origin contract |
| WebView boundary | CSP blocks remote script/connect sources; untrusted navigation and new windows are denied |
| Proxy allowlist | Arbitrary URL/method/header forwarding impossible |
| Input limits | Oversized body and malformed DTO rejected before business logic |
| Rate limits | Repeated failures are bounded and logged safely |
| Error handling | No stack traces, paths, SQL or secrets in response |
| Shutdown | Backend no longer accepts requests after stop |
| Secure storage failure | App fails closed; no plaintext fallback |

## 10. Residual risk and limits

A local installation secret is not a defense against malware running as the same Windows user with sufficient process inspection/injection capability. The objective is to prevent accidental exposure, browser-origin abuse, network access and casual local API invocation. Document this limitation. A future SaaS service requires a wholly separate identity, session, authorization and tenant-isolation model.