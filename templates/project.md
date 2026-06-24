---
type: project
category: personal
created: {{date:YYYY-MM-DD}}
title: "{{title}}"
slug: {{slug}}
timestamp: {{date:YYYYMMDD-HHmm}}
status: 🔴 to-do
area: self
entity: []
topics: []
code:
start_date: {{date:YYYY-MM-DD}}
end_date:
local_path:
url:
description: {{description}}
---

# {{title}}

{{description}}

## Start hier

- **Huidige fase:**
- **Werkfocus:**
- **Belangrijkste ingang:**
- **Volgende tastbare stap:**
- **Lokale werkmap:**

## Dashboard

| Veld | Waarde |
|---|---|
| Status | 🔴 to-do |
| Code | `{{code}}` |
| Start | {{date:YYYY-MM-DD}} |
| Einddatum |  |
| Primaire contacten |  |
| Lokale map |  |
| Externe link |  |

## Openstaande taken

```dataview
TABLE status AS Status, due AS Deadline, file.mtime AS Gewijzigd
FROM "10_notes"
WHERE project = this.slug
  AND type = "task"
  AND !contains(["🟢 done", "⚫ cancelled"], status)
SORT due ASC, timestamp DESC
```

## Recente activiteit

```dataview
LIST
FROM "10_notes"
WHERE project = this.slug
SORT timestamp DESC
LIMIT 15
```

## Werkcontext

- TBD

## Systemen en toegang

- TBD

## Contacten

- TBD

## Referenties

- TBD

## Features

| ID | Feature | Description |
| :--- | :--- | :--- |
| **F01** | {{feature}} | {{feature_description}} |

## Zoekanker

```query
project: {{slug}}
```

## Session Logs

### {{date:YYYY-MM-DD HH:mm}} - [Subject]
- **Prompt**:
- **Plan**:
- **Result**:
