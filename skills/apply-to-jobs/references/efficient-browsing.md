# Batch prescreening and compact observations

## Prescreen without losing evidence

Collect roughly 10-20 candidates at a time, or fewer for a targeted review. Use available structured connectors, official public job feeds, or search/listing pages. Follow tool permissions; never extract private browser sessions, call hidden endpoints, or bypass access restrictions. Search snippets can discover candidates but do not prove eligibility or closure.

Store one record per candidate in `private/prescreen.jsonl`:

```json
{"company":"Example","title":"Software Engineer Intern","url":"https://example.com/jobs/123","requisition":"123","retrieved_at":"ISO timestamp","location":"US","employment_type":"internship","graduation_window":null,"start_date":null,"mandatory_experience":null,"sponsorship":null,"citizenship":null,"evidence":[{"field":"location","source_url":"https://example.com/jobs/123","excerpt":"United States"}],"decision":"detail_review","reason":"Graduation eligibility not yet established"}
```

- Null means unknown. Do not turn absent text into a negative requirement or a positive sponsorship promise.
- Possible decisions: `shortlist`, `detail_review`, `skip`, `duplicate`. This file is screening evidence, not a submission ledger. Use `jobs.py` for the application record and duplicate check.
- Skip only on explicit current evidence that conflicts with the profile/user criteria. Preserve the entire qualifying sentence, including exceptions and whether it is required or preferred.
- Resolve aliases and suspicious near-duplicates against existing application records. Do not assume a spelling difference or a second ATS link identifies a new role. Park ambiguous prior submissions.
- Before opening a shortlisted application, read the full official description once and confirm employer, role, location, and eligibility. If bulk sources omit a fact, inspect the official detail; do not reject solely because extraction failed.
- Save the full description privately once. Later decisions may use the compact evidence record; reread the relevant source when a conflict or update appears.

## Read what changed, with coverage checks

Use the environment's documented browser APIs. Prefer a form/section-scoped DOM or accessibility observation; fall back to a screenshot where textual state is insufficient. Do not cache screen coordinates or reuse stale accessibility indices.

1. On first entry, inventory every form section and reachable step. Capture labels, required/optional markers, types, values, option labels, help text, uploads, consent language, eligibility statements, errors, and progress/submit controls. Include relevant content outside the form element. This initial observation must establish coverage, not simply match a few keywords.
2. Keep that inventory and the current URL/employer identity in working state. Avoid repeatedly returning navigation menus, cookie boilerplate, the full job description, or unrelated page content.
3. Fill a small deterministic group of known independent fields. Then refresh the active section and error/progress state. If an answer reveals conditional fields, enumerate those before continuing. Choosing a dropdown value or uploading a file can also change the form.
4. After navigation, a new step, a modal, an unexpected result, or missing labels, widen the read immediately. Incomplete compact output is a reason to inspect more, never a reason to guess.
   Some browser text snapshots omit email or telephone values even when they are visibly filled. Use a focused screenshot when a value is missing or conflicts with the observed action; do not repeatedly refill it or assume success from the fill call alone. An upload is complete only when the expected filename is shown and any upload-progress state has cleared.
5. Before submission or a user preview, audit all sections: actual values, selected option labels, required fields, empty optional fields, attached documents, consents, eligibility answers, and visible errors. Verify autocomplete choices are selected, not merely typed. Check available browser validity indicators without sending the form.
6. After an authorized submission, inspect a real success signal. A pressed button, disabled control, navigation, or absence of an error is not proof of receipt.

Compact observation reduces repeated context, not the required verification. It cannot guarantee that server-only validation will pass before submission. Do not change resume tailoring, rendering, or document-verification policy as part of this optimization; follow the existing document instructions and the user's overrides.
