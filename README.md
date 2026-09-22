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

Invoke the skill in Codex with `$apply-to-jobs`. Replace every value in angle brackets before sending a prompt.

### 1. First-time setup

Attach your current resume, then use:

```text
Use $apply-to-jobs to set up my private job-application workspace from the attached resume. Ask me only for candidate facts that are missing and cannot be inferred safely. Create private/profile.md, private/resume.md, and the base resume PDF. Do not submit any applications during setup. Never store my email password or verification codes.
```

Review the generated profile before starting an application batch.

### 2. Find and automatically submit a batch

```text
Use $apply-to-jobs to find and submit exactly <NUMBER> applications for <FULL-TIME OR INTERNSHIP> roles in the United States.

Target roles: <ROLE FAMILIES, FOR EXAMPLE SOFTWARE ENGINEER, PRODUCT ENGINEER, AI ENGINEER, HARDWARE ENGINEER, PRODUCT MANAGER, AI PRODUCT MANAGER>.
Graduation date for this batch: <MONTH YEAR>.
Location requirements: <LOCATIONS OR ANYWHERE IN THE US>.
Work authorization and sponsorship requirements: <COPY THE TRUTHFUL ANSWERS FROM YOUR PROFILE>.
Sources: <JOB LIST URLS OR SITES TO SEARCH>.

Automatically submit matching applications without asking me to approve each one. Do not apply to a role that explicitly conflicts with my sponsorship, work-authorization, graduation-date, location, or role requirements. Do not apply twice to the same role, including when the same posting appears on multiple sites or ATS URLs. Use the connected application inbox only when verification is required. Never invent candidate information. Count an application only after a visible submission confirmation. Continue until <NUMBER> applications are confirmed or all matching sources are exhausted, and send a progress update after every five confirmed applications.
```

Example:

> Use $apply-to-jobs to apply to 20 US software engineering new-grad roles that do not explicitly say they will not sponsor. Do not apply twice to the same role.

### 3. Continue a previous batch

```text
Use $apply-to-jobs to continue my most recent application batch until it reaches <NUMBER> confirmed applications. Read the existing application log first, do not resubmit any applied or uncertain prior attempt, keep the original search criteria, and automatically move to another matching role when one application is blocked.
```

### 4. Monitor interview and OA email

```text
Use $apply-to-jobs in response-tracking mode and create a recurring task that checks my connected application inbox every 30 minutes. Alert me in this chat only for a new interview, recruiter screen, scheduling request, online assessment, coding assessment, HackerRank, CodeSignal, Karat, take-home assignment, offer, deadline, or other required action. Include the company, role when known, event type, sender, subject, received time, deadline, and next step. Deduplicate every alert and stay silent when nothing has changed. Never reply, modify mail, open an assessment link, start a test, or expose or store verification codes. If inbox access expires, tell me once and remain quiet until access is restored.
```

Keep the application inbox signed in or connect an email tool that Codex can read. The tracker stores only a message fingerprint and the minimum metadata required for deduplication.

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
