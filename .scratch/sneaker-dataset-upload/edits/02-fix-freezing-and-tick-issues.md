# Edit 02: Fix False-Positive Spec Freezing & Update Issue Checkboxes

## Requested Change
User stated:
> "คือว่ามันฟรีซตอนเล้าหนึ่งใช่ไหมตอนที่มันกำลังทำ คือถ้าตอนกำลังทำอยู่แล้วก็กลับไปติ๊กด้วยไง แต่ตอนนี้คือมันทำเสร็จแล้วมันก็ไม่ติ๊ก แล้วกูจะรู้ไหมว่ามันทำเสร็จอันไหนบ้าง เก็ตป่ะ แล้วก็พอมันไม่ติ๊กตั้งแต่ตอนที่ให้เริ่มทำ มันก็ต้องกลับไป edit เพราะว่ากูไม่ชอบอยู่ดีไง ก็กลายเป็น feedback ใหม่ ก็กลับไปแก้หน่อย ก็ไปอ่าน feedback ด้วยว่าทำไมถึงต้องทำอย่างนั้น feedback แล้วก็ได้ edit ด้วยเห็นไหม ก็ไปดูดิ"

The user identified that premature freezing in Round 1 prevented checking off completed tasks in `issues/*.md`. This left the user unaware of which tasks were finished, creating a redundant feedback-and-edit loop.

## Rationale & Impact
- **Root Cause**: `.agents/hooks/pre_tool_spec_enforcer.py` contained a naive message-count heuristic (`len(post_spec_user_times) >= 2`) that prematurely locked `issues/*.md` during Round 1 execution. It also treated issue checkbox updates (`- [x]`) as forbidden spec alterations.
- **Pain Point**: When work finished, `issues/*.md` remained completely unchecked (`[ ]`), giving zero visibility into actual feature completion.
- **Impact**: Removing the message counter and unblocking issue checkbox updates allows real-time progress tracking in Round 1 and lets issue files reflect true task completion.

## Planned Changes & Acceptance Criteria
- [x] Refactor `.agents/hooks/pre_tool_spec_enforcer.py` to remove the message-counter heuristic (`len(post_spec_user_times) >= 2`).
- [x] Ensure `issues/*.md` can have checklists `- [x]` and statuses updated without being blocked as a frozen spec.
- [x] Update `.scratch/sneaker-dataset-upload/issues/01-preflight-and-single-image-verification.md` with completed checkboxes `[x]` and `Status: done`.
- [x] Update `.scratch/sneaker-dataset-upload/issues/02-bulk-dataset-upload-and-split.md` with completed checkboxes `[x]` and `Status: done`.
- [x] Update `.scratch/sneaker-dataset-upload/issues/03-roboflow-auto-label-and-yolo-export.md` to reflect ready scripts and mark remaining manual UI steps clearly.
- [x] Record feedback in `feedback/02-allow-issue-checkbox-ticks.md` and complete incident report in `incident-spec-freeze.md`.
