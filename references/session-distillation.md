# Distilling Session Feedback

Improve future execution from session evidence—failures, corrections, avoidable work, and successful techniques—while preserving the scope and exact constraints of the original instruction.

## Distillation Workflow

1. **Audit the trajectory:** Inspect decisions, tool calls, artifacts, and user feedback (even in successful sessions). Separate the user's explicit instruction from inferred explanations.
2. **Diagnose cause -> remedy before mutation:** Connect **observation -> supported cause -> proposed remedy -> expected observable result**. When responding to diagnostic feedback, symptom inquiries, or defect reports, complete the diagnosis and confirm the proposed remedy before mutating files.
   - Distinguish a missing rule from an ignored, undiscoverable, or contradictory existing rule before adding text.
   - Fix broken helpers, schemas, or CLI docs when the root cause is in tooling rather than the prompt.
   - Label unconfirmed explanations as hypotheses and identify a check to test them; do not encode a hypothesis or one-off recovery step as a permanent rule.
   - Distill remedies into high-density invariants: state the minimal, self-contained rule (`Directive: concise rationale`) rather than embedding narrative post-mortems or conversational history.
3. **Scope applicability:** Classify whether feedback is a personal preference, repository convention, contract-specific rule, or reusable pattern. Remove transient session noise while preserving exact limits, exceptions, required identifiers, and authorization boundaries.
4. **Route to the canonical owner:** Update the existing owner and affected callers rather than duplicating rules across files. Make the smallest change that addresses the cause. Practice in-file density first in `SKILL.md` before proliferating auxiliary files.
5. **Verify:** Check the change against the original failure case and a nearby case that must remain unaffected. State observation, cause/confidence, owner changed, and verification performed (distinguishing lint, script checks, and live agent runs).

## Execution Trajectory Audit

| Lens | What to inspect | Evidence to retain |
|---|---|---|
| Explicit corrections & failures | Ignored requirements, tool errors, broken contracts, or user intervention | Original requirement, conflicting action/output, and consequence |
| Inefficiencies | Unjustified repeated reads/searches, unnecessary full-file ingestion, or serialized independent work | Repeated work, what it contributed, and measured cost (if any) |
| Unnecessary steps | Questions already answered in context, unrelated inspection, or redundant approvals | Information already available and the step it made unnecessary |
| Wrong decisions or ordering | Invented flags/facts, acting before evidence, premature mutation before diagnosis, skipped verification, or cyclic retries | Decision point, missing evidence, and resulting failure or risk |
| Successful techniques | A check, helper, example, or recovery path that demonstrably improved completion | Conditions under which it helped and observable result |

*Note:* Sequential work or repeated reads are valid when justified by dependencies, file mutations, or verification.

## Canonical Owner Routing

| Lesson concerns | Preferred owner | Keep elsewhere |
|---|---|---|
| Coding style or repo-wide rules | Shared coding instructions (steering) | Links from affected workflows (steering must remain role-agnostic; keep specialized agent gates in the agent/skill) |
| Test conventions or environment setup | Shared testing guidance or test runner | Task-specific invocation and inputs |
| Agent responsibility, routing, or tools | Relevant agent definition (or shared router) | Procedural details in the owning skill |
| Task procedure, modes, or recovery | Owning skill (`SKILL.md`; in-file density first) or conditional reference if `> 14 KB` | Short routing link from entrypoint |
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
| Agent made a false assumption from missing error docs | `Silence != Permission: Absence of a documented error or restriction is never proof an operation is allowed.` | Writing multi-paragraph explanations of backend engines, quoting specs, and recounting session failure history |
| User reports symptom feedback or asks "why did agent do X" | Isolate root cause, state cause $\rightarrow$ remedy, and confirm scope before editing | Mutating files immediately on a symptom report without diagnostic confirmation |
| Specialized workflow needs gating or clarification | Encapsulate gate in custom agent and owning skill | Leaking specialized workflow gates into global workspace steering |
| New decision criteria or small lookup rule needed | Embed concisely in `SKILL.md` (in-file density first) if `< 14 KB` | Creating a new auxiliary reference file prematurely |
| Runtime rejects a metadata field (e.g. Gemini rejects 'tools' in agent frontmatter) | Enforce runtime-specific frontmatter constraints in validator and templates; configure capabilities natively | Assuming all agent wrappers share identical frontmatter schemas |
