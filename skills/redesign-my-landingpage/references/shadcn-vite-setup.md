# shadcn/ui + Vite setup (React + TypeScript)

Use this when the user wants a full Vite project scaffold, not just a component.

## Notes on Tailwind versions

- Default: Tailwind v4 setup.
- If the project is on Tailwind v3, pin the shadcn CLI version compatible with that stack (the shadcn docs call this out).

## 1) Create the Vite project

Create a new React + TypeScript app:

```bash
pnpm create vite@latest
```

Then install deps and run dev:

```bash
pnpm install
pnpm dev
```

## 2) Add Tailwind CSS (Tailwind v4)

Install Tailwind and the Vite plugin:

```bash
pnpm add tailwindcss @tailwindcss/vite
```

Replace `src/index.css` with:

```css
@import "tailwindcss";
```

## 3) Configure path aliases for `@/...`

Edit `tsconfig.json` and add:

```json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    }
  }
}
```

Also edit `tsconfig.app.json` and add the same `baseUrl` + `paths` mapping under `compilerOptions`.

## 4) Update `vite.config.ts`

Install Node types:

```bash
pnpm add -D @types/node
```

Update `vite.config.ts` to include Tailwind and the alias:

```ts
import path from "path"
import tailwindcss from "@tailwindcss/vite"
import react from "@vitejs/plugin-react"
import { defineConfig } from "vite"

export default defineConfig({
  plugins: [react(), tailwindcss()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
})
```

## 5) Initialize shadcn/ui

Run the init command:

```bash
pnpm dlx shadcn@latest init
```

This creates `components.json` and sets up shadcn theme tokens.

## 6) Add the components you will use

For a typical landing page, add a small set:

```bash
pnpm dlx shadcn@latest add button
pnpm dlx shadcn@latest add card
pnpm dlx shadcn@latest add badge
pnpm dlx shadcn@latest add separator
pnpm dlx shadcn@latest add accordion
pnpm dlx shadcn@latest add sheet
pnpm dlx shadcn@latest add avatar
pnpm dlx shadcn@latest add input
```

Then import like:

```ts
import { Button } from "@/components/ui/button"
```

## 7) Iconify (icons)

Install:

```bash
pnpm add @iconify/react
```

Use icons by name (on demand):

```tsx
import { Icon } from "@iconify/react"

<Icon icon="lucide:arrow-right" aria-hidden="true" />
```

## Optional: dark mode

If the user asks for dark mode, follow the shadcn dark mode guide for Vite and implement a theme toggle.
