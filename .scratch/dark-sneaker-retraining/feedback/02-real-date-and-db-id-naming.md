# Feedback 02: Real Wall-Clock Date and Sequence Prefix for Captured Evidence

**Feature**: dark-sneaker-retraining
**Linked edit**: edits/02-real-date-and-db-id-naming.md
**Signal**: refine

## What the user said (verbatim)
> จะรู้ได้ไงอันไหนเก่าใหม่
> แก้ให้หน่อย
> (Recommended) แก้การตั้งชื่อไฟล์และโฟลเดอร์: ให้ใช้วันที่เวลาปัจจุบันจริง (เช่น 2026-11-10) พร้อมใส่เลข DB ID นำหน้า (เช่น #00071_...) เพื่อให้เห็นชัดเจนทันทีว่ารูปไหนเก่า-ใหม่ และไม่ติดเป็นปี 1970

## Reason the user gave
ไฟล์ภาพและโฟลเดอร์ติดปี 1970 (เนื่องจาก timestamp จากวิดีโอเป็น relative offset เช่น 109s) และชื่อไฟล์ไม่มีเลขลำดับ ทำให้ผู้ใช้ดูไม่ออกว่ารูปไหนเป็นเหตุการณ์เก่าหรือใหม่

## What the user asked to change
- ใช้วันที่เวลาจริง (Wall-clock real time เช่น `2026-11-10`) สำหรับการจัดโฟลเดอร์และบันทึกเวลา
- ใส่เลขลำดับเหตุการณ์ / DB ID นำหน้าชื่อไฟล์ เช่น `event_00071_...` หรือ `71_...` เพื่อให้เรียงตามชื่อไฟล์แล้วรู้ทันทีว่าอันไหนเก่า-ใหม่

## What was actually changed (fill in after the edit)
- `src/storage/evidence_writer.py`: Added `event_id: Optional[int] = None` formatting 5-digit prefix (`{event_id:05d}_...`) and updated `_extract_date_str()` to prevent `1970-01-01` folders.
- `src/pipeline/coordinator.py`: Added `self.crossing_counter` sequence tracking and mapped relative video timestamps to current wall-clock date/time `datetime.now()`.
- `tests/unit/test_evidence_writer.py`: Added tests `test_evidence_writer_with_event_id_prefix` and `test_evidence_writer_fallbacks_for_epoch_1970`.
- All 42 unit and integration tests pass cleanly (`uv run pytest`).
