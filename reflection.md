# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

For my initial design, I chose four main classes: Owner, Pet, Task, and Scheduler.

The Owner class is responsible for storing the owner's name and managing multiple pets. It acts as the main container for the system.

The Pet class is responsible for storing basic pet information, such as name, species, and age, along with that pet's list of care tasks.

The Task class represents one pet care activity, such as feeding, walking, medication, or an appointment. It stores the task details like description, time, duration, priority, and completion status.

The Scheduler class is responsible for gathering tasks from the owner's pets and organizing them into a daily schedule. Its purpose is to help sort and manage the tasks in one place.

**b. Design changes**


After reviewing my class skeleton with Copilot, I did not make any major design changes. The main relationships were already clear: the Owner manages multiple pets, each Pet stores its own tasks, and the Scheduler works through the Owner to access and organize tasks.

The review did help me notice a few implementation details to be careful with later, such as keeping the task time format consistent and avoiding duplicated logic between Owner.get_all_tasks() and Scheduler.get_all_tasks(). I decided to keep the design simple for now so it stays aligned with the project requirements.
---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- My scheduler primarily considers **time order** (sorting tasks by their `"HH:MM"` value) and **completion status** (optionally excluding completed tasks from the daily plan).
- I chose these constraints first because they are the most visible and useful for a pet owner: you want a clear chronological list of what to do next, and you usually want the plan to focus on what still needs to be done.

**b. Tradeoffs**

- My scheduler only checks for **exact time conflicts** (two tasks with the same `"HH:MM"`), rather than detecting overlapping tasks based on durations.
- This tradeoff is reasonable for this starter version because my `Task` model keeps time as a simple string and does not track a start/end range. Exact-match conflict warnings are easy to understand, quick to compute, and still help the owner spot obvious scheduling problems.

---

## 3. AI Collaboration

**a. How you used AI**

- I used Copilot to brainstorm a small, realistic UML design, to generate initial class skeletons, and to help draft simple algorithms (sorting by time, filtering, recurrence rollover, and conflict warnings).
- The most helpful prompts were specific and constrained, like: “add a beginner-friendly filter method,” “sort HH:MM times safely,” and “write a small pytest for daily recurrence.”

**b. Judgment and verification**

- One suggestion I modified was adding more advanced scheduling features (like durations, priorities, and overlap detection). I rejected that scope increase to keep the system aligned with the four-class design and the project requirements.
- I verified changes by running the CLI demo (`main.py`) and writing/expanding pytest tests to confirm behavior (sorting, conflicts, recurrence) before committing.

---

## 4. Testing and Verification

**a. What you tested**

- I tested task completion, adding tasks to a pet, sorting tasks by time, daily recurrence creating the next-day task, conflict detection for duplicate times, and the edge case of a pet with no tasks.
- These tests are important because they verify the “smart” behaviors are correct and prevent regressions when I make changes to the scheduler logic.

**b. Confidence**

- I’m reasonably confident (about 4/5) because the key behaviors are covered by automated tests and the CLI demo shows the same results.
- Next, I would test time-format edge cases (invalid `"HH:MM"` input), weekly recurrence rules tied to an actual weekday, and more complex conflict cases (like overlap checking if durations were added back).

---

## 5. Reflection

**a. What went well**

- I’m most satisfied with keeping the design small and consistent (Owner → Pets → Tasks, plus a Scheduler) while still adding “smart” behaviors like sorting, filtering, recurrence rollover, and conflict warnings.

**b. What you would improve**

- I would improve how times/dates are represented (moving from strings to stronger types or validation), and I would refine recurrence to be more realistic (for example, weekly tasks on a specific day).

**c. Key takeaway**

- My key takeaway is that AI is most effective when I stay the “lead architect”: I set constraints, review suggestions critically, and verify behavior with small demos and tests. Using separate chat sessions per phase helped keep context focused and prevented scope creep.
