---
type: health
category: migraine
created: <% tp.date.now("YYYY-MM-DD") %>
title: Migraine Log
slug: <% tp.date.now("YYYYMMDD-HHmm") %>-migraine
timestamp: <% tp.date.now("YYYYMMDD-HHmm") %>
area: self
date: <% tp.date.now("YYYY-MM-DD") %>
pain_level: <% await tp.system.suggester(["🟢 none", "🔵 tension", "🟡 mild", "🟠 moderate", "🔴 severe"], ["🟢", "🔵", "🟡", "🟠", "🔴"], false, "Pijnniveau") %>
triggers: [<% await tp.system.suggester(["geen", "geur", "voedsel", "slaap", "licht", "sport", "stress", "griep"], ["", "geur", "voedsel", "slaap", "licht", "sport", "stress", "griep"], false, "Trigger (belangrijkste)") %>]
meds: [<% await tp.system.suggester(["geen", "Paracetamol 1000mg", "Rizatriptan 5mg", "Paracetamol + Rizatriptan"], ["", "Paracetamol 1000mg", "Rizatriptan 5mg", "Paracetamol 1000mg, Rizatriptan 5mg"], false, "Medicatie") %>]
preventive: Metoprolol 100mg
---

# Migraine Log — <% tp.date.now("D MMMM YYYY", 0, tp.file.title, "YYYYMMDD-HHmm-[migraine]", "nl") %>

## Verloop

<% tp.file.cursor() %>

## Context

- **Slaap:**
- **Eten:**
- **Stress:**
- **Weer:**
