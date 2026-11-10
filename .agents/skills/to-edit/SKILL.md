---
name: to-feedback
description: Record the user's raw feedback every time they react to a finished build and ask for a change — whether they dislike something, want a small tweak, like it and want to extend it, or report a bug. A companion to to-edit; it only logs what the user said and what was changed, with no analysis or interpretation. Make sure to use this skill whenever the user responds to a build in a session that already has spec.md and issues/ — e.g. "ไม่ถูกใจ", "แก้หน่อย", "ขอปรับ", "ดีแล้วแต่ขอเพิ่ม", "ไม่เอาแบบนี้", "เปลี่ยนเป็น…", "tweak this", "change this", "can you adjust" — even if the user never says the word feedback.
---

# To Feedback

A companion to `to-edit`. It does one job: **log the user's raw feedback** each time they ask for a change in the existing flow (spec → tickets → edit).

It does not analyze, find root causes, or summarize patterns. The point is only to make sure that what the user said, and what was actually changed, is written down while it is fresh, so it can be read back later instead of reconstructed from memory.

## Why log every change request, not only complaints

Users ask for changes for several different reasons, and the non-negative ones are worth as much as the complaints:

- They dislike something and want it changed.
- They are fine with it but want a small improvement.
- They like it and want to extend it in a new direction.
- They found a bug or something that doesn't work.

A user who keeps asking for changes usually wants to keep building on the work, not abandon it. So never assume every piece of feedback is a criticism. Record what the user actually said and let the label reflect it.

## Scope (keep it narrow)

**Do**
- Quote the user's own words verbatim in a blockquote.
- Record what the user asked to have changed and which files were actually touched.
- Attach exactly one signal label.
- Pair the log with the edit ticket by using the same number.

**Don't**
- Don't write a cause or root cause unless the user stated a reason themselves. If they gave none, write "Not stated". A guessed reason sits in the file looking like something the user said, and anyone reading it later would take it as fact.
- Don't derive rules, patterns, or lessons.
- Don't judge whether the user is happy or unhappy. If it isn't clear, use the `unclear` label.
- Don't edit or rewrite `spec.md` or `issues/*`. They are frozen once Round 1 is complete.
- Don't hold up the edit. Logging takes seconds and happens before or alongside the edit ticket; it is not an approval gate.

## When to use

Use it in Round 2+ of the current session: `.scratch/<feature-slug>/spec.md` and `issues/*.md` already exist, and the user is responding to something that was built.

If the current session has no spec or issues yet, it is still Round 1. Do `to-spec` and `to-tickets` first; there is nothing to log yet.

If the feature folder belongs to a past session, don't add anything to it. Start a new folder, following the rules in `to-edit`.

## Steps

1. **Find the current feature folder**, the one created in this session under `.scratch/<feature-slug>/`.
2. **Pick the number.** Look at `.scratch/<feature-slug>/edits/` and use the same number as the edit ticket about to be written (`01`, `02`, `03`, …). Matching numbers keep each log paired with its edit.
3. **Write the file** at `.scratch/<feature-slug>/feedback/<NN>-<slug>.md` using the template below, with the same slug as the edit ticket.
4. **Carry on** with the edit ticket and the change as `to-edit` describes.
5. **After the change is made**, come back to the same file and fill in "What was actually changed". Update the one file; don't create a new one.

## Signal labels

Pick the single label that best matches what the user said.

| Label | Use when |
|---|---|
| `dislike` | The user says or clearly shows they don't like what they got |
| `refine` | The user is fine with it and wants a detail adjusted |
| `extend` | The user likes it and wants to add to it or take it further |
| `bug` | Something doesn't work or the result is wrong |
| `unclear` | The wording doesn't let you tell. Don't guess. |

## Template

```markdown
# Feedback <NN>: <short title>

**Feature**: <feature-slug>
**Linked edit**: edits/<NN>-<slug>.md
**Signal**: dislike | refine | extend | bug | unclear

## What the user said (verbatim)
> <the user's message exactly as written; no rewording, no summary>

## Reason the user gave
<only what the user actually said; if none, write "Not stated">

## What the user asked to change
- <short list, as requested>

## What was actually changed (fill in after the edit)
- <files / parts touched>
```

## Examples

**Input** The user writes: "ปุ่มดูแข็งไปหน่อย อยากให้นุ่มกว่านี้ แต่เลย์เอาต์โอเคแล้วนะ"

**Output** `feedback/02-soften-button.md`
- Signal: `refine` (the user says the layout is fine and only wants the button adjusted)
- Verbatim: the whole sentence above
- Reason the user gave: "ดูแข็งไปหน่อย"
- Asked to change: make the button feel softer

Don't add something like "because it lacks spring motion". The user didn't say that.

**Input** The user writes: "ดีเลย ขอเพิ่มโหมดมืดด้วย"

**Output** Signal: `extend`. Reason the user gave: "Not stated". Asked to change: add a dark mode.

**Input** The user writes: "อืม... ไม่รู้สิ ลองเปลี่ยนสีดู"

**Output** Signal: `unclear`. Reason the user gave: "Not stated". Asked to change: try a different color.