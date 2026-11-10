# Feedback 03: Lateral Side-View Vertical Tripwire & Floor Alignment

**Feature**: core-video-pipeline
**Linked edit**: edits/03-lateral-side-view-vertical-tripwire.md
**Signal**: dislike

## What the user said (verbatim)
> แก้ไขเรื่องเส้นทำไมอยู่ด้านบนมันควรที่อยู่ใต้เท้าและเราบอกว่ารูปแบบ video จะเป็นด้านข้างด้วยอันนี้ทำไมตาม plan adr ไม่ถูกไจ และ ไม่แสดงเป็นvideo ให้ดู ไม่ถูกใจเหมือนกันและไม่รู้ทำไม adr ไม่เคิดเรื่องนี้ไว้ด้วยไม่ถูกใจเหมือนกัน

## Reason the user gave
เส้นอยู่ด้านบนตัดผ่านหัว/หน้าผาก แทนที่จะเป็นแนวตั้งตัดผ่านระดับการก้าวเดิน/ใต้เท้าตามมุมกล้องมองด้านข้างทางเดิน (Lateral Side View) ที่เคยระบุไว้

## What the user asked to change
- เปลี่ยนแนวเส้น Tripwire จากเส้นแนวนอน (y=360) เป็นเส้นแนวตั้งผ่ากึ่งกลางตามข้อกำหนด Lateral Side View ใน ADR-0005 (x = w/2 หรือ x=960 ใน 1080p) เพื่อให้คนเดินจากซ้ายไปขวา (Zone A -> Zone B) ตัดผ่านเส้นด้วยจุด Ground Anchor ที่เท้า
- ให้ความยาวเส้นและพิกัดรองรับขนาดภาพจริง (1920x1080) โดยอัตโนมัติ
- วาดแนวเส้นเสมือน ลูกศรทิศทาง A -> B และขอบเขตพื้นให้ชัดเจนตรงตามมุมมองด้านข้างในรูปตัวอย่าง

## What was actually changed (fill in after the edit)
- Realigned tripwire geometry to Lateral Side View per ADR-0005: replaced horizontal line with vertical dividing line down the middle of the frame (`x = w // 2`, $x=960$ on 1080p).
- Updated `TripwireZone` to handle vertical line crossing from Left to Right ($A \to B$) at the Ground Anchor Point ($P_{anchor}$ at feet level).
- Enhanced HUD overlay: draws vertical neon line, directional arrow pointing Left to Right, Zone A (Entry) and Zone B (Exit) labels, and lower-body 30% ROI outline.
- Added tests for vertical lateral crossing (`test_tripwire_vertical_lateral_side_view_crossing` and `test_pipeline_lateral_side_view_end_to_end_integration`). All 26 tests pass.
