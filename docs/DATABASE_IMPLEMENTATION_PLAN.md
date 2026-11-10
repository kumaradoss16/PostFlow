# PostFlow — Database Implementation Plan

**Status:** Proposed M1 persistence contract  
**Database:** SQLite | **ORM:** SQLAlchemy 2.x | **Migrations:** Alembic

## 1. Objectives and scope

M1 establishes durable, versioned local persistence without introducing a database server. SQLite is the structured-data source of truth; binary media remains on the filesystem.

M1 schema scope is intentionally small:
- local application profile/installation metadata, excluding secret values;
- workspace;
- brand;
- non-secret application settings;
- migration metadata and any required audit metadata.

Do not create campaign, social account, OAuth, content publishing, analytics or team-membership tables in M1 merely because they appear in legacy schema drafts. Add them only in the milestone that implements and tests the corresponding domain capability.

## 2. Technology and access model

- SQLite database in the per-user Tauri application data directory.
- SQLAlchemy 2.x typed declarative models.
- Alembic versioned migrations.
- Use synchronous SQLAlchemy sessions initially unless an approved measured requirement justifies async database I/O. FastAPI can execute bounded synchronous DB work in its worker threadpool. Avoid `aiosqlite` complexity without a demonstrated need.
- One engine per backend process; short-lived session per request/use case.
- SQLite connection pool configured explicitly. For a single local process, use a bounded pool compatible with the chosen SQLAlchemy/SQLite threading model; document the selected `QueuePool`/`NullPool` behavior and test it. Do not assume server-database pool defaults are appropriate.
- No database access from React or Rust.

## 3. SQLite connection configuration

Every connection must apply and verify:
```sql
PRAGMA foreign_keys = ON;
PRAGMA busy_timeout = 5000;
```

Database initialization must set and verify:
```sql
PRAGMA journal_mode = WAL;
PRAGMA synchronous = NORMAL;
```

`NORMAL` is an initial performance/durability trade-off, not an absolute power-loss guarantee. Reassess `FULL` if user data criticality or measured workload warrants it. WAL mode requires all readers/writers to use the same database directory and should be checkpointed deliberately.

Rules:
- Set a finite connection timeout and `busy_timeout`.
- Enable foreign keys on every connection, not only once at startup.
- Use short transactions; never hold a write transaction during network, AI or media processing.
- Use atomic conditional updates for any future job-claiming logic.
- Do not share a SQLAlchemy Session across threads or requests.
- Do not copy only the `.db` file while WAL is active.
- Handle `SQLITE_BUSY`, disk-full, permission and corruption errors as explicit operational states.

## 4. Schema conventions

- UUID primary keys serialized as lowercase hyphenated text.
- UTC, timezone-aware timestamps; reject naive datetime input.
- Explicit created/updated timestamps.
- Stable snake_case table/column names.
- Explicit FK names, unique constraints, check constraints and indexes.
- `ON DELETE` behavior must be deliberate and tested; do not cascade-delete user data by accident.
- Boolean values use SQLite integer representation through SQLAlchemy.
- JSON is stored as text only after schema validation; do not use JSON as a substitute for relational constraints.
- Avoid floating point for money or exact usage values.
- Use optimistic concurrency/version columns where concurrent edits could overwrite data.
- Workspace-owned records must include workspace ID and enforce scoped access in service/repository layer; database uniqueness should include workspace scope where applicable.

## 5. Data validation and transaction boundaries

Validation layers:
1. Pydantic request DTO validates shape, type, length and allowed values.
2. Domain/service layer validates business invariants and ownership.
3. Database constraints enforce uniqueness, non-nullability, foreign keys and basic invariants.
4. Repository translates expected integrity failures into stable application errors.

Do not rely solely on frontend validation. Do not expose raw SQLite exception messages to users.

Transactions:
- one use-case transaction per logical mutation;
- commit only after all related rows are consistent;
- rollback on any exception;
- no external API call inside a DB transaction;
- use explicit transaction boundaries in service layer;
- test rollback and concurrent update behavior.

## 6. Alembic migration workflow

1. Model change is reviewed with domain and data-lifecycle impact.
2. Generate a candidate migration with Alembic autogenerate.
3. Manually inspect generated operations; autogenerate is not authoritative.
4. Add upgrade and downgrade logic where safe; if downgrade is destructive or unsupported, document why and provide backup/restore recovery.
5. Run migration against an empty database.
6. Run migration against a fixture from the previous released schema with representative populated data.
7. Verify row counts, FK integrity, indexes, uniqueness and application compatibility.
8. Run tests with migration failure injected.
9. Commit model and migration together.
10. On app startup, migration runs before readiness; failure prevents the app from declaring healthy.

Never edit an already released migration. Never use `create_all()` as the production schema migration mechanism. `create_all()` may be used only in isolated tests where migration behavior is not under test.

## 7. Backup and restore

Backup must use SQLite's online backup API or another proven SQLite-consistent method. Do not copy a live WAL database file as a normal filesystem copy.

Backup package should include:
- database snapshot;
- schema/application compatibility metadata;
- creation timestamp;
- integrity/checksum metadata;
- optional media manifest only if media backup is explicitly in scope.

No credentials or secret values are included. The backup is not a complete account credential recovery mechanism.

Restore workflow:
1. show source, target and compatibility;
2. require explicit user confirmation;
3. create a pre-restore backup;
4. restore to a temporary path;
5. run `PRAGMA integrity_check` and `foreign_key_check`;
6. verify expected schema version and required tables;
7. atomically replace active database only after validation;
8. reopen engine and verify application-level reads;
9. retain recovery path if activation fails.

M1 must test backup while WAL has uncheckpointed writes and restore into a clean profile.

## 8. Deletion and filesystem semantics

M1 has no media library, but define the rule before adding file references: database and filesystem deletion are not one atomic transaction. Use staged deletion/cleanup records or a recoverable two-phase operation; never delete a file first and then assume the DB commit succeeded. No recursive deletion based on untrusted paths.

## 9. Required tests

- fresh database migration from base to head;
- populated previous-version upgrade;
- migration failure leaves app unavailable and recoverable;
- foreign keys enforced on each connection;
- WAL and busy timeout verified;
- concurrent reads and bounded writes;
- transaction rollback on service failure;
- uniqueness and invalid ownership rejected;
- stale update conflict detected where versioning is used;
- backup consistency during WAL writes;
- restore integrity and FK checks;
- corrupted/incompatible backup rejected without replacing live DB;
- restart persistence;
- disk-full/permission failure returns safe error;
- no secret values in database or backup.

## 10. M1 acceptance boundary

M1 does not claim to implement the full PostFlow data model. It proves the persistence foundation and minimal workspace/brand slice. Every later domain milestone must introduce its own models, migration, constraints, data-retention rules and migration tests.