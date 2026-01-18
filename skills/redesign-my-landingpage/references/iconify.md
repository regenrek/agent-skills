# Iconify icons (Iconify icon sets)

Use icons from https://icon-sets.iconify.design/.

## Recommended approach for React + Vite

Use `@iconify/react`.
It loads icon data on demand from the Iconify API, so you only pay for icons you actually use.

### Install

```bash
pnpm add @iconify/react
```

### Basic usage

```tsx
import { Icon } from "@iconify/react"

export function Example() {
  return <Icon icon="mdi:home" />
}
```

## App-wide rules

- Use 1 icon collection per page (2 max). Example collections: `mdi:`, `tabler:`, `ph:`, `lucide:`.
- Match style to the aesthetic direction (outline vs filled, rounded vs sharp).
- Do not sprinkle icons everywhere. If it does not add meaning, remove it.

## Wrapper component (recommended)

Create `src/components/app-icon.tsx`:

```tsx
import { Icon, type IconProps } from "@iconify/react"

type AppIconProps = IconProps & {
  decorative?: boolean
  label?: string
}

export function AppIcon({ decorative = true, label, ...props }: AppIconProps) {
  if (decorative) {
    return <Icon aria-hidden="true" {...props} />
  }
  return <Icon aria-label={label ?? "Icon"} role="img" {...props} />
}
```

### Example in a shadcn Button

```tsx
import { Button } from "@/components/ui/button"
import { AppIcon } from "@/components/app-icon"

export function PrimaryCTA() {
  return (
    <Button size="lg" className="gap-2">
      Start free
      <AppIcon icon="mdi:arrow-right" className="size-4" decorative />
    </Button>
  )
}
```

## Picking icons fast

- Search by concept, then lock a prefix.
- Prefer simple shapes for small sizes.
- For feature lists, reuse a consistent style: all outline or all filled.

## If you must avoid a third-party API

Use Iconify offline mode (bundle specific icons) or host an Iconify API.
Only do this if the user asks for it.
