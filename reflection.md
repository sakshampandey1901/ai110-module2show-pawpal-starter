# PawPal+ Project Reflection

## 1. System Design

### Core user actions (from scenario)

1. **Register pets and care items** — Add one or more pets and attach care tasks (walks, feedings, medications, appointments) with time, frequency, and priority so the system has a single source of truth for what needs doing.

2. **See and adjust today’s plan** — View tasks for a chosen day sorted by time, filter by pet or completion status, and mark tasks done; the app should surface conflicts when two items land at the same time.

3. **Trust recurring and priorities** — Rely on daily/weekly recurrence to roll completed routines forward and use the scheduler to order work sensibly for a busy owner.

**a. Initial design**

- **Owner** — Holds the owner’s name and a collection of **Pet** instances. Responsible for adding pets and exposing all tasks across pets for the scheduler.
- **Pet** — Identity (`name`, `species`) and a list of **Task** objects. Responsible for attaching tasks to the right animal and completing tasks (including appending the next occurrence for recurring items).
- **Task** — One concrete activity: description, clock time (`HH:MM`), calendar date, frequency (`once` / `daily` / `weekly`), completion flag, duration, priority, and optional `pet_name` for filtering/display after assignment.
- **Scheduler** — Uses an **Owner** to gather tasks, filters by date and optional criteria, sorts by time, and returns lightweight conflict warnings when multiple tasks share the same slot.

**b. Design changes**

- **`pet_name` on `Task`** — Tasks are owned by a `Pet`, but the scheduler works with flat lists. Setting `pet_name` inside `Pet.add_task()` makes filtering and conflict messages readable without passing pet objects everywhere.
- **`Pet.complete_task()`** — Centralizes “mark done + append next recurrence” so the UI and tests do not duplicate recurrence rules.
- **Conflict detection on `Scheduler`** — Kept separate from `Owner` so the domain model stays about entities, while cross-pet checks stay lightweight utilities.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- **Calendar date** — Only tasks whose `task_date` matches the viewed day appear in the daily schedule (`tasks_for_date`).
- **Clock time** — Primary ordering uses start time (`HH:MM`); priority is visible in the table but does not reorder tasks automatically (a deliberate simplification so behavior stays predictable).
- **Completion** — Optional filter hides finished work; recurring tasks spawn the next dated instance when completed.
- **Why time first** — For a household routine, “when is something due?” is the main coordination question; priority can be layered later (e.g., tie-break or optimization pass).

**b. Tradeoffs**

- **Exact-time conflicts only** — `detect_conflicts` treats a clash as the same **date and start time string** only. It ignores overlapping **durations** (e.g., a 60-minute walk starting at 09:00 vs. a 30-minute slot at 09:30).
- **Why that’s reasonable** — No duration-aware calendar engine is required for the module scope; owners still get a clear signal for double-booked start times. A future version could convert intervals to minutes and detect overlaps.

---

## 3. AI Collaboration

**a. How you used AI**

- **Brainstorming & structure** — AI helped turn the written scenario into concrete classes, a Mermaid sketch, and a sensible split between domain objects (`Owner`, `Pet`, `Task`) and the `Scheduler` service.
- **Implementation speed** — Generating stubs, edge-case ideas (empty pet list, duplicate times), and pytest outlines reduced boilerplate so effort could go into behavior and tests.
- **Helpful prompts** — “What should happen when a daily task is marked complete?” and “What edge cases matter for a pet scheduler?” produced checklists that shaped `main.py` and `tests/test_pawpal.py`.

**b. Judgment and verification**

- **Rejected / adapted:** A fuller “AI optimizer” that **re-sorted by priority** was set aside to keep ordering **time-primary** and predictable for a classroom demo; priority remains visible data for a future iteration.
- **Verification** — Every behavioral change ran through `python3 main.py` and `python3 -m pytest`; failing tests were treated as ground truth for fixing logic before adjusting the Streamlit layer.

---

## 4. Testing and Verification

**a. What you tested**

- **Completion and addition** — Baseline object behavior (`mark_complete`, `add_task` count).
- **Sorting** — Chronological order for `HH:MM` strings on a fixed day.
- **Daily recurrence** — Completing a daily task yields exactly one new instance on the next calendar day.
- **Conflicts** — Two pets with the same start time on the same day trigger `detect_conflicts`.
- **Empty schedule** — A pet with no tasks still runs through `sort_by_time` without failure.

These tests guard the behaviors users see in both `main.py` and Streamlit: ordering, recurrence after “done,” and visible warnings.

**b. Confidence**

- **Rating:** about **4/5** — Happy paths and several edge cases are automated; the design is small enough to reason about by hand.
- **Next edge cases:** weekly recurrence with month boundaries; tasks at `24:00` or invalid time strings; partial overlaps using duration; multi-day “appointments”; persistence across browser sessions (database or file store).

---

## 5. Reflection

**a. What went well**

- **CLI-first workflow** — Proving scheduling, recurrence, and conflicts in `main.py` before Streamlit avoided UI-only bugs and made pytest cases easy to justify.
- **Small, composable classes** — Dataclasses with a thin `Scheduler` kept responsibilities clear and the test surface area understandable.

**b. What you would improve**

- **Priority-aware scheduling** — Use priority as a tie-breaker or optimization layer once duration-overlap detection exists.
- **Persistence** — `st.session_state` is enough for a demo; a file or database would separate “demo app” from “personal tracker.”

**c. Key takeaway**

- **Lead architect with AI:** The model accelerates draft code and test ideas, but humans still own invariants (what “conflict” means, how recurrence advances) and must verify with runnable checks—separate chat topics for “design” vs “testing” vs “algorithms” reduce confusion and tangled prompts.

### VS Code Copilot (module prompt alignment)

- **Effective features:** Chat/codebase questions for wiring `Scheduler` to `Owner`, inline refactors for readable terminal output, and test generation scaffolds.
- **Example rejection:** Skipping automatic **priority re-ordering** to preserve a clear **time-ordered** mental model for owners (see 3b).
- **Separate sessions:** Treating design, algorithms, and testing as distinct conversations mirrors how a team works in tickets—fewer contradictory suggestions and easier commits per concern.
- **Role of the human:** Decide boundaries (exact-time conflicts only), acceptable tradeoffs, and what “done” means; use AI to draft, not to override product judgment.
