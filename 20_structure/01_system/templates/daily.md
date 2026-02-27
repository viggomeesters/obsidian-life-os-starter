---
type: entry
category: daily
created: <% tp.date.now("YYYY-MM-DD") %>
slug: <% tp.date.now("YYYYMMDD") %>-0600-daily
timestamp: <% tp.date.now("YYYYMMDD") %>-0600
area: self
title: "Daily Note"
topics: [daily]
---

| PREVIOUS | NEXT |
| --- | --- |
| [[<% tp.date.now("YYYYMMDD", -1) %>-0600-daily]] | [[<% tp.date.now("YYYYMMDD", 1) %>-0600-daily]] |

# <% tp.date.now("dddd D MMMM YYYY", 0, tp.file.title, "YYYYMMDD-HHmm-[daily]") %>

## Schedule


## Notes


## Activity

<% tp.file.cursor() %>
