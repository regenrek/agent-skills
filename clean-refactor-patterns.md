# clean refactor patterns for coding agents

coding agents do their best to keep a contract alive. they add normalization, double owners, fallback paths, and other compact fixes to avoid breaking changes.

that sounds nice at first, but we want a scalable codebase, not a linear one that keeps growing by patches. those fixes create noise, make things messy, make testing harder, and over time the real ownership starts to drift.

and even when you later hard cut old contracts or refactor them out, you still pay for it. either you keep guards around so the old shape never comes back, or you leave empty stubs and compatibility crumbs behind.

painful to hear, but this is still work. it is usually not about one-shot cleanup. it is about keeping layers alive without letting them overlap. and when you refactor, it should be done clean, without adding more guards and more code around the old path.

copy-pasting skills or patterns is only one side of it. they still need to be adapted to your own codebase. at minimum, form docs around your actual architecture so the agent knows how your system is supposed to stay clean over time.

these are some of the patterns i use for that.

## 1. architecture ownership

i built this skill to make ownership explicit.

it helps declare the runtime owner, the first-fix owner, and the canonical long-term owner of a feature.

without that, codex tends to place features in the wrong layer, or patch the layer where the bug shows up instead of the layer that should own it long term.

for example, if you have an x-api, x-backend, and x-daemon, the coding agent needs to know where the behavior currently happens, where the first fix belongs, and where the feature should actually live after cleanup. otherwise refactors drift and duplicate ownership starts to grow.

## 2. root-cause finder

this skill is useful if you want to avoid hotfixes around a small path.

coding agents often quick-fix the visible failure so the error goes away. but a lot of the time the real problem is earlier in the chain: a wrong write, wrong owner, hidden sync path, restore path, watcher, or background mutation.

root-cause finder forces the agent to trace the behavior back to the first unintended side effect before changing contracts, parsing, or types.

that is also why architecture-ownership matters in the first place. if you do not know who should own the behavior, it is much easier to patch the wrong layer and call it fixed.

## 3. find-duplicate-ownership

i run this skill from time to time, sometimes with subagents, to explore duplicate ownership, hidden second sources of truth, and contract drift.

it is useful when the same rule starts getting owned in multiple places, like frontend and backend both repairing the same data, or runtime code and persisted state both trying to be canonical.

it also helps separate real duplicate ownership from legitimate boundary work, so you do not end up flagging every adapter or transform as an architecture problem.

## 4. hard-cut

this is the brother of find-duplicate-ownership.

once you know there is dual ownership, hard-cut tells the coding agent to keep one canonical current-state path and delete fallback, compatibility, dual-read, dual-write, or silent coercion code unless transition support was explicitly asked for.

the point is to actually remove the losing owner, not wrap it in another layer.

## x. mcp / cli

whatever you use, cli or mcp, use something that can actually talk to and inspect your app.

it is much easier for a coding agent to work from live state, real behavior, and visible runtime signals than to guess only from the codebase.

## y. small task system / memory

there are dozens of memory and task-based solutions out there. you can use them on your behalf if they fit, but often a small plan -> code -> review loop is enough.

that can live in a json file or whatever fits your project. the important part is not building a huge system. it is giving the agent just enough structure to stay grounded while it works.
