# Graph Report - my-cv  (2026-11-10)

## Corpus Check
- 158 files · ~470,054 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 7 file(s) not represented in the graph (top: (none) 4, .example 1, .lock 1)

## Summary
- 1124 nodes · 1794 edges · 110 communities (80 shown, 30 thin omitted)
- Extraction: 92% EXTRACTED · 8% INFERRED · 0% AMBIGUOUS · INFERRED: 148 edges (avg confidence: 0.92)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- TrackedPerson
- Rules
- Diagnosing Bugs
- Test-Driven Development
- pre_tool_spec_enforcer.py
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
- pytest
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
- numpy
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
- Feature Spec: Core Video and Tracking Pipeline
- coordinator.py
- json
- person_tracker.py
- 2. System Invariants & Non-Negotiable Rules
- EventRepository
- 01-frame-source-abstraction.md
- 02-person-detection-and-tracking.md
- 03-virtual-line-tripwire.md
- 04-lower-body-roi-and-sneaker-inspection.md
- 05-decoupled-concurrency-and-main-loop.md
- PipelineHud
- 3. Step-by-Step Execution Playbook for Next Agent
- FrameSource
- test_evidence_writer.py
- Edit 02: Real-time Live Video GUI Preview Window with Visual HUD
- SyntheticFrameSource
- CameraFrameSource
- session-start-main.py
- pathlib
- 2. Immediate Next Steps for Next Agent
- TripwireZone
- test_sneaker_model.py
- Edit 03: Realign Tripwire to Lateral Side-View Vertical Geometry per ADR-0005
- Feedback 01: macOS AVFoundation Camera Backend
- evaluate_and_export.py
- Edit 03: Accurate Two-Foot Annotation & Verification Pipeline
- Feedback 03: Lateral Side-View Vertical Tripwire & Floor Alignment
- Feedback 03: Curate and Annotate Both Feet
- Edit 01: Implement Retraining Pipeline and Generate 5 Visual Augmentation Samples
- 01-sqlite-event-repository.md
- 02-evidence-image-writer.md
- 04-active-dataset-curation-and-export.md
- merge_datasets.py
- Feedback 01: Start Implementation and Request 5 Visual Augmentation Samples
- dataset_exporter.py
- PersonTracker
- 2. Immediate Next Steps for Next Feature
- VideoFileFrameSource
- sync-traces.py
- Edit 05: Dark Sneaker Augmentation Strategy & ADR
- 1.1 Core Video Pipeline Feature Inception & Delivery
- .reset_tracking
- 1. What Was Completed in This Session
- Edit 04: Annotate Occluded and Blurred Second Shoes
- Feedback 04: Annotate Occluded and Blurred Second Shoes
- Feedback 05: Dark Sneaker Augmentation Strategy & ADR
- 01-manifest-dataset-merger-with-oversampling.md
- 2. Immediate Next Steps for Next Feature
- 02-adr0007-training-time-augmentation-pipeline.md
- 03-dual-gate-evaluation-backup-and-visual-report.md
- 04-execute-retraining-promote-weights-and-verify.md
- Handoff: Sneaker Dataset Ingestion & Pre-Tool Hook Fix
- is_frozen_spec_target
- Incident Report: False-Positive Spec Freezing Gate during Task Implementation
- 1. What Was Completed in This Session
- train_sneaker_model
- .save_evidence
- Edit 02: Real Wall-Clock Date and Sequence Prefix for Captured Evidence
- Feedback 02: Real Wall-Clock Date and Sequence Prefix for Captured Evidence
- Edit 01: Implement Storage Persistence & Active Retraining Pipeline
- Feedback 01: Implement Storage Persistence & Active Retraining Pipeline
- ._extract_date_str
- 1. What Was Completed

## God Nodes (most connected - your core abstractions)
1. `PipelineCoordinator` - 36 edges
2. `FrameSource` - 29 edges
3. `EventRepository` - 29 edges
4. `SyntheticFrameSource` - 27 edges
5. `CameraFrameSource` - 24 edges
6. `TrackedPerson` - 21 edges
7. `VideoFileFrameSource` - 20 edges
8. `PipelineConfig` - 19 edges
9. `CrossingRecord` - 18 edges
10. `TripwireZone` - 18 edges

## Surprising Connections (you probably didn't know these)
- `1. What Was Completed` --references--> `is_frozen_spec_target()`  [INFERRED]
  .scratch/handoffs/2026-11-10-162500-handoff.md → .agents/hooks/pre_tool_spec_enforcer.py
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

## Communities (110 total, 30 thin omitted)

### Community 0 - "TrackedPerson"
Cohesion: 0.21
Nodes (3): TrackedPerson, MockLateralTracker, MockTracker

### Community 1 - "Rules"
Cohesion: 0.08
Nodes (25): 1.1 Lifecycle Flow, 1.2 Execution Workflow & AI Duties, 1. Answer first, 1. Delivery Lifecycle & PR Workflow, 1. Think Before Coding, 2. Kill ceremony, 2. Simplicity First, 3. Short word (+17 more)

### Community 2 - "Diagnosing Bugs"
Cohesion: 0.13
Nodes (14): Completion criterion: a tight loop that goes red, Diagnosing Bugs, Minimise, Non-deterministic bugs, Phase 1: Build a feedback loop, Phase 2: Reproduce + minimise, Phase 3: Hypothesise, Phase 4: Instrument (+6 more)

### Community 3 - "Test-Driven Development"
Cohesion: 0.15
Nodes (10): Designing for Mockability, When to Mock, Anti-patterns, Rules of the loop, Seams: where tests go, Test-Driven Development, What a good test is, Bad Tests (+2 more)

### Community 4 - "pre_tool_spec_enforcer.py"
Cohesion: 0.14
Nodes (11): check_graphify_installed(), check_spec_in_workspace(), get_latest_user_input_time(), get_project_root(), get_spec_creation_time(), get_user_inputs(), is_production_code_modification(), main() (+3 more)

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

### Community 17 - "pytest"
Cohesion: 0.21
Nodes (4): calculate_ground_anchor_point(), test_calculate_ground_anchor_point_asymmetric(), test_calculate_ground_anchor_point_exact_formula(), test_person_tracker_detection_filtering_and_tracking()

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

### Community 31 - "numpy"
Cohesion: 0.06
Nodes (21): main(), segment_feet_boxes(), apply_erasing(), apply_flip_and_scale(), apply_hsv_jitter(), apply_rotation(), draw_boxes(), generate_samples() (+13 more)

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
Cohesion: 0.10
Nodes (10): 03: Pipeline Worker Storage Integration, PipelineConfig, main(), on_crossing_event(), PipelineCoordinator, ProcessedCrossingEvent, MockInspector, test_pipeline_end_to_end_integration() (+2 more)

### Community 45 - "Feature Spec: Core Video and Tracking Pipeline"
Cohesion: 0.22
Nodes (8): Feature Spec: Core Video and Tracking Pipeline, Further Notes, Implementation Decisions, Out of Scope, Problem Statement, Solution, Testing Decisions, User Stories

### Community 46 - "coordinator.py"
Cohesion: 0.11
Nodes (3): CrossingTask, TripwireCrossing, test_pipeline_bounded_queue_invariant()

### Community 47 - "json"
Cohesion: 0.22
Nodes (9): analyze(), load_trace(), main(), save_trace(), extract_latest_user_prompt(), get_trace_file(), load_trace(), main() (+1 more)

### Community 49 - "2. System Invariants & Non-Negotiable Rules"
Cohesion: 0.18
Nodes (10): 1. Domain Terminology, 2. System Invariants & Non-Negotiable Rules, GLOSSARY.md — Domain Terminology & System Invariants, Invariant 1: 30+ FPS Real-Time Capture Guarantee, Invariant 2: Bounded Event Queue (Max Capacity = 20), Invariant 3: Single-Class Inspection Scope, Invariant 4: Floor-Plane Anchor Formulation, Invariant 5: SQLite WAL Mode Persistence (+2 more)

### Community 50 - "EventRepository"
Cohesion: 0.09
Nodes (9): Planned Changes, What was actually changed (fill in after the edit), CrossingRecord, EventRepository, populated_db_and_images(), temp_db_path(), test_sqlite_repository_initialization_enables_wal_and_creates_schema(), test_sqlite_repository_insert_and_query_by_track_id() (+1 more)

### Community 56 - "PipelineHud"
Cohesion: 0.14
Nodes (6): Feedback 02: Real-time Live Video GUI Preview, Reason the user gave, What the user asked to change, What the user said (verbatim), What was actually changed (fill in after the edit), PipelineHud

### Community 57 - "3. Step-by-Step Execution Playbook for Next Agent"
Cohesion: 0.18
Nodes (10): 2. Grill-Me Consensus & Architectural Decisions, 3. Step-by-Step Execution Playbook for Next Agent, 4. Key File & Directory References, 5. Suggested Skills, Handoff: Sneaker Model Retraining & Production Verification (Ticket 05), Step 1: Prepare Merged Dataset Configuration, Step 2: Execute Retraining with Tuned Augmentations, Step 3: Run Benchmark Gate & Weight Export (+2 more)

### Community 59 - "test_evidence_writer.py"
Cohesion: 0.21
Nodes (5): What was actually changed (fill in after the edit), temp_capture_dir(), test_evidence_writer_fallbacks_for_epoch_1970(), test_evidence_writer_handles_empty_detections(), test_evidence_writer_with_event_id_prefix()

### Community 60 - "Edit 02: Real-time Live Video GUI Preview Window with Visual HUD"
Cohesion: 0.33
Nodes (5): Acceptance Criteria, Edit 02: Real-time Live Video GUI Preview Window with Visual HUD, Planned Changes, Rationale & Impact, Target Files

### Community 61 - "SyntheticFrameSource"
Cohesion: 0.13
Nodes (4): FrameData, SyntheticFrameSource, test_synthetic_frame_source_context_manager(), test_synthetic_frame_source_yields_expected_stream()

### Community 62 - "CameraFrameSource"
Cohesion: 0.13
Nodes (7): Acceptance Criteria, Edit 01: Enable AVFoundation Camera Backend for macOS, Planned Changes, Rationale & Impact, Target Files, CameraFrameSource, test_camera_frame_source_initialization()

### Community 63 - "session-start-main.py"
Cohesion: 0.20
Nodes (6): detect_session_role(), is_codex_caller(), make_empty_payload(), make_inject_payload(), parse_hook_input(), read_files_to_message()

### Community 64 - "pathlib"
Cohesion: 0.14
Nodes (7): load_env_file(), main(), main(), assign_splits(), collect_images(), load_env_file(), main()

### Community 65 - "2. Immediate Next Steps for Next Agent"
Cohesion: 0.33
Nodes (5): 1. What Was Completed, 2. Immediate Next Steps for Next Agent, 3. Suggested Skills for Next Agent, 4. Key Paths & Artifacts, Handoff: Sneaker YOLO11n Model Training Complete — Ready for Core Video Pipeline

### Community 66 - "TripwireZone"
Cohesion: 0.18
Nodes (6): What was actually changed (fill in after the edit), TripwireZone, test_tripwire_cooldown_debounce_suppression(), test_tripwire_crossing_entry_and_exit_discrimination(), test_tripwire_exit_resets_cooldown_immediately(), test_tripwire_vertical_lateral_side_view_crossing()

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

### Community 73 - "Feedback 03: Lateral Side-View Vertical Tripwire & Floor Alignment"
Cohesion: 0.40
Nodes (4): Feedback 03: Lateral Side-View Vertical Tripwire & Floor Alignment, Reason the user gave, What the user asked to change, What the user said (verbatim)

### Community 74 - "Feedback 03: Curate and Annotate Both Feet"
Cohesion: 0.33
Nodes (5): Feedback 03: Curate and Annotate Both Feet, Reason the user gave, What the user asked to change, What the user said (verbatim), What was actually changed (fill in after the edit)

### Community 75 - "Edit 01: Implement Retraining Pipeline and Generate 5 Visual Augmentation Samples"
Cohesion: 0.33
Nodes (5): Acceptance Criteria, Edit 01: Implement Retraining Pipeline and Generate 5 Visual Augmentation Samples, Planned Changes, Rationale & Impact, Target Files

### Community 79 - "merge_datasets.py"
Cohesion: 0.14
Nodes (8): find_label_for_image(), main(), merge_datasets(), resolve_split_images(), verify_labels_exist(), dummy_datasets(), test_merge_datasets_creates_manifests_and_oversamples(), test_verify_labels_exist()

### Community 80 - "Feedback 01: Start Implementation and Request 5 Visual Augmentation Samples"
Cohesion: 0.33
Nodes (5): Feedback 01: Start Implementation and Request 5 Visual Augmentation Samples, Reason the user gave, What the user asked to change, What the user said (verbatim), What was actually changed (fill in after the edit)

### Community 81 - "dataset_exporter.py"
Cohesion: 0.13
Nodes (6): 1. Executive Summary & Active State, main(), DatasetExporter, ExportSummary, EvidenceWriter, test_dataset_exporter_creates_yolo_structure_and_labels()

### Community 82 - "PersonTracker"
Cohesion: 0.18
Nodes (8): Acceptance Criteria, Edit 02: Tracker ID Stability and Reset Mechanism, Planned Changes, Rationale & Impact, Target Files, PersonTracker, test_person_tracker_device_auto_detection(), test_person_tracker_reset_resets_track_id()

### Community 83 - "2. Immediate Next Steps for Next Feature"
Cohesion: 0.50
Nodes (3): 1. What Was Completed, 2. Immediate Next Steps for Next Feature, Handoff: Sneaker YOLO11n Model Fine-Tuning & Evaluation Pipeline

### Community 86 - "Edit 05: Dark Sneaker Augmentation Strategy & ADR"
Cohesion: 0.33
Nodes (5): Acceptance Criteria, Edit 05: Dark Sneaker Augmentation Strategy & ADR, Planned Changes, Rationale & Impact, Target Files

### Community 87 - "1.1 Core Video Pipeline Feature Inception & Delivery"
Cohesion: 0.22
Nodes (8): 1.1 Core Video Pipeline Feature Inception & Delivery, 1.2 User Feedback & Iterative Edits (`feedback/` & `edits/`), 1.3 Verification & Quality Tooling, 1. What Was Completed in This Session, 2. Immediate Next Steps for Next Session, 3. Suggested Skills for Next Agent, 4. Key Paths & Code Locations, Handoff: Core Video & Tracking Pipeline Complete (Lateral Side-View) — Ready for Storage & Evidence

### Community 88 - ".reset_tracking"
Cohesion: 0.20
Nodes (5): Feedback 02: Tracker ID Stability and Reset, Reason the user gave, What the user asked to change, What the user said (verbatim), What was actually changed (fill in after the edit)

### Community 89 - "1. What Was Completed in This Session"
Cohesion: 0.18
Nodes (10): 1.1 Specification & Tracer Tickets, 1.2 Dataset Merger with 5x Oversampling (Ticket 01), 1.3 ADR-0007 Augmentation Pipeline & 5 Visual Samples (Ticket 02), 1.4 Fine-Tuning Execution & Dual-Gate Promotion (Ticket 03 & 04), 1.6 Log Diagnostics & Field Behavior Analysis, 1. What Was Completed in This Session, 2. Key Architecture & File References, 3. Immediate Next Steps for Next Session (+2 more)

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

### Community 98 - "Handoff: Sneaker Dataset Ingestion & Pre-Tool Hook Fix"
Cohesion: 0.33
Nodes (5): 1. What Was Completed, 2. Immediate Next Steps for Next Agent, 3. Suggested Skills for Next Agent, 4. Key Paths & Artifacts, Handoff: Sneaker Dataset Ingestion & Pre-Tool Hook Fix

### Community 99 - "is_frozen_spec_target"
Cohesion: 0.15
Nodes (10): Incident: False-Positive Spec Freezing Gate Blocking Issue Checklist Updates, Resolution Plan, Root Cause, get_session_start_mtime(), is_frozen_spec_target(), 1. What Was Completed, 2. Immediate Next Steps for Next Agent, 3. Suggested Skills for Next Agent (+2 more)

### Community 100 - "Incident Report: False-Positive Spec Freezing Gate during Task Implementation"
Cohesion: 0.33
Nodes (5): 1. What Happened (Timeline Reconstruction), 2. Root Cause Analysis, 3. Recommended Remediation, Flaws:, Incident Report: False-Positive Spec Freezing Gate during Task Implementation

### Community 101 - "1. What Was Completed in This Session"
Cohesion: 0.18
Nodes (10): 1.1 Specification & Tracer Tickets, 1.2 Dataset Merger with 5x Oversampling (Ticket 01), 1.3 ADR-0007 Augmentation Pipeline & 5 Visual Samples (Ticket 02), 1.4 Fine-Tuning Execution & Dual-Gate Promotion (Ticket 03 & 04), 1.6 Log Diagnostics & Field Behavior Analysis, 1. What Was Completed in This Session, 2. Key Architecture & File References, 3. Immediate Next Steps for Next Session (+2 more)

### Community 102 - "train_sneaker_model"
Cohesion: 0.20
Nodes (3): resolve_device(), train_sneaker_model(), test_train_sneaker_model_forwards_adr0007_parameters()

### Community 104 - "Edit 02: Real Wall-Clock Date and Sequence Prefix for Captured Evidence"
Cohesion: 0.33
Nodes (5): Acceptance Criteria, Edit 02: Real Wall-Clock Date and Sequence Prefix for Captured Evidence, Planned Changes, Rationale & Impact, Target Files

### Community 105 - "Feedback 02: Real Wall-Clock Date and Sequence Prefix for Captured Evidence"
Cohesion: 0.40
Nodes (4): Feedback 02: Real Wall-Clock Date and Sequence Prefix for Captured Evidence, Reason the user gave, What the user asked to change, What the user said (verbatim)

### Community 106 - "Edit 01: Implement Storage Persistence & Active Retraining Pipeline"
Cohesion: 0.40
Nodes (4): Acceptance Criteria, Edit 01: Implement Storage Persistence & Active Retraining Pipeline, Rationale & Impact, Target Files

### Community 107 - "Feedback 01: Implement Storage Persistence & Active Retraining Pipeline"
Cohesion: 0.40
Nodes (4): Feedback 01: Implement Storage Persistence & Active Retraining Pipeline, Reason the user gave, What the user asked to change, What the user said (verbatim)

### Community 109 - "1. What Was Completed"
Cohesion: 0.50
Nodes (3): 1. What Was Completed, 2. Immediate Next Steps, Handoff: Core Video & Tracking Pipeline Complete — Ready for Storage & Persistence

## Knowledge Gaps
- **1 isolated node(s):** `my-cv`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 687 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **30 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `PipelineCoordinator` connect `PipelineCoordinator` to `ADR-0007: Dark Footwear Robustness via Training-Time Augmentation vs Real-Time Preprocessing`, `PipelineHud`, `TripwireZone`, `Edit 02: Real Wall-Clock Date and Sequence Prefix for Captured Evidence`, `Edit 01: Implement Storage Persistence & Active Retraining Pipeline`, `1. What Was Completed`, `coordinator.py`, `dataset_exporter.py`, `EventRepository`, `PersonTracker`, `1.1 Core Video Pipeline Feature Inception & Delivery`, `.reset_tracking`, `FrameSource`, `Edit 02: Real-time Live Video GUI Preview Window with Visual HUD`, `numpy`?**
  _High betweenness centrality (0.067) - this node is a cross-community bridge._
- **Are the 18 inferred relationships involving `PipelineCoordinator` (e.g. with `Positive` and `Planned Changes`) actually correct?**
  _`PipelineCoordinator` has 18 INFERRED edges - model-reasoned connections that need verification._
- **What connects `my-cv` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Rules` be split into smaller, more focused modules?**
  _Cohesion score 0.07692307692307693 - nodes in this community are weakly interconnected._
- **Why does `EvidenceWriter` connect `dataset_exporter.py` to `PipelineCoordinator`, `.save_evidence`, `._extract_date_str`, `coordinator.py`, `test_evidence_writer.py`?**
  _High betweenness centrality (0.051) - this node is a cross-community bridge._
- **Are the 8 inferred relationships involving `FrameSource` (e.g. with `Encapsulation Rules:` and `3. Testing Strategy & Testability Seams`) actually correct?**
  _`FrameSource` has 8 INFERRED edges - model-reasoned connections that need verification._
- **Should `Diagnosing Bugs` be split into smaller, more focused modules?**
  _Cohesion score 0.13333333333333333 - nodes in this community are weakly interconnected._