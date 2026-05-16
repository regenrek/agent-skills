# Usage Examples

## iOS SwiftUI progress ring

```bash
search-context run "visual progress indicator ring for ios app latest 2026" \
  --preset ios-swift \
  --max-repos 5 \
  --min-stars 10
```

## Web React progress ring

```bash
search-context run "visual progress ring React TypeScript Tailwind" \
  --preset web-react \
  --max-repos 5
```

## Preview without cloning

```bash
search-context run "SwiftUI calendar component" \
  --preset ios-swift \
  --dry-run
```

## Search local references

```bash
search-context library search "ProgressViewStyle"
```

## Register a third-party folder

```bash
search-context library add ../third-party/progress-ring \
  --tags swiftui,progress \
  --presets ios-swift \
  --project current
```

## Mix library and GitHub discovery

```bash
search-context run "SwiftUI progress ring animation" \
  --preset ios-swift \
  --sources library,github \
  --project current
```

## Keep outputs in the current project

```bash
search-context run "SwiftUI calendar component" \
  --preset ios-swift \
  --project-local
```

When using `--project-local` inside a Git worktree, add `.refs/` and `.context/` to `.gitignore` first.
