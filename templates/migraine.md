---
type: health
category: migraine
created: <% tp.date.now("YYYY-MM-DD") %>
title: Migraine Log
slug: <% tp.date.now("YYYYMMDD-HHmm") %>-migraine
timestamp: <% tp.date.now("YYYYMMDD-HHmm") %>
area: self
date: <% tp.date.now("YYYY-MM-DD") %>
pain_level: <% await tp.system.suggester(["🟢 none", "🔵 tension", "🟡 mild", "🟠 moderate", "🔴 severe"], ["🟢", "🔵", "🟡", "🟠", "🔴"], false, "Pain level") %>
triggers: [<% await tp.system.suggester(["none", "smell", "food", "sleep", "light", "exercise", "stress"], ["", "smell", "food", "sleep", "light", "exercise", "stress"], false, "Primary trigger") %>]
meds: [<% await tp.system.suggester(["none", "Acetaminophen 1000mg", "Sumatriptan 50mg", "Acetaminophen + Sumatriptan"], ["", "Acetaminophen 1000mg", "Sumatriptan 50mg", "Acetaminophen 1000mg, Sumatriptan 50mg"], false, "Medication") %>]
preventive:
---

# Migraine Log — <% tp.date.now("D MMMM YYYY") %>

## Progression

<% tp.file.cursor() %>

## Context

- **Sleep:**
- **Diet:**
- **Stress:**
- **Weather:**
