# Section templates (shadcn + Iconify)

Use these as a starting point, then adapt to the product, copy, and aesthetic.

Assumptions:
- shadcn components live in `src/components/ui/*`
- You have `AppIcon` from `references/iconify.md`

## File structure

```txt
src/
  components/
    AppIcon.tsx
    sections/
      Navbar.tsx
      Hero.tsx
      SocialProof.tsx
      Features.tsx
      Testimonials.tsx
      FAQ.tsx
      CTABand.tsx
      Footer.tsx
  pages/
    LandingPage.tsx
  App.tsx
```

## Navbar

```tsx
import { Button } from "@/components/ui/button";

export function Navbar() {
  return (
    <header className="sticky top-0 z-40 border-b bg-background/70 backdrop-blur">
      <div className="mx-auto flex max-w-6xl items-center justify-between px-4 py-3">
        <div className="flex items-center gap-2">
          <div className="size-8 rounded-lg bg-foreground" />
          <span className="text-sm font-semibold tracking-tight">Brand</span>
        </div>

        <nav className="hidden items-center gap-6 text-sm text-muted-foreground md:flex">
          <a className="hover:text-foreground" href="#features">Features</a>
          <a className="hover:text-foreground" href="#proof">Proof</a>
          <a className="hover:text-foreground" href="#faq">FAQ</a>
        </nav>

        <div className="flex items-center gap-2">
          <Button variant="ghost" className="hidden sm:inline-flex">Sign in</Button>
          <Button>Start free</Button>
        </div>
      </div>
    </header>
  );
}
```

## Hero

```tsx
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { AppIcon } from "@/components/AppIcon";

export function Hero() {
  return (
    <section className="relative overflow-hidden">
      <div className="pointer-events-none absolute inset-0 opacity-60">
        <div className="absolute -left-24 -top-24 size-[28rem] rounded-full bg-muted blur-3xl" />
        <div className="absolute -bottom-24 -right-24 size-[28rem] rounded-full bg-muted blur-3xl" />
      </div>

      <div className="mx-auto grid max-w-6xl grid-cols-1 gap-10 px-4 py-14 md:grid-cols-2 md:py-20">
        <div className="relative">
          <Badge className="mb-4" variant="secondary">
            <AppIcon icon="lucide:sparkles" className="mr-2 size-4" />
            New: 7-day onboarding playbook
          </Badge>

          <h1 className="text-balance text-4xl font-semibold tracking-tight md:text-5xl">
            Turn messy work into momentum in one workspace
          </h1>

          <p className="mt-4 text-pretty text-base leading-relaxed text-muted-foreground md:text-lg">
            A single place to plan, ship, and share. Templates that start fast and stay flexible.
          </p>

          <ul className="mt-6 space-y-2 text-sm text-muted-foreground">
            <li className="flex items-center gap-2">
              <AppIcon icon="lucide:check" className="size-4" />
              Launch a workspace in minutes
            </li>
            <li className="flex items-center gap-2">
              <AppIcon icon="lucide:check" className="size-4" />
              Keep teams aligned without meetings
            </li>
            <li className="flex items-center gap-2">
              <AppIcon icon="lucide:check" className="size-4" />
              Track outcomes with clarity
            </li>
          </ul>

          <div className="mt-8 flex flex-col gap-3 sm:flex-row">
            <Button className="h-11 px-6">Use for free</Button>
            <Button variant="outline" className="h-11 px-6">
              Request a demo
              <AppIcon icon="lucide:arrow-right" className="ml-2 size-4" />
            </Button>
          </div>

          <div className="mt-6 text-xs text-muted-foreground">
            Trusted by teams at 1,200+ companies.
          </div>
        </div>

        <div className="relative">
          <div className="aspect-[4/3] w-full rounded-2xl border bg-muted/40 shadow-sm" />
          <div className="mt-3 flex items-center justify-between text-xs text-muted-foreground">
            <span>Preview</span>
            <span>Live collaboration, tasks, docs</span>
          </div>
        </div>
      </div>
    </section>
  );
}
```

## Social proof

```tsx
import { Card, CardContent } from "@/components/ui/card";

export function SocialProof() {
  const logos = ["Acme", "Orbit", "Quanta", "Nimbus", "Copper"];

  return (
    <section id="proof" className="border-y bg-muted/20">
      <div className="mx-auto max-w-6xl px-4 py-10">
        <p className="text-center text-xs font-medium text-muted-foreground">
          Trusted by product teams and agencies
        </p>

        <div className="mt-6 grid grid-cols-2 gap-3 sm:grid-cols-3 md:grid-cols-5">
          {logos.map((name) => (
            <div key={name} className="flex items-center justify-center rounded-xl border bg-background px-3 py-4 text-sm text-muted-foreground">
              {name}
            </div>
          ))}
        </div>

        <div className="mt-8 grid gap-4 md:grid-cols-3">
          <Card>
            <CardContent className="p-6">
              <div className="text-2xl font-semibold">3.2x</div>
              <div className="mt-1 text-sm text-muted-foreground">Faster onboarding</div>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="p-6">
              <div className="text-2xl font-semibold">28%</div>
              <div className="mt-1 text-sm text-muted-foreground">More tasks shipped</div>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="p-6">
              <div className="text-2xl font-semibold">2h</div>
              <div className="mt-1 text-sm text-muted-foreground">Saved per week, per person</div>
            </CardContent>
          </Card>
        </div>
      </div>
    </section>
  );
}
```

## Features

```tsx
import { Card, CardContent } from "@/components/ui/card";
import { AppIcon } from "@/components/AppIcon";

const items = [
  {
    icon: "lucide:layout-dashboard",
    title: "Everything in one view",
    body: "Docs, tasks, and decisions stay connected so you never lose context.",
  },
  {
    icon: "lucide:wand-2",
    title: "Templates that evolve",
    body: "Start structured, then adapt without breaking your system.",
  },
  {
    icon: "lucide:shield",
    title: "Permission clarity",
    body: "Share confidently with granular access and simple controls.",
  },
];

export function Features() {
  return (
    <section id="features">
      <div className="mx-auto max-w-6xl px-4 py-14">
        <div className="max-w-2xl">
          <h2 className="text-2xl font-semibold tracking-tight md:text-3xl">Built to move work forward</h2>
          <p className="mt-2 text-muted-foreground">Outcome-first features that reduce friction and increase follow-through.</p>
        </div>

        <div className="mt-8 grid gap-4 md:grid-cols-3">
          {items.map((f) => (
            <Card key={f.title} className="overflow-hidden">
              <CardContent className="p-6">
                <div className="flex items-center gap-3">
                  <div className="grid size-10 place-items-center rounded-xl border bg-muted/30">
                    <AppIcon icon={f.icon} className="size-5" />
                  </div>
                  <div className="font-medium">{f.title}</div>
                </div>
                <p className="mt-3 text-sm leading-relaxed text-muted-foreground">{f.body}</p>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </section>
  );
}
```

## FAQ (Accordion)

```tsx
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion";

const faqs = [
  { q: "Can I start free?", a: "Yes. Start free, upgrade only when you need advanced controls." },
  { q: "Will this work for teams?", a: "Yes. Invite teammates, set permissions, and keep work organized." },
  { q: "How fast can I set it up?", a: "Most teams are productive in under 30 minutes using templates." },
];

export function FAQ() {
  return (
    <section id="faq" className="border-t">
      <div className="mx-auto max-w-6xl px-4 py-14">
        <h2 className="text-2xl font-semibold tracking-tight md:text-3xl">FAQ</h2>
        <p className="mt-2 text-muted-foreground">Answer objections before they become drop-offs.</p>

        <div className="mt-6 max-w-2xl">
          <Accordion type="single" collapsible>
            {faqs.map((item) => (
              <AccordionItem key={item.q} value={item.q}>
                <AccordionTrigger>{item.q}</AccordionTrigger>
                <AccordionContent>{item.a}</AccordionContent>
              </AccordionItem>
            ))}
          </Accordion>
        </div>
      </div>
    </section>
  );
}
```

## CTA band

```tsx
import { Button } from "@/components/ui/button";
import { AppIcon } from "@/components/AppIcon";

export function CTABand() {
  return (
    <section className="border-t bg-muted/20">
      <div className="mx-auto flex max-w-6xl flex-col items-start gap-6 px-4 py-14 md:flex-row md:items-center md:justify-between">
        <div>
          <h3 className="text-xl font-semibold tracking-tight">Start with momentum</h3>
          <p className="mt-1 text-sm text-muted-foreground">Get set up today. Invite your team tomorrow.</p>
        </div>
        <div className="flex w-full flex-col gap-3 sm:w-auto sm:flex-row">
          <Button className="h-11 px-6">Use for free</Button>
          <Button variant="outline" className="h-11 px-6">
            See pricing
            <AppIcon icon="lucide:arrow-right" className="ml-2 size-4" />
          </Button>
        </div>
      </div>
    </section>
  );
}
```

## Footer

```tsx
export function Footer() {
  return (
    <footer className="border-t">
      <div className="mx-auto flex max-w-6xl flex-col gap-6 px-4 py-10 md:flex-row md:items-center md:justify-between">
        <div className="text-sm text-muted-foreground">© {new Date().getFullYear()} Brand. All rights reserved.</div>
        <div className="flex gap-5 text-sm text-muted-foreground">
          <a className="hover:text-foreground" href="#">Privacy</a>
          <a className="hover:text-foreground" href="#">Terms</a>
          <a className="hover:text-foreground" href="#">Contact</a>
        </div>
      </div>
    </footer>
  );
}
```

## Compose the page

`src/pages/LandingPage.tsx`

```tsx
import { Navbar } from "@/components/sections/Navbar";
import { Hero } from "@/components/sections/Hero";
import { SocialProof } from "@/components/sections/SocialProof";
import { Features } from "@/components/sections/Features";
import { FAQ } from "@/components/sections/FAQ";
import { CTABand } from "@/components/sections/CTABand";
import { Footer } from "@/components/sections/Footer";

export function LandingPage() {
  return (
    <div className="min-h-svh bg-background text-foreground">
      <Navbar />
      <main>
        <Hero />
        <SocialProof />
        <Features />
        <FAQ />
        <CTABand />
      </main>
      <Footer />
    </div>
  );
}
```
