# Distilling Session Feedback

Improve future execution from session evidence—failures, corrections, avoidable work, and successful techniques—while preserving the scope and exact constraints of the original instruction.

## Distillation Workflow

1. **Audit the trajectory:** Inspect decisions, tool calls, artifacts, and user feedback (even in successful sessions). Separate the user's explicit instruction from inferred explanations.
2. **Diagnose cause -> remedy:** Connect **observation -> supported cause -> proposed remedy -> expected observable result**.
   - Distinguish a missing rule from an ignored, undiscoverable, or contradictory existing rule before adding text.
   - Fix broken helpers, schemas, or CLI docs when the root cause is in tooling rather than the prompt.
   - Label unconfirmed explanations as hypotheses and identify a check to test them; do not encode a hypothesis or one-off recovery step as a permanent rule.
3. **Scope applicability:** Classify whether feedback is a personal preference, repository convention, contract-specific rule, or reusable pattern. Remove transient session noise while preserving exact limits, exceptions, required identifiers, and authorization boundaries.
4. **Route to the canonical owner:** Update the existing owner and affected callers rather than duplicating rules across files. Make the smallest change that addresses the cause.
5. **Verify:** Check the change against the original failure case and a nearby case that must remain unaffected. State observation, cause/confidence, owner changed, and verification performed (distinguishing lint, script checks, and live agent runs).

## Execution Trajectory Audit

| Lens | What to inspect | Evidence to retain |
|---|---|---|
| Explicit corrections & failures | Ignored requirements, tool errors, broken contracts, or user intervention | Original requirement, conflicting action/output, and consequence |
| Inefficiencies | Unjustified repeated reads/searches, unnecessary full-file ingestion, or serialized independent work | Repeated work, what it contributed, and measured cost (if any) |
| Unnecessary steps | Questions already answered in context, unrelated inspection, or redundant approvals | Information already available and the step it made unnecessary |
| Wrong decisions or ordering | Invented flags/facts, acting before evidence, skipped verification, or cyclic retries | Decision point, missing evidence, and resulting failure or risk |
| Successful techniques | A check, helper, example, or recovery path that demonstrably improved completion | Conditions under which it helped and observable result |

*Note:* Sequential work or repeated reads are valid when justified by dependencies, file mutations, or verification.

## Canonical Owner Routing

| Lesson concerns | Preferred owner | Keep elsewhere |
|---|---|---|
| Coding style or repo-wide rules | Shared coding instructions | Links from affected workflows |
| Test conventions or environment setup | Shared testing guidance or test runner | Task-specific invocation and inputs |
| Agent responsibility, routing, or tools | Relevant agent definition (or shared router) | Procedural details in the owning skill |
| Task procedure, modes, or recovery | Owning skill (`SKILL.md`) or conditional reference | Short routing link from entrypoint |
| Schemas, examples, or lookup tables | `references/` (guidance) or `assets/` (templates) | Discoverable link with read/use condition |
| Deterministic parsing, validation, or CLI args | Helper script in `scripts/` + regression test | Command invocation in the calling skill |
| Contract-specific data or behavior | That contract and its fixtures | Broader guidance only when evidence supports it |

## Scope-Preserving Examples

| Feedback or evidence | Faithful instruction | Avoid |
|---|---|---|
| One consumer requires `null` for an absent optional collection | Preserve that consumer's declared absence semantics | Requiring `null` for all optional collections in every API |
| User says "at most two questions" | Ask at most two questions per turn in the stated scope | Rewriting the limit as two to three |
| A named test dependency was stopped | Verify dependencies declared by the selected test suite before running | Starting every local service or inventing a container name |
| Two components drifted after copying the same standard | Keep the standard in its canonical owner and link callers | Adding another paraphrase to each component |
| User supplies an exact identifier required by an output contract | Preserve it in the relevant contract or fixture | Removing required identifiers because they look session-specific |
