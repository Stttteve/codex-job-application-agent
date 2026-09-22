# Codex Job Application Agent

An open-source Codex skill that can find matching jobs, tailor application documents, submit authorized applications, prevent duplicate submissions, and monitor an application inbox for new interview or online-assessment invitations.

The email tracker is read-only. It reports new interviews, recruiter screens, scheduling requests, OAs, coding assessments, take-home assignments, offers, deadlines, and other required actions. It ignores routine receipts and stays quiet when nothing has changed.

## Features

- Applies to a user-defined number of jobs within explicit role, location, graduation-date, and sponsorship criteria.
- Creates a tailored resume and, when requested by the form, a cover letter for each application.
- Deduplicates jobs across source URLs and ATS links.
- Logs every reviewed posting and only counts applications with visible confirmation.
- Uses an already connected inbox or signed-in webmail for verification and response monitoring.
- Deduplicates email alerts without storing message bodies, verification codes, assessment tokens, or private links.
- Keeps all candidate data and generated documents under the gitignored `private/` directory.

## Requirements

- Codex desktop with browser access
- Python 3.9 or newer
- [`uv`](https://docs.astral.sh/uv/) for PDF resume and cover-letter rendering
- An email connector or a signed-in webmail tab if email monitoring is enabled

## Install

```bash
git clone https://github.com/Stttteve/codex-job-application-agent.git
cd codex-job-application-agent
./scripts/bootstrap.sh
ln -s "$PWD/skills/apply-to-jobs" "$HOME/.codex/skills/apply-to-jobs"
```

If that skill path already exists, remove the old link or copy and then create the link again. Restart Codex after installing or updating the skill.

Fill `private/profile.md` and `private/resume.md` with truthful candidate data. The templates explain the expected fields. Never commit the `private/` directory.

## Use

Invoke the skill in Codex with `$apply-to-jobs`, for example:

> Use $apply-to-jobs to apply to 20 US software engineering new-grad roles that do not explicitly say they will not sponsor. Do not apply twice to the same role.

Useful local commands:

```bash
./run jobs status
./run jobs report
./run email-tracker status
```

To monitor responses, create a recurring Codex task that invokes `$apply-to-jobs` in response-tracking mode and checks the inbox every 30 minutes. The task should report only new actionable messages in the current chat and remain silent otherwise. The skill records alert fingerprints in `private/email-tracker.json` so the same message is not announced twice.

The agent never starts an assessment, schedules an interview, replies to mail, or changes mailbox state. Those actions stay with the candidate.

## Privacy

Candidate data, resumes, cover letters, application records, email state, and generated PDFs belong under `private/`, which is excluded from version control. Browser-managed passwords and inbox credentials must never be written into this repository.

Before publishing a fork, inspect staged files:

```bash
git diff --cached --stat
git grep -n -i -E 'gmail\.com|usc\.edu|@example\.com' -- ':!README.md'
```

## Attribution

This project is derived from [LuizFelipeBarbosa/job-application-skill](https://github.com/LuizFelipeBarbosa/job-application-skill) at commit `a5196571f0d5b7a79c330136b6d61b31b6948b0c` and is distributed under the MIT License. See [NOTICE.md](NOTICE.md) for details.

## Disclaimer

Review the skill instructions and your candidate profile before using automatic submission. You are responsible for the accuracy of submitted information and for following each job site's terms.
