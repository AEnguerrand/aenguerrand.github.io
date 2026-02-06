import * as React from "react";
import { Blocks, ShieldCheck, Siren, Wrench } from "lucide-react";

import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "@/components/ui/accordion";
import { Badge } from "@/components/ui/badge";
import { Card, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";

const focusItems = [
  {
    value: "security",
    title: "Security Engineering",
    subtitle: "Supply-chain integrity and runtime protection",
    description:
      "SLSA-driven build trust, image signing, and identity-aware controls integrated across CI/CD and workloads.",
    icon: ShieldCheck,
  },
  {
    value: "sre",
    title: "SRE & Reliability",
    subtitle: "Incident-ready systems that scale",
    description:
      "Error budgets, observability, and response playbooks designed to keep critical services stable under load.",
    icon: Siren,
  },
  {
    value: "platform",
    title: "Platform Strategy",
    subtitle: "Secure-by-default enablement",
    description:
      "Reusable blueprints, guardrails, and developer experience patterns that standardize quality without friction.",
    icon: Blocks,
  },
] as const;

export function FocusAccordion() {
  return (
    <section id="focus" className="space-y-6">
      <Card className="border-border/70 bg-card/80 shadow-[0_16px_44px_hsl(var(--foreground)/0.05)]">
        <CardHeader className="space-y-4">
          <Badge variant="secondary" className="w-fit border border-border/70 bg-secondary/65">
            Focus areas
          </Badge>
          <CardTitle className="text-3xl sm:text-4xl">How I drive platform security</CardTitle>
          <CardDescription className="max-w-3xl text-base leading-relaxed">
            I work at the intersection of architecture, operations, and enablement. These are
            the core tracks I lead with product and platform teams.
          </CardDescription>
        </CardHeader>
      </Card>

      <Accordion type="single" collapsible className="w-full space-y-3">
        {focusItems.map((item) => {
          const Icon = item.icon;
          return (
            <AccordionItem
              key={item.value}
              value={item.value}
              className="overflow-hidden rounded-xl border border-border/70 bg-card/85 px-5 shadow-[0_10px_26px_hsl(var(--foreground)/0.04)]"
            >
              <AccordionTrigger className="py-5 hover:no-underline">
                <div className="flex items-center gap-3 text-left">
                  <span className="rounded-lg border border-primary/30 bg-primary/10 p-2">
                    <Icon className="h-4 w-4 text-primary" />
                  </span>
                  <div>
                    <p className="text-base font-semibold text-foreground">{item.title}</p>
                    <p className="text-sm text-muted-foreground">{item.subtitle}</p>
                  </div>
                </div>
              </AccordionTrigger>
              <AccordionContent className="pb-5">
                <div className="rounded-xl border border-border/60 bg-secondary/45 px-4 py-3">
                  <div className="mb-2 flex items-center gap-2 text-sm font-medium text-foreground">
                    <Wrench className="h-4 w-4 text-primary" />
                    Execution approach
                  </div>
                  <p className="text-sm leading-relaxed text-muted-foreground">{item.description}</p>
                </div>
              </AccordionContent>
            </AccordionItem>
          );
        })}
      </Accordion>
    </section>
  );
}
