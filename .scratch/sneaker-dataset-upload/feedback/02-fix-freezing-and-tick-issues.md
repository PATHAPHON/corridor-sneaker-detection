# Feedback 02: Fix Premature Freezing and Update Issue Checkboxes

**Feature**: sneaker-dataset-upload
**Linked edit**: edits/02-fix-freezing-and-tick-issues.md
**Signal**: bug

## What the user said (verbatim)
> คือว่ามันฟรีซตอนเล้าหนึ่งใช่ไหมตอนที่มันกำลังทำ คือถ้าตอนกำลังทำอยู่แล้วก็กลับไปติ๊กด้วยไง แต่ตอนนี้คือมันทำเสร็จแล้วมันก็ไม่ติ๊ก แล้วกูจะรู้ไหมว่ามันทำเสร็จอันไหนบ้าง เก็ตป่ะ แล้วก็พอมันไม่ติ๊กตั้งแต่ตอนที่ให้เริ่มทำ มันก็ต้องกลับไป edit เพราะว่ากูไม่ชอบอยู่ดีไง ก็กลายเป็น feedback ใหม่ ก็กลับไปแก้หน่อย ก็ไปอ่าน feedback ด้วยว่าทำไมถึงต้องทำอย่างนั้น feedback แล้วก็ได้ edit ด้วยเห็นไหม ก็ไปดูดิ

## Reason the user gave
ระบบฟรีซตั้งแต่ตอน Round 1 กำลังทำ ทำให้ไม่ได้กลับไปติ๊ก [x] เมื่อทำเสร็จ ทำให้ผู้ใช้ไม่รู้ว่าอันไหนเสร็จแล้วบ้าง จนต้องวนกลับมาทำ edit ซ้ำซ้อน

## What the user asked to change
- แก้ระบบไม่ให้ฟรีซระหว่างทำใน Round 1 เพื่อให้กลับไปติ๊ก [x] ได้ทันทีเมื่อทำงานเสร็จ
- อัปเดตติ๊ก [x] ใน issues/*.md ให้ตรงกับความเป็นจริง เพื่อให้ผู้ใช้รู้ว่าแต่ละอันเสร็จไปถึงไหนแล้ว

## What was actually changed (fill in after the edit)
- Fixed `.agents/hooks/pre_tool_spec_enforcer.py`: removed the flawed heuristic Check 3 (`len(post_spec_user_times) >= 2`) and unblocked `issues/*.md` from being falsely treated as frozen specs. Checkbox updates (`- [x]`) and status changes now execute without restriction.
- Updated `.scratch/sneaker-dataset-upload/issues/01-preflight-and-single-image-verification.md` (`Status: done`, all checkboxes ticked `[x]`).
- Updated `.scratch/sneaker-dataset-upload/issues/02-bulk-dataset-upload-and-split.md` (`Status: done`, all checkboxes ticked `[x]`).
- Updated `.scratch/sneaker-dataset-upload/issues/03-roboflow-auto-label-and-yolo-export.md` (`Status: in-progress`, download script marked ready `[x]`, remaining Roboflow UI manual steps clearly listed).
- Documented full timeline and root cause in `.scratch/sneaker-dataset-upload/incident-spec-freeze.md`.
