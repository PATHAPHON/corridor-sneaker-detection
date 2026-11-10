# Incident Report: False-Positive Spec Freezing Gate during Task Implementation

- **Date:** 2026-11-10
- **Feature:** `sneaker-dataset-upload`
- **Originating Session:** `bca05775-67b8-4f41-98e8-93efeb000f16`
- **Impacted Files:** `.scratch/sneaker-dataset-upload/issues/01-preflight-and-single-image-verification.md` (and subsequent tickets 02, 03)

---

## 1. What Happened (Timeline Reconstruction)

1. **Step 61 (15:07:39)**: Agent created tracer tickets `01`, `02`, `03` under `.scratch/sneaker-dataset-upload/issues/`.
2. **User Input 1 (15:08:20)**: User sent `/setup-agent-and-glossary ก่อนที่จะเรื่มช่วย เพื่ม spce ทำ agent.md กับ glossary ให้หน่อย`.
3. **User Input 2 (15:08:37)**: User sent `เริ่ม`.
4. **Step 119 (15:10:57)**: Agent completed Ticket 01 and executed `write_file` to tick all checkboxes `- [x]` in `01-preflight-and-single-image-verification.md` and set `Status: done`.
5. **Step 120 (15:10:57)**: Pre-tool hook `.agents/hooks/pre_tool_spec_enforcer.py` intercepted and **HARD-DENIED** the tool call:
   ```text
   Encountered error in step execution: tool call denied by pre-tool hook:
   🚨 SPEC ENFORCEMENT GATE: Blocked modification to 'frozen_spec: .scratch/sneaker-dataset-upload/issues/01-preflight-and-single-image-verification.md'.
   Reason: 🚨 FROZEN SPEC/TICKETS: Modifying '.scratch/sneaker-dataset-upload/issues/01-preflight-and-single-image-verification.md' is forbidden!
   ```
6. **Step 121 (15:11:00)**: Agent inferred: *"The system enforces a strict rule: modifications to specification files (`*.md`) within the designated directory are blocked after the initial build phase. This indicates Ticket 01 has passed verification and is now frozen."*
7. **Consequence**: Agent was prevented from marking acceptance criteria as completed in `issues/*.md`. When user later asked to review and tick checkboxes, agent was forced to create Edit Ticket `01-complete-upload-and-address-review.md` to record completion outside the blocked `issues/` directory.

---

## 2. Root Cause Analysis

In `.agents/hooks/pre_tool_spec_enforcer.py`:

```python
# Lines 192-197: is_frozen_spec_target()
user_inputs = get_user_inputs(transcript_path)
if user_inputs:
    post_spec_user_times = [t for t in user_inputs if t >= (spec_creation - 2.0)]
    if len(post_spec_user_times) >= 2:
        return True, rel
```

### Flaws:
1. **Flawed Round 2 Heuristic**: Counting user messages `>= 2` after spec creation as proof that "Round 1 is completed" is invalid. Normal user interactions (e.g. asking for glossary setup, answering questions, or sending "เริ่ม") immediately trigger Check 3 before implementation even starts.
2. **Blocking Progress Updates**: The hook treats updating `- [ ]` to `- [x]` as "editing the specification", conflating contract modification with progress tracking.
3. **Status Schema Conflict**: Line 581 in `validate_scratch_write` strictly mandates `**Status:** ready-for-agent`, blocking status transitions to `done` or `in-progress`.

---

## 3. Recommended Remediation

1. Remove Check 3 (`len(post_spec_user_times) >= 2`) from `is_frozen_spec_target()`.
2. Allow `issues/*.md` modifications that strictly update checkbox states (`- [ ]` to `- [x]`) and ticket status during Round 1.
3. Only freeze `spec.md` and `issues/*.md` when `edits/` directory contains an active edit ticket or cross-session boundaries are crossed.
