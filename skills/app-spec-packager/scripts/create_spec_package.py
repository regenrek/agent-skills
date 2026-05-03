#!/usr/bin/env python3
"""Scaffold a production application spec package.

This script creates a Markdown folder with the standard files used by the
app-spec-packager skill. It intentionally creates structured placeholders;
the agent should fill them with app-specific content.
"""

from __future__ import annotations

import argparse
import re
import shutil
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path

BASE_FILES: dict[str, str] = {
    "README.md": """# {app_name} Specification Package

Generated: {generated_at}
Platforms: {platforms}

## Purpose

This package specifies {app_name} as a production-ready application for coding agents.

## Package contents

- PRODUCT_SPEC.md: product definition, scope, requirements, monetization, and non-goals.
- UX_FLOWS.md: navigation, screen map, state machine, and user journeys.
- DESIGN_SYSTEM_SPEC.md: visual direction, components, accessibility, and platform UI rules.
- TECH_ARCHITECTURE.md: system architecture, data flows, deployment, failure modes.
- ADRS.md: major architecture decisions and alternatives.
- SAFETY_PRIVACY_SECURITY.md: data inventory, security controls, privacy, safety boundaries.
- API_AND_DATA_MODEL.md: API contracts, models, storage, retention, and migrations.
- CLIENT_IMPLEMENTATION_SPEC.md: client implementation requirements.
- ANALYTICS_OBSERVABILITY_SPEC.md: analytics, monitoring, logs, alerts, and cost tracking.
- QA_ACCEPTANCE_TESTS.md: test strategy and acceptance matrix.
- RELEASE_READINESS.md: deployment/app-store/release checklist.
- TASKS.md: executable build tasks for coding agents.

## Global assumptions

- [Fill with app-specific assumptions.]

## Global non-goals

- [Fill with explicit non-goals.]

## Critical invariants

- [Fill with constraints coding agents must never violate.]
""",
    "PRODUCT_SPEC.md": """# Product Specification

## Vision

## Product promise

## Target users

## Problems solved

## Product principles

## V1 scope

## Explicit non-goals

## User personas

## Core objects and vocabulary

## Core user journeys

## Feature requirements

### Feature 1

- REQ-PROD-001: [Testable requirement.]

## Plans, tiers, and monetization

## Integrations

## Content, moderation, and safety boundaries

## Success metrics

## Analytics constraints

## Open decisions
""",
    "UX_FLOWS.md": """# UX Flows

## Navigation model

## Screen map

## State machine

```text
STATE_A -> STATE_B
Trigger:
Guard:
Side effects:
Failure behavior:
```

## Onboarding flow

## Primary creation/setup flow

## Home/dashboard states

## Detail states

## Error, empty, offline, and loading states

## Paywall and entitlement states

## Settings, export, delete, and account flows

## Accessibility behavior

## Localization behavior

## Acceptance criteria
""",
    "DESIGN_SYSTEM_SPEC.md": """# Design System Specification

## Design principles

## Brand tone

## Visual direction

## Color system

## Typography

## Spacing and layout

## Component system

## Motion and haptics

## Iconography and illustration

## Data visualization rules

## Accessibility requirements

## Platform-specific UI conventions

## Do not do
""",
    "TECH_ARCHITECTURE.md": """# Technical Architecture

## Architecture goals

## System context diagram

```text
Client
  -> Backend/API
  -> Database
  -> Third-party providers
```

## Client architecture

## Backend architecture

## Data architecture

## AI architecture

## Auth and identity

## Payment/subscription architecture

## Integrations

## Security architecture

## Privacy architecture

## Observability

## Deployment environments

## Failure modes and fallback behavior

## Scalability assumptions

## Open technical decisions
""",
    "ADRS.md": """# Architecture Decision Records

## ADR-001: [Decision title]

Status: Proposed

### Context

### Decision

### Alternatives considered

### Consequences

### Risks

### Follow-up tasks
""",
    "SAFETY_PRIVACY_SECURITY.md": """# Safety, Privacy, and Security

## Data inventory

| Data item | Classification | Stored where | Sent to | Retention | Delete/export | Analytics/logging |
|---|---|---|---|---|---|---|
| [Example] | [PUBLIC/INTERNAL/PERSONAL/SENSITIVE/SECRET] | [Location] | [Provider] | [Window] | [Behavior] | [Allowed?] |

## Data classification

## Local data

## Server data

## Third-party/provider data

## Analytics data

## Consent and disclosure requirements

## Retention policy

## Export and deletion policy

## Logging policy

## Security controls

## Abuse prevention

## Safety risk taxonomy

## Crisis/escalation behavior if relevant

## Compliance notes

## Legal/platform review checklist
""",
    "API_AND_DATA_MODEL.md": """# API and Data Model

## API principles

## Authentication and authorization

## Endpoint summary

| Method | Path | Purpose | Auth | Rate limit |
|---|---|---|---|---|

## Endpoint definitions

### POST /v1/example

Request:

```json
{}
```

Response:

```json
{}
```

Errors:

Rate limits:

Idempotency:

Security notes:

## Client data models

## Server data models

## Provider data models

## Database schema

## State transitions

## Migrations

## Retention and deletion behavior
""",
    "CLIENT_IMPLEMENTATION_SPEC.md": """# Client Implementation Specification

## Platform target

## App structure

## Navigation

## State management

## Local persistence

## Networking

## Auth/session handling

## Payment/entitlement handling

## Notifications

## Accessibility

## Localization

## Error handling

## Offline behavior

## Testing requirements
""",
    "ANALYTICS_OBSERVABILITY_SPEC.md": """# Analytics and Observability

## Product analytics principles

## Allowed events

| Event | Trigger | Properties | Forbidden properties |
|---|---|---|---|

## Forbidden events/properties

## Error monitoring

## Performance monitoring

## Security audit events

## AI/provider usage monitoring

## Cost monitoring

## Alerting

## Dashboards
""",
    "QA_ACCEPTANCE_TESTS.md": """# QA and Acceptance Tests

## Test strategy

## Unit tests

## Integration tests

## UI/E2E tests

## Accessibility tests

## Security tests

## Privacy tests

## AI evals and safety red-team tests

## Billing tests

## Offline/failure tests

## Release smoke test

## Feature acceptance matrix

| Feature | Requirements | Tasks | Tests | Status |
|---|---|---|---|---|
""",
    "RELEASE_READINESS.md": """# Release Readiness

## Environment checklist

## Build/release process

## App store or deployment checklist

## Privacy disclosures

## Legal review items

## Security review items

## Monitoring and incident response

## Rollback plan

## Provider outage plan

## Launch smoke tests
""",
    "TASKS.md": """# Build Tasks

## Global instructions for coding agents

- Read README.md, PRODUCT_SPEC.md, TECH_ARCHITECTURE.md, and this file first.
- Use specialized docs for the area being implemented.
- Treat acceptance criteria as completion requirements.

## Global non-goals

- [Fill with non-goals.]

## Task dependency map

```text
TASK-FND-001 -> TASK-[AREA]-002
```

## Tasks

### TASK-FND-001: Initialize production project structure

Goal:
Create the baseline project/repository structure required for implementation.

Context:
This task establishes the foundation for all later work.

Requirements:
- [Fill with app-specific requirements.]

Files or areas likely involved:
- [Paths]

Acceptance criteria:
- [Observable criterion.]

Tests:
- [Test.]

Dependencies:
- None

Do not do:
- Do not implement unrelated features.
""",
    "REFERENCES.md": """# References

Use this file to record current external facts used in the spec.

| Source | Date accessed | Used for | Notes |
|---|---|---|---|
""",
}

OPTIONAL_BY_PLATFORM = {
    "ai": {
        "AI_SPEC.md": """# AI Specification

## AI product role

## AI modes

## Model/provider strategy

## Prompt architecture

## System prompts

## Tool/function calling

## Context construction

## Memory policy

## Safety policy

## Rate limits and plan limits

## Evaluation plan

## Red-team cases

## Fallback behavior

## Logging and retention

## User consent copy
"""
    },
    "backend": {
        "BACKEND_IMPLEMENTATION_SPEC.md": """# Backend Implementation Specification

## Service structure

## API routing

## Database and migrations

## Auth/identity

## Rate limits

## Background jobs

## Webhooks

## Provider adapters

## Logging

## Observability

## Security controls

## Data deletion/export jobs

## Deployment requirements

## Testing requirements
"""
    },
    "payments": {
        "SUBSCRIPTION_BILLING_SPEC.md": """# Subscription and Billing Specification

## Plans and entitlements

## Free plan behavior

## Paid plan behavior

## Trials and promotions

## Upgrade/downgrade/cancel behavior

## Payment provider architecture

## Webhooks and idempotency

## Entitlement caching

## Usage limits

## Refund and billing failure behavior

## Analytics constraints

## Acceptance tests
"""
    },
}

PLATFORM_ALIASES = {
    "ios": "ios",
    "iphone": "ios",
    "ipad": "ios",
    "android": "android",
    "web": "web",
    "webapp": "web",
    "saas": "web",
    "backend": "backend",
    "api": "backend",
    "ai": "ai",
    "ai-feature": "ai",
    "ai-product": "ai",
    "llm": "ai",
    "payments": "payments",
    "billing": "payments",
    "subscription": "payments",
}

PLATFORM_HELP = "ios, android, web, backend, payments, ai"


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "application"


def normalize_platforms(platforms: list[str]) -> list[str]:
    normalized: list[str] = []
    for platform in platforms:
        raw = platform.lower().strip()
        key = PLATFORM_ALIASES.get(raw)
        if key is None:
            raise ValueError(f"Unknown --platform '{platform}'. Expected one of: {PLATFORM_HELP}.")
        if key and key not in normalized:
            normalized.append(key)
    return normalized or ["application"]


def write_file(path: Path, content: str, force: bool) -> None:
    if path.exists() and not force:
        raise FileExistsError(f"Refusing to overwrite existing file: {path}. Use --force.")
    path.write_text(content, encoding="utf-8")


def create_zip(folder: Path) -> Path:
    zip_path = folder.with_suffix(".zip")
    if zip_path.exists():
        zip_path.unlink()
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for file_path in sorted(folder.rglob("*")):
            if file_path.is_file():
                archive.write(file_path, file_path.relative_to(folder.parent))
    return zip_path


def build_package(app_name: str, slug: str, platforms: list[str], output_dir: Path, force: bool, make_zip: bool) -> tuple[Path, Path | None]:
    package_dir = output_dir / f"{slug}-spec"
    if package_dir.exists():
        if not force:
            raise FileExistsError(f"Package directory already exists: {package_dir}. Use --force.")
        shutil.rmtree(package_dir)
    package_dir.mkdir(parents=True, exist_ok=True)

    generated_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
    context = {
        "app_name": app_name,
        "slug": slug,
        "platforms": ", ".join(platforms),
        "generated_at": generated_at,
    }

    files = dict(BASE_FILES)
    for platform in platforms:
        files.update(OPTIONAL_BY_PLATFORM.get(platform, {}))

    # AI and payments often imply backend mediation in production.
    if "ai" in platforms or "payments" in platforms:
        files.update(OPTIONAL_BY_PLATFORM["backend"])
    if "payments" in platforms:
        files.update(OPTIONAL_BY_PLATFORM["payments"])

    for filename, content in sorted(files.items()):
        rendered = content
        for key, value in context.items():
            rendered = rendered.replace("{" + key + "}", value)
        write_file(package_dir / filename, rendered, force=force)

    zip_path = create_zip(package_dir) if make_zip else None
    return package_dir, zip_path


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Scaffold a production app spec package. Platform values are coarse product-module "
            "hints for the generated docs; all specs are written for AI coding agents."
        )
    )
    parser.add_argument("--name", required=True, help="Human-readable app name, e.g. 'Askese'.")
    parser.add_argument("--slug", help="Output slug. Defaults to slugified --name.")
    parser.add_argument(
        "--platform",
        action="append",
        default=[],
        help=(
            "Product module hint. Repeatable. Use web for web app/SaaS concerns, backend for API/server "
            "concerns, payments for billing, and ai only when the product itself has AI/LLM/agent features."
        ),
    )
    parser.add_argument("--out", default=".", help="Output directory. Defaults to current directory.")
    parser.add_argument("--zip", action="store_true", help="Also create a .zip artifact next to the package folder.")
    parser.add_argument("--force", action="store_true", help="Overwrite existing package folder.")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    app_name = args.name.strip()
    if not app_name:
        print("--name must not be empty", file=sys.stderr)
        return 2
    slug = slugify(args.slug or app_name)

    try:
        platforms = normalize_platforms(args.platform)
        output_dir = Path(args.out).expanduser().resolve()
        output_dir.mkdir(parents=True, exist_ok=True)
        package_dir, zip_path = build_package(app_name, slug, platforms, output_dir, args.force, args.zip)
    except Exception as exc:  # noqa: BLE001 - CLI should show actionable error.
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print(f"Created package: {package_dir}")
    if zip_path:
        print(f"Created zip: {zip_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
