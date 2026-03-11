---
name: hard-cut
description: "Enforce a hard-cut product policy: keep one canonical current-state implementation and delete compatibility, migration, fallback, adapter, and dual-behavior code unless the user explicitly asks for transition support. Use when a task changes product behavior, persisted state, startup recovery, routing, contracts, configuration, schema or enum shapes, feature flags, or architecture where old-state compatibility might otherwise be preserved."
---

# Hard-Cut Policy

## Overview

Apply a hard-cut policy as the default decision filter for product and architecture changes. Keep one current-state codepath, fail fast on invalid old state, and prefer explicit recovery steps over compatibility logic.

## Operating Rules

- Treat historical local state as non-authoritative unless the user explicitly requests migration or compatibility support.
- Delete compatibility bridges, fallback paths, dual reads/writes, adapter layers, old enum aliases, legacy route parsing, and silent coercions when touching the primary codepath.
- Update contracts, validation, flags, constants, and configuration in one canonical location. Do not preserve parallel policy logic.
- Fail fast when persisted state, inputs, or contracts do not match the canonical format.
- Prefer explicit operator or user recovery steps over automatic migration.
- If a change makes old local state invalid, surface that clearly and keep the canonical implementation clean.

## Decision Test

1. Ask whether there is a real external-user compatibility requirement.
2. If not, remove the old path and keep only the canonical current-state behavior.
3. If yes because the user explicitly asked for transition support, keep it narrow and temporary.
4. In the same diff, state why the compatibility code exists, why the canonical path is insufficient, the exact deletion criteria, and the tracking ADR or task.

## Review Checklist

- Remove dead migration and fallback code once the canonical path exists.
- Collapse duplicated validation or policy logic into one source of truth.
- Replace silent fallback with an explicit error, assertion, or recovery instruction.
- Prefer invalid-state diagnostics over best-effort parsing or coercion.
- Call out any unavoidable temporary compatibility code in the final summary or PR body.
