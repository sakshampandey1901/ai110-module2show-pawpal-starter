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

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
