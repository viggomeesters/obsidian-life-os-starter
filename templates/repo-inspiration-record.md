---
template: repo-inspiration-record
version: 1
---

# Repo inspiration record template

Gebruik dit wanneer Viggo een GitHub repo doorstuurt vanuit Trending of expliciet vraagt om een repo te minen.

```yaml
id: owner-repo
repo: owner/repo
url: https://github.com/owner/repo
first_seen: YYYY-MM-DD
source: github-trending
source_id: telegram:<chat_id>:<message_or_session_id>
status: inbox
why_interesting: ""
mined_for: []
tags: []
license: unknown
attribution_needed: unknown
copied_code: false
ideas_extracted: []
applied_in: []
review_notes: ""
last_reviewed: null
```

## Status discipline

- `inbox`: alleen vastgelegd.
- `reviewed`: repo bekeken; bruikbaar/niet bruikbaar is onderbouwd.
- `mined`: concrete patterns/ideeën staan in `ideas_extracted`.
- `adopted`: eigen implementatie staat in `applied_in`.
- `rejected`: bewust niet gebruiken.
- `archived`: historische provenance.

## Copy/licentiegrens

Laat `copied_code: false` tenzij er bewust code is overgenomen en licentie/attribution is gecontroleerd.
