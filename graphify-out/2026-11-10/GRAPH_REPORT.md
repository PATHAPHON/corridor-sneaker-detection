# Graph Report - my-cv  (2026-11-10)

## Corpus Check
- 141 files · ~424,499 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 4 file(s) not represented in the graph (top: (none) 2, .example 1, .lock 1)

## Summary
- 1155 nodes · 1806 edges · 108 communities (80 shown, 28 thin omitted)
- Extraction: 92% EXTRACTED · 8% INFERRED · 0% AMBIGUOUS · INFERRED: 150 edges (avg confidence: 0.92)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `d2685ac0`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- TrackedPerson
- Rules
- Diagnosing Bugs
- Test-Driven Development
- check_spec_in_workspace
- Process
- ADR-0001: Person Detection and Multi-Object Tracking Pipeline
- Set-Call: Universal Tool-Call & Command Error Correction Playbook
- 2. Step-by-Step Procedure
- ADR-NNNN: [Decision Title]
- hitl-loop.template.sh
- to-spec/SKILL.md
- 1. Core Tool Invocation Standards
- To Feedback
- Process
- Project Agent Guidelines (AGENTS.md Template)
- Project Glossary & Domain Invariants (GLOSSARY.md Template)
- EventRepository
- Feature Spec: Storage Persistence & Active Retraining Pipeline
- ADR-0002: Virtual Line Crossing and Tripwire Mechanism
- ADR-0003: Lower-Body ROI Extraction and Sneaker Detection
- ADR-0004: Event Logging, Image Evidence Storage, and Database Architecture
- ADR-0005: Camera Placement and Optical Geometry Specification (MacBook Webcam)
- Spec: Architecture Governance — AGENTS.md & GLOSSARY.md Synthesis
- AGENTS.md — Engineering Guidelines & Operational Standards
- Spec: Sneaker Dataset Ingestion & Auto-Box Annotation Pipeline
- 01-preflight-and-single-image-verification.md
- 02-bulk-dataset-upload-and-split.md
- 03-roboflow-auto-label-and-yolo-export.md
- 01-synthesize-agents-and-glossary.md
- cv2
- Edit 01: Complete Dataset Upload & Code Review Checklist Verification
- Feedback: Code Review and Ticket Checklist Update
- ADR-0007: Dark Footwear Robustness via Training-Time Augmentation vs Real-Time Preprocessing
- Feedback 02: Fix Premature Freezing and Update Issue Checkboxes
- Edit 02: Fix False-Positive Spec Freezing & Update Issue Checkboxes
- Spec: Sneaker Model Fine-Tuning & Evaluation Pipeline
- PipelineCoordinator
- 01-project-dependencies-and-hardware-preflight.md
- 02-sneaker-model-fine-tuning.md
- 03-metric-evaluation-and-model-export.md
- my-cv
- 2. การตัดสินใจเชิงสถาปัตยกรรม (ADR-0001 ถึง ADR-0007)
- Feature Spec: Core Video and Tracking Pipeline
- person_tracker.py
- coordinator.py
- is_frozen_spec_target
- 2. System Invariants & Non-Negotiable Rules
- test_storage.py
- 01-frame-source-abstraction.md
- 02-person-detection-and-tracking.md
- 03-virtual-line-tripwire.md
- 04-lower-body-roi-and-sneaker-inspection.md
- 05-decoupled-concurrency-and-main-loop.md
- 1.1 Core Video Pipeline Feature Inception & Delivery
- 3. Step-by-Step Execution Playbook for Next Agent
- FrameSource
- EvidenceWriter
- Edit 02: Real-time Live Video GUI Preview Window with Visual HUD
- numpy
- CameraFrameSource
- json
- pathlib
- test_preflight.py
- pre_tool_spec_enforcer.py
- test_sneaker_model.py
- Edit 03: Realign Tripwire to Lateral Side-View Vertical Geometry per ADR-0005
- Feedback 01: macOS AVFoundation Camera Backend
- evaluate_and_export.py
- Edit 03: Accurate Two-Foot Annotation & Verification Pipeline
- detect_session_role
- Feedback 03: Curate and Annotate Both Feet
- Edit 01: Implement Retraining Pipeline and Generate 5 Visual Augmentation Samples
- 01-sqlite-event-repository.md
- 02-evidence-image-writer.md
- 04-active-dataset-curation-and-export.md
- PipelineHud
- Feedback 01: Start Implementation and Request 5 Visual Augmentation Samples
- Real-Time Corridor Tripwire Footwear Inspection System
- PersonTracker
- 2. Immediate Next Steps for Next Feature
- VideoFileFrameSource
- SyntheticFrameSource
- Edit 05: Dark Sneaker Augmentation Strategy & ADR
- 4. บันทึกประวัติการ Prompt การทำงาน และการแก้ปัญหาอย่างละเอียด (Prompt Trace & Incident History)
- 5.3 ภาพเปรียบเทียบผลการตรวจจับจริง (Before vs After Evidence)
- 1. What Was Completed in This Session
- Edit 04: Annotate Occluded and Blurred Second Shoes
- Feedback 04: Annotate Occluded and Blurred Second Shoes
- Feedback 05: Dark Sneaker Augmentation Strategy & ADR
- 01-manifest-dataset-merger-with-oversampling.md
- 2. Immediate Next Steps for Next Feature
- 02-adr0007-training-time-augmentation-pipeline.md
- 03-dual-gate-evaluation-backup-and-visual-report.md
- 04-execute-retraining-promote-weights-and-verify.md
- 3. บันทึกกระบวนการทำงาน การสนทนากับ AI และการแก้ปัญหาตามบริบทจริง
- Feedback 02: Real-time Live Video GUI Preview
- 2. Immediate Next Steps for Next Agent
- Incident Report: False-Positive Spec Freezing Gate during Task Implementation
- 7. โครงสร้างโปรเจกต์และวิธีติดตั้งใช้งาน
- Edit 01: Implement Storage Persistence & Active Retraining Pipeline
- Edit 02: Real Wall-Clock Date and Sequence Prefix for Captured Evidence
- Feedback 01: Implement Storage Persistence & Active Retraining Pipeline
- get_user_inputs
- 1. What Was Completed

## God Nodes (most connected - your core abstractions)
1. `PipelineCoordinator` - 36 edges
2. `FrameSource` - 31 edges
3. `EventRepository` - 29 edges
4. `SyntheticFrameSource` - 27 edges
5. `CameraFrameSource` - 24 edges
6. `TrackedPerson` - 21 edges
7. `VideoFileFrameSource` - 20 edges
8. `PipelineConfig` - 19 edges
9. `CrossingRecord` - 18 edges
10. `TripwireZone` - 18 edges

## Surprising Connections (you probably didn't know these)
- `4.4 Session 8: การจัดการเหตุการณ์ขัดข้อง (Incident) ของ Pre-Tool Spec Enforcer Hook` --references--> `is_frozen_spec_target()`  [INFERRED]
  README.md → .agents/hooks/pre_tool_spec_enforcer.py
- `3. Recommended Remediation` --references--> `is_frozen_spec_target()`  [INFERRED]
  .scratch/sneaker-dataset-upload/incident-spec-freeze.md → .agents/hooks/pre_tool_spec_enforcer.py
- `1. What Was Completed` --references--> `validate_scratch_write()`  [INFERRED]
  .scratch/handoffs/2026-11-10-172321-handoff.md → .agents/hooks/pre_tool_spec_enforcer.py
- `Flaws:` --references--> `validate_scratch_write()`  [INFERRED]
  .scratch/sneaker-dataset-upload/incident-spec-freeze.md → .agents/hooks/pre_tool_spec_enforcer.py
- `Encapsulation Rules:` --references--> `FrameSource`  [INFERRED]
  AGENTS.md → src/capture/base.py

## Import Cycles
- None detected.

## Communities (108 total, 28 thin omitted)

### Community 0 - "TrackedPerson"
Cohesion: 0.09
Nodes (12): Feedback 03: Lateral Side-View Vertical Tripwire & Floor Alignment, Reason the user gave, What the user asked to change, What the user said (verbatim), What was actually changed (fill in after the edit), TrackedPerson, MockLateralTracker, MockTracker (+4 more)

### Community 1 - "Rules"
Cohesion: 0.08
Nodes (25): 1.1 Lifecycle Flow, 1.2 Execution Workflow & AI Duties, 1. Answer first, 1. Delivery Lifecycle & PR Workflow, 1. Think Before Coding, 2. Kill ceremony, 2. Simplicity First, 3. Short word (+17 more)

### Community 2 - "Diagnosing Bugs"
Cohesion: 0.13
Nodes (14): Completion criterion: a tight loop that goes red, Diagnosing Bugs, Minimise, Non-deterministic bugs, Phase 1: Build a feedback loop, Phase 2: Reproduce + minimise, Phase 3: Hypothesise, Phase 4: Instrument (+6 more)

### Community 3 - "Test-Driven Development"
Cohesion: 0.15
Nodes (10): Designing for Mockability, When to Mock, Anti-patterns, Rules of the loop, Seams: where tests go, Test-Driven Development, What a good test is, Bad Tests (+2 more)

### Community 4 - "check_spec_in_workspace"
Cohesion: 0.20
Nodes (7): check_spec_in_workspace(), get_project_root(), get_spec_creation_time(), is_production_code_modification(), main(), validate_edit_ticket_content(), validate_scratch_write()

### Community 5 - "Process"
Cohesion: 0.15
Nodes (12): 1. Gather context, 2. Explore the codebase (optional), 3. Draft vertical slices, 4. Quiz the user, 5. Publish the tickets to the configured tracker, Acceptance criteria, Blocked by, <NN>: <Ticket title> (+4 more)

### Community 6 - "ADR-0001: Person Detection and Multi-Object Tracking Pipeline"
Cohesion: 0.15
Nodes (12): ADR-0001: Person Detection and Multi-Object Tracking Pipeline, Alternative 1: YOLO Small / Medium (`YOLOv8s` / `YOLOv8m`), Alternative 1: YOLOv8 Nano (`yolov8n.pt`), Alternative 2: YOLO-Pose (Human Pose Estimation), Alternative 3: Background Subtraction + Optical Flow / Contour Tracking, Alternatives Considered, Consequences, Context (+4 more)

### Community 7 - "Set-Call: Universal Tool-Call & Command Error Correction Playbook"
Cohesion: 0.18
Nodes (10): 1. Database Schema & Query Execution (Zero Schema Guessing), 2. File Reading, Creation & Directory Paths (Zero Path Guessing), 3. Git Commands & Diff Safety, 4. Shell Quoting & Inline Python Scripts, 5. Python Unittest Execution, 6. Test Runners & Typecheck CLI Calls, 7. Background Tasks & Subagent Management (`manage_task` & `invoke_subagent`), 8. Spec Enforcement & Hook Gating (Zero Probing & Immediate Halt) (+2 more)

### Community 8 - "2. Step-by-Step Procedure"
Cohesion: 0.18
Nodes (10): 1. Generate `AGENTS.md`, 1. Process Flow, 2. Generate `GLOSSARY.md`, 2. Step-by-Step Procedure, 3. When to Invoke `setup-agent-and-glossary`, Setup Agent & Glossary: Architecture-to-Guideline Synthesizer, Step 1: Scan for ADRs in `docs/adr/`, Step 2A: Guide ADR Creation (If No ADR Exists) (+2 more)

### Community 9 - "ADR-NNNN: [Decision Title]"
Cohesion: 0.18
Nodes (10): ADR-NNNN: [Decision Title], Alternative 1: [Name], Alternative 2: [Name], Alternatives Considered, Consequences, Context, Decision, Negative (+2 more)

### Community 10 - "hitl-loop.template.sh"
Cohesion: 0.83
Nodes (3): capture(), hitl-loop.template.sh script, step()

### Community 11 - "to-spec/SKILL.md"
Cohesion: 0.20
Nodes (9): Further Notes, Implementation Decisions, Out of Scope, Problem Statement, Process, Required Workspace Structure (`.scratch/<feature-slug>/`), Solution, Testing Decisions (+1 more)

### Community 12 - "1. Core Tool Invocation Standards"
Cohesion: 0.22
Nodes (8): 1. Core Tool Invocation Standards, 2. Trace Harvesting & Distillation Workflow, 3. When to Run `setup-core`, A. Command Execution (`run_command`), B. Knowledge Graph Traversal (`graphify`), C. File Operations (`read_file`, `write_file`, `edit_file`), Setup-Core: Tool Invocation Standards & Evolution Distiller, Step-by-Step Distillation Process:

### Community 13 - "To Feedback"
Cohesion: 0.22
Nodes (8): Examples, Scope (keep it narrow), Signal labels, Steps, Template, To Feedback, When to use, Why log every change request, not only complaints

### Community 14 - "Process"
Cohesion: 0.25
Nodes (7): 1. Pin the fixed point, 2. Identify the spec source, 3. Identify the standards sources, 4. Spawn both sub-agents in parallel, 5. Aggregate, Process, Why two axes

### Community 15 - "Project Agent Guidelines (AGENTS.md Template)"
Cohesion: 0.25
Nodes (7): 1. Project Stack, 2. Build, Run & Test Commands, 3. Code Style & Conventions, 4. Architecture & Module Boundaries, 5. Boundaries (Never-Touch Rules), 6. Standard Delivery Workflow, Project Agent Guidelines (AGENTS.md Template)

### Community 16 - "Project Glossary & Domain Invariants (GLOSSARY.md Template)"
Cohesion: 0.50
Nodes (3): 1. Domain Terminology, 2. System Invariants & Non-Negotiable Rules, Project Glossary & Domain Invariants (GLOSSARY.md Template)

### Community 17 - "EventRepository"
Cohesion: 0.11
Nodes (7): 1. Executive Summary & Active State, main(), DatasetExporter, ExportSummary, EventRepository, test_dataset_exporter_creates_yolo_structure_and_labels(), test_sqlite_repository_insert_and_query_by_track_id()

### Community 19 - "Feature Spec: Storage Persistence & Active Retraining Pipeline"
Cohesion: 0.15
Nodes (12): Execution Roadmap (Order of Operations), Feature Spec: Storage Persistence & Active Retraining Pipeline, Further Notes, Implementation Decisions, Out of Scope, Phase 1: Storage Layer & Pipeline Integration, Phase 2: Active Dataset Export & Curation, Phase 3: Model Retraining & Deployment (+4 more)

### Community 20 - "ADR-0002: Virtual Line Crossing and Tripwire Mechanism"
Cohesion: 0.17
Nodes (11): ADR-0002: Virtual Line Crossing and Tripwire Mechanism, Alternative 1: Bidirectional Processing (Evaluating both A → B and B → A), Alternative 2: Custom Vector Mathematics (No External CV Library), Alternative 3: Dual Virtual Lines / Polygon ROI Zone, Alternatives Considered, Consequences, Context, Decision (+3 more)

### Community 21 - "ADR-0003: Lower-Body ROI Extraction and Sneaker Detection"
Cohesion: 0.17
Nodes (11): ADR-0003: Lower-Body ROI Extraction and Sneaker Detection, Alternative 1: Multi-Style Footwear Detection (Boots, Flip-flops, Sandals, Loafers), Alternative 2: Manual Bounding Box Labeling from Scratch, Alternative 3: Full-Frame Continuous Sneaker Detection, Alternatives Considered, Consequences, Context, Decision (+3 more)

### Community 22 - "ADR-0004: Event Logging, Image Evidence Storage, and Database Architecture"
Cohesion: 0.18
Nodes (10): ADR-0004: Event Logging, Image Evidence Storage, and Database Architecture, Alternative 1: Flat JSON Lines (`events.jsonl`) Only, Alternative 2: Remote PostgreSQL / Cloud Database, Alternatives Considered, Consequences, Context, Decision, Negative (+2 more)

### Community 23 - "ADR-0005: Camera Placement and Optical Geometry Specification (MacBook Webcam)"
Cohesion: 0.14
Nodes (13): 1. Physical Setup & Layout, 2. Virtual Tripwire (Vertical Line), 3. Visual Detection HUD & Annotations, ADR-0005: Camera Placement and Optical Geometry Specification (MacBook Webcam), Alternative 1: High Ceiling External Mount (> 2.5m), Alternative 2: Front-Facing Head-On View (Walking Directly Toward MacBook), Alternatives Considered, Consequences (+5 more)

### Community 24 - "Spec: Architecture Governance — AGENTS.md & GLOSSARY.md Synthesis"
Cohesion: 0.25
Nodes (7): Implementation Decisions, Out of Scope, Problem Statement, Solution, Spec: Architecture Governance — AGENTS.md & GLOSSARY.md Synthesis, Testing Decisions, User Stories

### Community 25 - "AGENTS.md — Engineering Guidelines & Operational Standards"
Cohesion: 0.08
Nodes (23): 1. Project Overview & Tech Stack, 2. Build, Run & Test Commands, 3. Code Style & Architecture Conventions, 4. Architecture & Module Boundaries, 5. Boundaries (Never-Touch Rules), 6. Standard Delivery Workflow, AGENTS.md — Engineering Guidelines & Operational Standards, Clean 10-Line Pattern (Decoupled Stage Architecture) (+15 more)

### Community 26 - "Spec: Sneaker Dataset Ingestion & Auto-Box Annotation Pipeline"
Cohesion: 0.22
Nodes (8): Further Notes, Implementation Decisions, Out of Scope, Problem Statement, Solution, Spec: Sneaker Dataset Ingestion & Auto-Box Annotation Pipeline, Testing Decisions, User Stories

### Community 31 - "cv2"
Cohesion: 0.13
Nodes (10): main(), segment_feet_boxes(), apply_erasing(), apply_flip_and_scale(), apply_hsv_jitter(), apply_rotation(), draw_boxes(), generate_samples() (+2 more)

### Community 32 - "Edit 01: Complete Dataset Upload & Code Review Checklist Verification"
Cohesion: 0.22
Nodes (8): Acceptance Criteria, Edit 01: Complete Dataset Upload & Code Review Checklist Verification, Planned Changes, Rationale & Impact, Requested Change, Ticket 01: Preflight and Single-Image Verification, Ticket 02: Bulk Dataset Upload and Split, Ticket 03: Roboflow Auto-Label and YOLO Export Preparation

### Community 33 - "Feedback: Code Review and Ticket Checklist Update"
Cohesion: 0.50
Nodes (3): Feedback: Code Review and Ticket Checklist Update, What was asked, What was changed

### Community 34 - "ADR-0007: Dark Footwear Robustness via Training-Time Augmentation vs Real-Time Preprocessing"
Cohesion: 0.18
Nodes (10): ADR-0007: Dark Footwear Robustness via Training-Time Augmentation vs Real-Time Preprocessing, Alternative 1: Real-Time CLAHE (Contrast Limited Adaptive Histogram Equalization), Alternative 2: Multi-Frame Burst Capture with Laplacian Sharpness Selection, Alternatives Considered, Consequences, Context, Decision, Negative (+2 more)

### Community 35 - "Feedback 02: Fix Premature Freezing and Update Issue Checkboxes"
Cohesion: 0.33
Nodes (5): Feedback 02: Fix Premature Freezing and Update Issue Checkboxes, Reason the user gave, What the user asked to change, What the user said (verbatim), What was actually changed (fill in after the edit)

### Community 36 - "Edit 02: Fix False-Positive Spec Freezing & Update Issue Checkboxes"
Cohesion: 0.40
Nodes (4): Edit 02: Fix False-Positive Spec Freezing & Update Issue Checkboxes, Planned Changes & Acceptance Criteria, Rationale & Impact, Requested Change

### Community 37 - "Spec: Sneaker Model Fine-Tuning & Evaluation Pipeline"
Cohesion: 0.22
Nodes (8): Further Notes, Implementation Decisions, Out of Scope, Problem Statement, Solution, Spec: Sneaker Model Fine-Tuning & Evaluation Pipeline, Testing Decisions, User Stories

### Community 38 - "PipelineCoordinator"
Cohesion: 0.08
Nodes (15): Planned Changes, What was actually changed (fill in after the edit), 03: Pipeline Worker Storage Integration, PipelineConfig, main(), on_crossing_event(), CrossingTask, PipelineCoordinator (+7 more)

### Community 44 - "2. การตัดสินใจเชิงสถาปัตยกรรม (ADR-0001 ถึง ADR-0007)"
Cohesion: 0.25
Nodes (8): 2. การตัดสินใจเชิงสถาปัตยกรรม (ADR-0001 ถึง ADR-0007), ADR-0001: Person Detection and Multi-Object Tracking Pipeline, ADR-0002: Virtual Line Crossing and Tripwire Mechanism, ADR-0003: Lower-Body ROI Extraction and Sneaker Detection, ADR-0004: Event Logging and Data Storage, ADR-0005: Camera Placement and Optical Geometry, ADR-0006: Runtime Architecture, Concurrency and Testing Strategy, ADR-0007: Dark Footwear Robustness via Training-Time Augmentation

### Community 45 - "Feature Spec: Core Video and Tracking Pipeline"
Cohesion: 0.22
Nodes (8): Feature Spec: Core Video and Tracking Pipeline, Further Notes, Implementation Decisions, Out of Scope, Problem Statement, Solution, Testing Decisions, User Stories

### Community 47 - "coordinator.py"
Cohesion: 0.10
Nodes (8): FootwearInspectionResult, FootwearInspector, extract_lower_body_roi(), LowerBodyRoi, test_extract_lower_body_roi_boundary_clamping(), test_extract_lower_body_roi_exact_formula(), test_footwear_inspector_negative_detection(), test_footwear_inspector_positive_detection()

### Community 48 - "is_frozen_spec_target"
Cohesion: 0.14
Nodes (11): is_frozen_spec_target(), 1. What Was Completed, 2. Immediate Next Steps for Next Agent, 3. Suggested Skills for Next Agent, 4. Key Paths & Artifacts, Handoff: Sneaker Dataset Ingestion & Pre-Tool Hook Fix, 1. What Was Completed, 2. Immediate Next Steps for Next Agent (+3 more)

### Community 49 - "2. System Invariants & Non-Negotiable Rules"
Cohesion: 0.18
Nodes (10): 1. Domain Terminology, 2. System Invariants & Non-Negotiable Rules, GLOSSARY.md — Domain Terminology & System Invariants, Invariant 1: 30+ FPS Real-Time Capture Guarantee, Invariant 2: Bounded Event Queue (Max Capacity = 20), Invariant 3: Single-Class Inspection Scope, Invariant 4: Floor-Plane Anchor Formulation, Invariant 5: SQLite WAL Mode Persistence (+2 more)

### Community 50 - "test_storage.py"
Cohesion: 0.08
Nodes (4): populated_db_and_images(), temp_db_path(), test_sqlite_repository_initialization_enables_wal_and_creates_schema(), test_sqlite_repository_query_all_and_count()

### Community 56 - "1.1 Core Video Pipeline Feature Inception & Delivery"
Cohesion: 0.22
Nodes (8): 1.1 Core Video Pipeline Feature Inception & Delivery, 1.2 User Feedback & Iterative Edits (`feedback/` & `edits/`), 1.3 Verification & Quality Tooling, 1. What Was Completed in This Session, 2. Immediate Next Steps for Next Session, 3. Suggested Skills for Next Agent, 4. Key Paths & Code Locations, Handoff: Core Video & Tracking Pipeline Complete (Lateral Side-View) — Ready for Storage & Evidence

### Community 57 - "3. Step-by-Step Execution Playbook for Next Agent"
Cohesion: 0.18
Nodes (10): 2. Grill-Me Consensus & Architectural Decisions, 3. Step-by-Step Execution Playbook for Next Agent, 4. Key File & Directory References, 5. Suggested Skills, Handoff: Sneaker Model Retraining & Production Verification (Ticket 05), Step 1: Prepare Merged Dataset Configuration, Step 2: Execute Retraining with Tuned Augmentations, Step 3: Run Benchmark Gate & Weight Export (+2 more)

### Community 59 - "EvidenceWriter"
Cohesion: 0.14
Nodes (8): Planned Changes, EvidenceWriter, SavedEvidencePaths, temp_capture_dir(), test_evidence_writer_creates_date_directory_and_saves_images(), test_evidence_writer_fallbacks_for_epoch_1970(), test_evidence_writer_handles_empty_detections(), test_evidence_writer_with_event_id_prefix()

### Community 60 - "Edit 02: Real-time Live Video GUI Preview Window with Visual HUD"
Cohesion: 0.33
Nodes (5): Acceptance Criteria, Edit 02: Real-time Live Video GUI Preview Window with Visual HUD, Planned Changes, Rationale & Impact, Target Files

### Community 62 - "CameraFrameSource"
Cohesion: 0.14
Nodes (6): Acceptance Criteria, Edit 01: Enable AVFoundation Camera Backend for macOS, Planned Changes, Rationale & Impact, Target Files, CameraFrameSource

### Community 63 - "json"
Cohesion: 0.31
Nodes (6): get_session_start_mtime(), extract_latest_user_prompt(), get_trace_file(), load_trace(), main(), save_trace()

### Community 64 - "pathlib"
Cohesion: 0.06
Nodes (18): load_env_file(), main(), find_label_for_image(), main(), merge_datasets(), resolve_split_images(), verify_labels_exist(), main() (+10 more)

### Community 65 - "test_preflight.py"
Cohesion: 0.25
Nodes (3): test_core_dependencies_importable(), test_mps_acceleration_available(), test_mps_tensor_operation()

### Community 66 - "pre_tool_spec_enforcer.py"
Cohesion: 0.27
Nodes (3): read_files_to_message(), check_graphify_installed(), is_graphify_available()

### Community 67 - "test_sneaker_model.py"
Cohesion: 0.17
Nodes (5): model_path(), test_sneaker_model_detects_real_sample(), test_sneaker_model_inference_contract(), test_sneaker_model_loads_and_single_class(), test_sneaker_model_weights_exist()

### Community 69 - "Edit 03: Realign Tripwire to Lateral Side-View Vertical Geometry per ADR-0005"
Cohesion: 0.33
Nodes (5): Acceptance Criteria, Edit 03: Realign Tripwire to Lateral Side-View Vertical Geometry per ADR-0005, Planned Changes, Rationale & Impact, Target Files

### Community 70 - "Feedback 01: macOS AVFoundation Camera Backend"
Cohesion: 0.33
Nodes (5): Feedback 01: macOS AVFoundation Camera Backend, Reason the user gave, What the user asked to change, What the user said (verbatim), What was actually changed (fill in after the edit)

### Community 71 - "evaluate_and_export.py"
Cohesion: 0.07
Nodes (23): 1. Manifest-Based Dataset Merger with Domain Oversampling, 2. ADR-0007 Training-Time Augmentation Contract, 3. Dual-Gate Evaluation, Safe Backup & Promotion, 4. Automated Before/After Hallway Visual Comparison, Feature Spec: Dark Sneaker Domain Adaptation, Retraining & Dual-Gate Verification, Further Notes, Implementation Decisions, Out of Scope (+15 more)

### Community 72 - "Edit 03: Accurate Two-Foot Annotation & Verification Pipeline"
Cohesion: 0.33
Nodes (5): Acceptance Criteria, Edit 03: Accurate Two-Foot Annotation & Verification Pipeline, Planned Changes, Rationale & Impact, Target Files

### Community 73 - "detect_session_role"
Cohesion: 0.20
Nodes (5): detect_session_role(), is_codex_caller(), make_empty_payload(), make_inject_payload(), parse_hook_input()

### Community 74 - "Feedback 03: Curate and Annotate Both Feet"
Cohesion: 0.33
Nodes (5): Feedback 03: Curate and Annotate Both Feet, Reason the user gave, What the user asked to change, What the user said (verbatim), What was actually changed (fill in after the edit)

### Community 75 - "Edit 01: Implement Retraining Pipeline and Generate 5 Visual Augmentation Samples"
Cohesion: 0.33
Nodes (5): Acceptance Criteria, Edit 01: Implement Retraining Pipeline and Generate 5 Visual Augmentation Samples, Planned Changes, Rationale & Impact, Target Files

### Community 79 - "PipelineHud"
Cohesion: 0.20
Nodes (3): 3.4 เฟสที่ 4: การพัฒนาระบบประมวลผลวิดีโอสด (Core Video Pipeline), 4.6 Session 10: การพัฒนา Core Video Pipeline และการแก้ปัญหาอุปกรณ์จริง, PipelineHud

### Community 80 - "Feedback 01: Start Implementation and Request 5 Visual Augmentation Samples"
Cohesion: 0.33
Nodes (5): Feedback 01: Start Implementation and Request 5 Visual Augmentation Samples, Reason the user gave, What the user asked to change, What the user said (verbatim), What was actually changed (fill in after the edit)

### Community 81 - "Real-Time Corridor Tripwire Footwear Inspection System"
Cohesion: 0.22
Nodes (8): 1.1 วัตถุประสงค์, 1.2 สถาปัตยกรรมหลักของระบบ (Two-Stage Decoupled Pipeline), 1. จุดเริ่มต้นและเป้าหมายของระบบ, 6. แผนการดำเนินงานและสิ่งที่ได้ทำไปแล้ว (Execution Plan & Status), 8.1 สรุปผลการส่งมอบในปัจจุบัน, 8.2 ทิศทางการต่อยอดในอนาคต, 8. สรุปผลลัพธ์และทิศทางการพัฒนาในอนาคต, Real-Time Corridor Tripwire Footwear Inspection System

### Community 82 - "PersonTracker"
Cohesion: 0.07
Nodes (18): Acceptance Criteria, Edit 02: Tracker ID Stability and Reset Mechanism, Planned Changes, Rationale & Impact, Target Files, Feedback 02: Tracker ID Stability and Reset, Reason the user gave, What the user asked to change (+10 more)

### Community 83 - "2. Immediate Next Steps for Next Feature"
Cohesion: 0.50
Nodes (3): 1. What Was Completed, 2. Immediate Next Steps for Next Feature, Handoff: Sneaker YOLO11n Model Fine-Tuning & Evaluation Pipeline

### Community 85 - "SyntheticFrameSource"
Cohesion: 0.15
Nodes (3): SyntheticFrameSource, test_synthetic_frame_source_context_manager(), test_synthetic_frame_source_yields_expected_stream()

### Community 86 - "Edit 05: Dark Sneaker Augmentation Strategy & ADR"
Cohesion: 0.33
Nodes (5): Acceptance Criteria, Edit 05: Dark Sneaker Augmentation Strategy & ADR, Planned Changes, Rationale & Impact, Target Files

### Community 87 - "4. บันทึกประวัติการ Prompt การทำงาน และการแก้ปัญหาอย่างละเอียด (Prompt Trace & Incident History)"
Cohesion: 0.22
Nodes (9): 4.1 Session 3: การตั้งโจทย์และการระดมความคิดทางสถาปัตยกรรม (Inception & ADR 0001-0005), 4.2 Session 4: การแก้ปัญหาชุดข้อมูลและข้อจำกัดการวาด Bounding Box, 4.3 Session 7: การสร้างระเบียบวิศวกรรมและการประมวลผล Dataset, 4.4 Session 8: การจัดการเหตุการณ์ขัดข้อง (Incident) ของ Pre-Tool Spec Enforcer Hook, 4.5 Session 9: การเทรนโมเดลตรวจจับรองเท้าและการวัดผลเชิงปริมาณ, 4.7 Session 11: การแก้ปัญหารองเท้าสีดำ และการสถาปนา ADR-0007, 4.8 Session 12: การเทรนรอบใหม่แก้ปัญหาสำเร็จ และการจัดระเบียบไฟล์หลักฐาน, 4.9 Session 13: การสรุปเอกสาร การปิดงาน และบันทึกร่องรอย Prompt ทั้งหมด (+1 more)

### Community 88 - "5.3 ภาพเปรียบเทียบผลการตรวจจับจริง (Before vs After Evidence)"
Cohesion: 0.25
Nodes (8): 5.1 ทำไม ADR-0007 จึงช่วยให้ระบบดีขึ้นอย่างก้าวกระโดด, 5.2 ตารางเปรียบเทียบประสิทธิภาพ ก่อน - หลัง ปรับใช้ ADR-0007, 5.3 ภาพเปรียบเทียบผลการตรวจจับจริง (Before vs After Evidence), 5. ผลกระทบของ ADR-0007 และการเปรียบเทียบ ก่อน - หลัง (Before vs After), ตัวอย่างที่ 1: การแก้ปัญหารองเท้าซ้อนกันและเงาดำ (Depth Overlap & Silhouette), ตัวอย่างที่ 2: การแก้ปัญหาภาพเบลอจากการก้าวเท้า (Motion Blur), ตัวอย่างที่ 3: การแก้ปัญหาแสงสะท้อนบนพื้นกระเบื้องขาว (Floor Glare), ตัวอย่างที่ 4: ตัวอย่างภาพที่ผ่านกระบวนการ Training-Time Augmentation

### Community 89 - "1. What Was Completed in This Session"
Cohesion: 0.06
Nodes (27): Feedback 02: Real Wall-Clock Date and Sequence Prefix for Captured Evidence, Reason the user gave, What the user asked to change, What the user said (verbatim), What was actually changed (fill in after the edit), 1.1 Specification & Tracer Tickets, 1.2 Dataset Merger with 5x Oversampling (Ticket 01), 1.3 ADR-0007 Augmentation Pipeline & 5 Visual Samples (Ticket 02) (+19 more)

### Community 90 - "Edit 04: Annotate Occluded and Blurred Second Shoes"
Cohesion: 0.33
Nodes (5): Acceptance Criteria, Edit 04: Annotate Occluded and Blurred Second Shoes, Planned Changes, Rationale & Impact, Target Files

### Community 91 - "Feedback 04: Annotate Occluded and Blurred Second Shoes"
Cohesion: 0.33
Nodes (5): Feedback 04: Annotate Occluded and Blurred Second Shoes, Reason the user gave, What the user asked to change, What the user said (verbatim), What was actually changed (fill in after the edit)

### Community 92 - "Feedback 05: Dark Sneaker Augmentation Strategy & ADR"
Cohesion: 0.33
Nodes (5): Feedback 05: Dark Sneaker Augmentation Strategy & ADR, Reason the user gave, What the user asked to change, What the user said (verbatim), What was actually changed (fill in after the edit)

### Community 94 - "2. Immediate Next Steps for Next Feature"
Cohesion: 0.50
Nodes (3): 1. What Was Completed, 2. Immediate Next Steps for Next Feature, Handoff: Sneaker YOLO11n Model Fine-Tuning & Evaluation Pipeline

### Community 98 - "3. บันทึกกระบวนการทำงาน การสนทนากับ AI และการแก้ปัญหาตามบริบทจริง"
Cohesion: 0.33
Nodes (6): 3.1 เฟสที่ 1: การวางรากฐานและธรรมาภิบาลโค้ด (Architecture Governance), 3.2 เฟสที่ 2: การเตรียมชุดข้อมูลรองเท้าผ้าใบ (Sneaker Dataset Ingestion), 3.3 เฟสที่ 3: การเทรนโมเดลเริ่มต้นและการกำหนดเกณฑ์วัดผล (Model Training), 3.5 เฟสที่ 5: ระบบจัดเก็บหลักฐานและปัญหาการตรวจจับรองเท้าสีดำ (Storage & Evidence), 3.6 เฟสที่ 6: การฝึกสอนโมเดลรอบใหม่และการจัดระเบียบไฟล์หลักฐาน (Dark Sneaker Retraining), 3. บันทึกกระบวนการทำงาน การสนทนากับ AI และการแก้ปัญหาตามบริบทจริง

### Community 99 - "Feedback 02: Real-time Live Video GUI Preview"
Cohesion: 0.33
Nodes (5): Feedback 02: Real-time Live Video GUI Preview, Reason the user gave, What the user asked to change, What the user said (verbatim), What was actually changed (fill in after the edit)

### Community 100 - "2. Immediate Next Steps for Next Agent"
Cohesion: 0.33
Nodes (5): 1. What Was Completed, 2. Immediate Next Steps for Next Agent, 3. Suggested Skills for Next Agent, 4. Key Paths & Artifacts, Handoff: Sneaker YOLO11n Model Training Complete — Ready for Core Video Pipeline

### Community 101 - "Incident Report: False-Positive Spec Freezing Gate during Task Implementation"
Cohesion: 0.33
Nodes (5): 1. What Happened (Timeline Reconstruction), 2. Root Cause Analysis, 3. Recommended Remediation, Flaws:, Incident Report: False-Positive Spec Freezing Gate during Task Implementation

### Community 102 - "7. โครงสร้างโปรเจกต์และวิธีติดตั้งใช้งาน"
Cohesion: 0.40
Nodes (5): 7.1 โครงสร้างไฟล์ในโปรเจกต์, 7.2 การติดตั้ง Dependencies, 7.3 การเรียกใช้งานระบบ, 7.4 การรันชุดทดสอบ (Automated Test Suite), 7. โครงสร้างโปรเจกต์และวิธีติดตั้งใช้งาน

### Community 103 - "Edit 01: Implement Storage Persistence & Active Retraining Pipeline"
Cohesion: 0.40
Nodes (4): Acceptance Criteria, Edit 01: Implement Storage Persistence & Active Retraining Pipeline, Rationale & Impact, Target Files

### Community 104 - "Edit 02: Real Wall-Clock Date and Sequence Prefix for Captured Evidence"
Cohesion: 0.40
Nodes (4): Acceptance Criteria, Edit 02: Real Wall-Clock Date and Sequence Prefix for Captured Evidence, Rationale & Impact, Target Files

### Community 105 - "Feedback 01: Implement Storage Persistence & Active Retraining Pipeline"
Cohesion: 0.40
Nodes (4): Feedback 01: Implement Storage Persistence & Active Retraining Pipeline, Reason the user gave, What the user asked to change, What the user said (verbatim)

### Community 107 - "1. What Was Completed"
Cohesion: 0.50
Nodes (3): 1. What Was Completed, 2. Immediate Next Steps, Handoff: Core Video & Tracking Pipeline Complete — Ready for Storage & Persistence

## Knowledge Gaps
- **1 isolated node(s):** `my-cv`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 714 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **28 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `FrameSource` connect `FrameSource` to `2. Immediate Next Steps for Next Agent`, `PipelineCoordinator`, `1. What Was Completed`, `2. การตัดสินใจเชิงสถาปัตยกรรม (ADR-0001 ถึง ADR-0007)`, `coordinator.py`, `Real-Time Corridor Tripwire Footwear Inspection System`, `2. Immediate Next Steps for Next Feature`, `VideoFileFrameSource`, `SyntheticFrameSource`, `CameraFrameSource`, `1.1 Core Video Pipeline Feature Inception & Delivery`, `AGENTS.md — Engineering Guidelines & Operational Standards`, `numpy`, `2. Immediate Next Steps for Next Feature`?**
  _High betweenness centrality (0.091) - this node is a cross-community bridge._
- **Are the 18 inferred relationships involving `PipelineCoordinator` (e.g. with `Positive` and `Planned Changes`) actually correct?**
  _`PipelineCoordinator` has 18 INFERRED edges - model-reasoned connections that need verification._
- **What connects `my-cv` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `TrackedPerson` be split into smaller, more focused modules?**
  _Cohesion score 0.09401709401709402 - nodes in this community are weakly interconnected._
- **Why does `PipelineCoordinator` connect `PipelineCoordinator` to `ADR-0007: Dark Footwear Robustness via Training-Time Augmentation vs Real-Time Preprocessing`, `Edit 01: Implement Storage Persistence & Active Retraining Pipeline`, `1. What Was Completed`, `person_tracker.py`, `coordinator.py`, `PipelineHud`, `EventRepository`, `PersonTracker`, `1.1 Core Video Pipeline Feature Inception & Delivery`, `FrameSource`, `EvidenceWriter`, `Edit 02: Real-time Live Video GUI Preview Window with Visual HUD`?**
  _High betweenness centrality (0.059) - this node is a cross-community bridge._
- **Are the 10 inferred relationships involving `FrameSource` (e.g. with `Encapsulation Rules:` and `3. Testing Strategy & Testability Seams`) actually correct?**
  _`FrameSource` has 10 INFERRED edges - model-reasoned connections that need verification._
- **Should `Rules` be split into smaller, more focused modules?**
  _Cohesion score 0.07692307692307693 - nodes in this community are weakly interconnected._