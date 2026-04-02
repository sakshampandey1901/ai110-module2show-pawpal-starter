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

- *(Updated in later phases if the model diverges from this blueprint.)*

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

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
