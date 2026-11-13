# Scheduling, Logs and Operational Visibility

**Level: Beginner | Learning draft | Independent review pending**

Goal: make a repeatable command observable before scheduling it. Prerequisites: [incremental extraction](incremental-extraction.md). Allow two hours for manual runs and log inspection, then a separate scheduling exercise if desired. Nothing in this guide installs a scheduled job on your computer.

## Start with one reliable manual command

Use the refreshed [starter ZIP](../../../downloads/canteen-starter.zip). Run the seed once, then the runner. Default files live beside the scripts. Optional relative arguments are resolved from the terminal's current directory, so prefer full paths for scheduling.

```text
python seed_source.py
python run_incremental.py
```

The seed remains static unless a learning exercise appends an event. Scheduling repeated runs of an unchanged source demonstrates operation, not a live feed of business activity. Do not schedule the seed as though it were ingestion.

## Read status correctly

| Process exit code | Meaning | Response |
| --- | --- | --- |
| 0 | Batch committed without new rejected rows | Check remaining events and freshness; unresolved earlier quarantine may still exist |
| 2 | Batch committed with rejected rows | Inspect quarantine and its business impact; do not blindly retry as a technical failure |
| 1 | Runner failed | Investigate logs and target state before retry; uncommitted batch changes roll back |

Argument parsing or interpreter errors can also produce nonzero codes. Inspect the message and log rather than interpreting every code 2 as a committed run. The `committed_with_rejects` log event distinguishes the runner's quality warning.

## Structured logs

`pipeline.log` contains JSON records with UTC timestamp, run ID and event type. Completion records include checkpoint, extracted/pending counts, per-batch outcomes and report rows. A failure records its exception type, without raw order payloads or credentials. The log rotates at approximately 1 MB with two backups. This is local logging, not a monitored alert service.

A run normally writes `started` and then either `committed`, `committed_with_rejects` or `failed`. A crash may leave only `started`. Logs are not transactionally committed with the database: if a process stops after commit but before its final log, inspect the checkpoint and rerun safely rather than assuming nothing committed.

## Inspect without guessing

Read the last lines of `pipeline.log` in a text editor. Match the run ID, not just the most recent timestamp. Compare the checkpoint, pending count and current report. A clean no-op run does not resolve yesterday's rejected records. A recent run timestamp does not prove source freshness; a real pipeline should also observe source activity/expected delivery and business dates.

Exercise: run `python run_incremental.py --fail-before-commit`, expect exit 1 and a failed log. Remove the flag and rerun. The next lesson explains how to prove recovery.

## Optional Windows scheduling exercise

Once the manual command and recovery checks work, Windows Task Scheduler can launch it without a paid orchestrator. Follow [Microsoft's scheduling documentation](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/schtasks-create). Configure these fields in a task action:

- **Program:** full path of your working Python interpreter, not a guessed command alias. Obtain it with `python -c "import sys; print(sys.executable)"`.
- **Arguments:** the full, quoted path to `run_incremental.py`; add full `--source`, `--db` and `--log` paths if using custom files.
- **Start in:** the extracted starter folder, without the script filename.
- **Trigger:** choose a suitable local time; distinguish it from UTC log timestamps.
- **Overlap rule:** do not start a second instance while one is running.

Use your normal account and local synthetic files; no administrator account or stored password is needed for a basic logged-in exercise. Test Run once, inspect history/logs and verify the database result. A sleeping or powered-off laptop may miss a trigger depending on settings. Turn the practice task off when finished. We test the Python command in CI; we do not claim every OS scheduler configuration is tested.

macOS/Linux learners can continue running manually or use their OS scheduler's official instructions with equivalent path, overlap, time-zone and exit-status checks. Cloud orchestration is an optional later extension, not required here.

## Completion evidence

Save one successful run summary, one quality-warning summary and one failed-run summary. Explain an action for each and which freshness signals are missing. Ask AI to critique your runbook using an example where the process succeeded but the source stopped sending data.

Sources checked 13 November 2026: [Python logging](https://docs.python.org/3/library/logging.html), [Microsoft task creation](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/schtasks-create).

Next: [Recovery and runbook](recovery-and-runbook.md).
