import * as React from "react";
import { ArrowUpRight, Radar, ShieldCheck, Workflow } from "lucide-react";

import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

export function Hero() {
  return (
    <section className="pt-8 pb-12 sm:pt-14">
      <div className="grid gap-6 lg:grid-cols-[1.35fr_1fr]">
        <Card className="overflow-hidden border-border/70 shadow-[0_18px_50px_hsl(var(--foreground)/0.07)]">
          <CardHeader className="space-y-6 p-7 sm:p-9">
            <div className="flex flex-wrap items-center gap-4">
              <Avatar className="h-14 w-14 ring-2 ring-primary/20">
                <AvatarImage src="/avatar.png" alt="Enguerrand Allamel" />
                <AvatarFallback>EA</AvatarFallback>
              </Avatar>
              <div className="flex flex-col gap-2">
                <Badge className="w-fit border border-primary/20 bg-primary/10 text-primary hover:bg-primary/20">
                  Staff Cloud Security Engineer
                </Badge>
                <p className="text-sm text-muted-foreground">
                  Security | SRE | Platform Engineering
                </p>
              </div>
            </div>

            <CardTitle className="max-w-3xl text-4xl leading-tight sm:text-5xl lg:text-6xl">
              Hi, I&apos;m Enguerrand. I build{" "}
              <span className="text-primary">secure and reliable cloud platforms</span>.
            </CardTitle>
            <CardDescription className="max-w-2xl text-base leading-relaxed text-muted-foreground sm:text-lg">
              This site is my notebook for talks, ideas, and field notes from security,
              SRE, and platform engineering. I write about what works in production and
              what still needs better defaults.
            </CardDescription>
          </CardHeader>
          <CardContent className="flex flex-wrap items-center gap-3 px-7 pb-8 sm:px-9">
            <Button asChild className="gap-2">
              <a href="/talks">
                Explore talks <ArrowUpRight className="h-4 w-4" />
              </a>
            </Button>
            <Button asChild variant="outline">
              <a href="#contact">Say hello</a>
            </Button>
          </CardContent>
        </Card>

        <Card className="border-border/70 bg-card/90 shadow-[0_14px_38px_hsl(var(--foreground)/0.06)]">
          <CardHeader className="space-y-1">
            <CardTitle className="text-2xl">Currently exploring</CardTitle>
            <CardDescription>Topics I&apos;m spending time on lately.</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="rounded-xl border border-border/70 bg-secondary/55 p-4">
              <div className="mb-2 flex items-center gap-2 text-sm font-semibold">
                <ShieldCheck className="h-4 w-4 text-primary" />
                Supply-chain trust
              </div>
              <p className="text-sm text-muted-foreground">
                Provenance, signing, and identity-based controls that are realistic for daily developer workflows.
              </p>
            </div>
            <div className="rounded-xl border border-border/70 bg-secondary/55 p-4">
              <div className="mb-2 flex items-center gap-2 text-sm font-semibold">
                <Radar className="h-4 w-4 text-primary" />
                Runtime security signals
              </div>
              <p className="text-sm text-muted-foreground">
                Better ways to prioritize risks using context instead of raw vulnerability counts.
              </p>
            </div>
            <div className="rounded-xl border border-border/70 bg-secondary/55 p-4">
              <div className="mb-2 flex items-center gap-2 text-sm font-semibold">
                <Workflow className="h-4 w-4 text-primary" />
                Platform guardrails
              </div>
              <p className="text-sm text-muted-foreground">
                Designing defaults that keep teams fast without creating silent reliability or security debt.
              </p>
            </div>
          </CardContent>
        </Card>
      </div>
    </section>
  );
}
