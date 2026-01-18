import { Icon } from '@iconify/react'

import { Button } from '@/components/ui/button'
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Separator } from '@/components/ui/separator'
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from '@/components/ui/accordion'
import { Sheet, SheetContent, SheetTrigger } from '@/components/ui/sheet'
import { Input } from '@/components/ui/input'

const NAV_LINKS = [
  { label: 'Features', href: '#features' },
  { label: 'Proof', href: '#proof' },
  { label: 'FAQ', href: '#faq' },
]

const LOGOS = ['Notion', 'Semrush', 'Linear', 'Stripe', 'Figma']

const FEATURES = [
  {
    title: 'Above-the-fold that lands the promise',
    body: 'A hero that states the outcome, shows the product, and makes the next step obvious.',
    icon: 'lucide:layout-template',
  },
  {
    title: 'Proof placed where doubt happens',
    body: 'Logos, metrics, and testimonials positioned to support the CTA, not buried in a footer.',
    icon: 'lucide:badge-check',
  },
  {
    title: 'Persuasion below the fold',
    body: 'Feature outcomes, objection-handling FAQ, and CTA repeats after key moments.',
    icon: 'lucide:sparkles',
  },
]

const FAQ = [
  {
    q: 'Do I need a credit card to start?',
    a: 'No. Start free and upgrade only when you are ready. Cancel anytime.',
  },
  {
    q: 'How fast can I launch this page?',
    a: 'In a day for most teams. Start from the template and swap in your product copy, proof, and visuals.',
  },
  {
    q: 'What should I put in the hero visual?',
    a: 'A concrete preview: a product UI screenshot, a report example, or a before/after result. Avoid decorative art that does not explain the offer.',
  },
]

export default function LandingPage() {
  return (
    <div className="min-h-dvh bg-background text-foreground">
      <SiteNav />
      <main>
        <Hero />
        <LogoCloud />
        <Separator className="mx-auto max-w-6xl" />
        <Features />
        <Proof />
        <FAQSection />
        <FinalCTA />
      </main>
      <SiteFooter />
    </div>
  )
}

function SiteNav() {
  return (
    <header className="sticky top-0 z-50 border-b border-border/60 bg-background/80 backdrop-blur">
      <div className="mx-auto flex max-w-6xl items-center justify-between px-4 py-3">
        <a href="#" className="inline-flex items-center gap-2">
          <span className="grid size-9 place-items-center rounded-lg border border-border bg-card">
            <Icon icon="lucide:triangle" aria-hidden="true" className="size-4" />
          </span>
          <span className="text-sm font-semibold tracking-tight">Acme Landing</span>
        </a>

        <nav className="hidden items-center gap-6 md:flex">
          {NAV_LINKS.map((item) => (
            <a
              key={item.href}
              href={item.href}
              className="text-sm text-muted-foreground hover:text-foreground"
            >
              {item.label}
            </a>
          ))}
        </nav>

        <div className="flex items-center gap-2">
          <Button className="hidden md:inline-flex" size="sm">
            Use for free
            <Icon icon="lucide:arrow-right" aria-hidden="true" className="ml-2 size-4" />
          </Button>

          <Sheet>
            <SheetTrigger asChild>
              <Button
                variant="outline"
                size="icon"
                className="md:hidden"
                aria-label="Open menu"
              >
                <Icon icon="lucide:menu" aria-hidden="true" className="size-5" />
              </Button>
            </SheetTrigger>
            <SheetContent>
              <div className="mt-8 flex flex-col gap-4">
                {NAV_LINKS.map((item) => (
                  <a
                    key={item.href}
                    href={item.href}
                    className="text-sm font-medium"
                  >
                    {item.label}
                  </a>
                ))}
                <Separator />
                <Button>
                  Use for free
                  <Icon
                    icon="lucide:arrow-right"
                    aria-hidden="true"
                    className="ml-2 size-4"
                  />
                </Button>
                <p className="text-xs text-muted-foreground">
                  No credit card required
                </p>
              </div>
            </SheetContent>
          </Sheet>
        </div>
      </div>
    </header>
  )
}

function Hero() {
  return (
    <section className="mx-auto max-w-6xl px-4 pb-10 pt-14 md:pb-16 md:pt-20">
      <div className="grid gap-8 md:grid-cols-12 md:gap-10">
        <div className="md:col-span-6">
          <Badge variant="secondary" className="gap-2">
            <Icon icon="lucide:zap" aria-hidden="true" className="size-4" />
            High-converting landing page anatomy
          </Badge>

          <h1 className="mt-5 text-balance text-4xl font-semibold tracking-tight md:text-5xl">
            Make your landing page obvious in 5 seconds
          </h1>

          <p className="mt-4 text-pretty text-base text-muted-foreground md:text-lg">
            Lead with the outcome, show a concrete visual, place proof next to the
            CTA, and remove objections below the fold.
          </p>

          <div className="mt-7 flex flex-col gap-3 sm:flex-row sm:items-center">
            <Button size="lg" className="justify-center">
              Start free
              <Icon icon="lucide:arrow-right" aria-hidden="true" className="ml-2 size-4" />
            </Button>
            <Button size="lg" variant="outline" className="justify-center">
              Request a demo
            </Button>
          </div>

          <div className="mt-3 flex items-center gap-3 text-xs text-muted-foreground">
            <span className="inline-flex items-center gap-1">
              <Icon icon="lucide:shield" aria-hidden="true" className="size-4" />
              No credit card
            </span>
            <span className="inline-flex items-center gap-1">
              <Icon icon="lucide:clock" aria-hidden="true" className="size-4" />
              60 seconds
            </span>
            <span className="inline-flex items-center gap-1">
              <Icon icon="lucide:x" aria-hidden="true" className="size-4" />
              Cancel anytime
            </span>
          </div>
        </div>

        <div className="md:col-span-6">
          <Card className="overflow-hidden">
            <CardHeader>
              <CardTitle className="text-sm">Hero visual</CardTitle>
              <CardDescription>
                Replace with a real product screenshot, report example, or outcome preview.
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="relative aspect-[16/10] overflow-hidden rounded-lg border border-border bg-gradient-to-br from-muted/60 to-muted">
                <div className="absolute inset-0 grid place-items-center">
                  <div className="text-center">
                    <Icon icon="lucide:image" aria-hidden="true" className="mx-auto size-7 text-muted-foreground" />
                    <p className="mt-2 text-xs text-muted-foreground">Drop your screenshot here</p>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </section>
  )
}

function LogoCloud() {
  return (
    <section className="mx-auto max-w-6xl px-4 pb-10">
      <p className="text-xs font-medium text-muted-foreground">
        Trusted by teams who ship fast
      </p>
      <div className="mt-4 flex flex-wrap items-center gap-x-6 gap-y-3">
        {LOGOS.map((logo) => (
          <div
            key={logo}
            className="text-sm font-semibold tracking-tight text-muted-foreground"
          >
            {logo}
          </div>
        ))}
      </div>
    </section>
  )
}

function Features() {
  return (
    <section id="features" className="mx-auto max-w-6xl px-4 py-12 md:py-16">
      <div className="flex items-end justify-between gap-6">
        <div>
          <h2 className="text-2xl font-semibold tracking-tight md:text-3xl">
            Build conviction in the right order
          </h2>
          <p className="mt-2 max-w-2xl text-sm text-muted-foreground md:text-base">
            Above the fold earns the scroll. Below the fold earns the conversion.
          </p>
        </div>
        <Button variant="outline" className="hidden md:inline-flex">
          See the checklist
          <Icon icon="lucide:chevron-right" aria-hidden="true" className="ml-2 size-4" />
        </Button>
      </div>

      <div className="mt-8 grid gap-4 md:grid-cols-3">
        {FEATURES.map((f) => (
          <Card key={f.title} className="h-full">
            <CardHeader>
              <div className="flex items-center gap-3">
                <span className="grid size-10 place-items-center rounded-lg border border-border bg-card">
                  <Icon icon={f.icon} aria-hidden="true" className="size-5" />
                </span>
                <CardTitle className="text-base">{f.title}</CardTitle>
              </div>
              <CardDescription className="mt-2 text-sm">{f.body}</CardDescription>
            </CardHeader>
          </Card>
        ))}
      </div>

      <div className="mt-8">
        <Card className="border-dashed">
          <CardHeader>
            <CardTitle className="text-base">Repeat the CTA after persuasion moments</CardTitle>
            <CardDescription>
              Place CTA blocks after features, after proof, and after the FAQ.
            </CardDescription>
          </CardHeader>
          <CardContent className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
            <div className="text-sm text-muted-foreground">
              Primary action stays consistent across the page.
            </div>
            <Button>
              Start free
              <Icon icon="lucide:arrow-right" aria-hidden="true" className="ml-2 size-4" />
            </Button>
          </CardContent>
        </Card>
      </div>
    </section>
  )
}

function Proof() {
  return (
    <section id="proof" className="mx-auto max-w-6xl px-4 pb-12 md:pb-16">
      <div className="grid gap-6 md:grid-cols-12">
        <div className="md:col-span-5">
          <h2 className="text-2xl font-semibold tracking-tight md:text-3xl">
            Proof that reduces risk
          </h2>
          <p className="mt-2 text-sm text-muted-foreground md:text-base">
            Use the smallest proof that removes the biggest doubt.
          </p>

          <div className="mt-6 grid grid-cols-2 gap-3">
            <Stat number="12k" label="teams" />
            <Stat number="2.1x" label="higher conversion" />
            <Stat number="60s" label="time to first value" />
            <Stat number="99.9%" label="uptime" />
          </div>
        </div>

        <div className="md:col-span-7">
          <Card>
            <CardHeader>
              <CardTitle className="text-base">A short testimonial</CardTitle>
              <CardDescription>
                Put one strong quote near the CTA instead of a wall of reviews.
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="flex gap-4">
                <div className="grid size-11 place-items-center rounded-full border border-border bg-muted">
                  <Icon icon="lucide:user" aria-hidden="true" className="size-5 text-muted-foreground" />
                </div>
                <div>
                  <p className="text-sm leading-relaxed">
                    “We changed our hero and proof placement and saw signups jump in a week.”
                  </p>
                  <p className="mt-2 text-xs text-muted-foreground">
                    Name, Role at Company
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>

          <div className="mt-4">
            <Card className="bg-card/60">
              <CardContent className="flex flex-col gap-3 p-6 sm:flex-row sm:items-center sm:justify-between">
                <div>
                  <p className="text-sm font-medium">Want this structure applied to your product?</p>
                  <p className="text-xs text-muted-foreground">Share your offer and audience. Get a mapped outline and code.</p>
                </div>
                <Button variant="secondary">
                  Get an outline
                  <Icon icon="lucide:chevron-right" aria-hidden="true" className="ml-2 size-4" />
                </Button>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </section>
  )
}

function Stat({ number, label }: { number: string; label: string }) {
  return (
    <Card>
      <CardContent className="p-4">
        <div className="text-xl font-semibold tracking-tight">{number}</div>
        <div className="mt-1 text-xs text-muted-foreground">{label}</div>
      </CardContent>
    </Card>
  )
}

function FAQSection() {
  return (
    <section id="faq" className="mx-auto max-w-6xl px-4 pb-12 md:pb-16">
      <h2 className="text-2xl font-semibold tracking-tight md:text-3xl">FAQ</h2>
      <p className="mt-2 max-w-2xl text-sm text-muted-foreground md:text-base">
        Answer objections before they become drop-offs.
      </p>

      <div className="mt-6">
        <Accordion type="single" collapsible className="w-full">
          {FAQ.map((item) => (
            <AccordionItem key={item.q} value={item.q}>
              <AccordionTrigger className="text-left">{item.q}</AccordionTrigger>
              <AccordionContent className="text-sm text-muted-foreground">
                {item.a}
              </AccordionContent>
            </AccordionItem>
          ))}
        </Accordion>
      </div>
    </section>
  )
}

function FinalCTA() {
  return (
    <section className="mx-auto max-w-6xl px-4 pb-14">
      <Card className="relative overflow-hidden">
        <CardContent className="grid gap-6 p-6 md:grid-cols-12 md:p-10">
          <div className="md:col-span-7">
            <h3 className="text-balance text-2xl font-semibold tracking-tight md:text-3xl">
              Ready to ship a page that converts?
            </h3>
            <p className="mt-2 max-w-xl text-sm text-muted-foreground md:text-base">
              Start with the anatomy, then tune the copy and proof. Keep the next step simple.
            </p>
          </div>

          <div className="md:col-span-5">
            <div className="flex flex-col gap-3 sm:flex-row sm:items-center">
              <Input placeholder="Work email" type="email" className="h-11" />
              <Button className="h-11">
                Start free
                <Icon icon="lucide:arrow-right" aria-hidden="true" className="ml-2 size-4" />
              </Button>
            </div>
            <p className="mt-2 text-xs text-muted-foreground">No credit card required</p>
          </div>
        </CardContent>
      </Card>
    </section>
  )
}

function SiteFooter() {
  return (
    <footer className="border-t border-border/60">
      <div className="mx-auto grid max-w-6xl gap-6 px-4 py-10 md:grid-cols-12">
        <div className="md:col-span-5">
          <div className="flex items-center gap-2">
            <span className="grid size-9 place-items-center rounded-lg border border-border bg-card">
              <Icon icon="lucide:triangle" aria-hidden="true" className="size-4" />
            </span>
            <span className="text-sm font-semibold">Acme Landing</span>
          </div>
          <p className="mt-3 max-w-sm text-xs text-muted-foreground">
            A starter template for a high-converting landing page structure.
          </p>
        </div>

        <div className="grid gap-6 sm:grid-cols-3 md:col-span-7">
          <FooterCol
            title="Product"
            links={[
              { label: 'Features', href: '#features' },
              { label: 'Proof', href: '#proof' },
              { label: 'FAQ', href: '#faq' },
            ]}
          />
          <FooterCol
            title="Company"
            links={[
              { label: 'About', href: '#' },
              { label: 'Careers', href: '#' },
              { label: 'Contact', href: '#' },
            ]}
          />
          <FooterCol
            title="Legal"
            links={[
              { label: 'Privacy', href: '#' },
              { label: 'Terms', href: '#' },
            ]}
          />
        </div>
      </div>

      <div className="border-t border-border/60">
        <div className="mx-auto flex max-w-6xl flex-col gap-2 px-4 py-4 text-xs text-muted-foreground md:flex-row md:items-center md:justify-between">
          <span>© {new Date().getFullYear()} Acme Landing</span>
          <span className="inline-flex items-center gap-2">
            <a href="#" className="hover:text-foreground">Twitter</a>
            <span aria-hidden="true">·</span>
            <a href="#" className="hover:text-foreground">GitHub</a>
          </span>
        </div>
      </div>
    </footer>
  )
}

function FooterCol({
  title,
  links,
}: {
  title: string
  links: { label: string; href: string }[]
}) {
  return (
    <div>
      <div className="text-xs font-semibold uppercase tracking-widest text-muted-foreground">
        {title}
      </div>
      <div className="mt-3 flex flex-col gap-2">
        {links.map((l) => (
          <a key={l.label} href={l.href} className="text-sm hover:text-foreground">
            {l.label}
          </a>
        ))}
      </div>
    </div>
  )
}
