import * as React from "react";
import { Github, Linkedin, Mail, MessageSquareMore } from "lucide-react";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";

export function ContactCard() {
  return (
    <section id="contact" className="mt-16">
      <Card className="overflow-hidden border-border/70 bg-card/90 shadow-[0_16px_42px_hsl(var(--foreground)/0.06)]">
        <CardHeader className="space-y-4">
          <Badge className="w-fit border border-primary/20 bg-primary/10 text-primary hover:bg-primary/20">
            Contact
          </Badge>
          <CardTitle className="text-3xl sm:text-4xl">Need help on security and platform strategy?</CardTitle>
          <CardDescription>
            Share your context and goals, and I can help shape a practical plan across security,
            reliability, and engineering enablement.
          </CardDescription>
        </CardHeader>
        <CardContent className="grid gap-5 pb-8 lg:grid-cols-[1.25fr_1fr]">
          <div className="rounded-xl border border-border/70 bg-secondary/45 p-5">
            <div className="mb-3 flex items-center gap-2 text-sm font-semibold uppercase tracking-[0.08em] text-muted-foreground">
              <MessageSquareMore className="h-4 w-4 text-primary" />
              Best for
            </div>
            <p className="text-sm leading-relaxed text-muted-foreground">
              Architecture reviews, platform hardening roadmaps, incident readiness, and cloud risk reduction programs.
            </p>
          </div>

          <div className="space-y-3">
            <Button asChild className="w-full justify-start gap-2">
              <a href="mailto:hello@enguerrand.dev">
                <Mail className="h-4 w-4" />
                hello@enguerrand.dev
              </a>
            </Button>
            <Button asChild variant="outline" className="w-full justify-start gap-2">
              <a href="https://www.linkedin.com/in/enguerrandallamel/" target="_blank" rel="noreferrer">
                <Linkedin className="h-4 w-4" />
                linkedin.com/in/enguerrandallamel
              </a>
            </Button>
            <Button asChild variant="outline" className="w-full justify-start gap-2">
              <a href="https://github.com/AEnguerrand" target="_blank" rel="noreferrer">
                <Github className="h-4 w-4" />
                github.com/AEnguerrand
              </a>
            </Button>
          </div>
        </CardContent>
      </Card>
    </section>
  );
}
