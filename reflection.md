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

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- My scheduler only checks for **exact time conflicts** (two tasks with the same `"HH:MM"`), rather than detecting overlapping tasks based on durations.
- This tradeoff is reasonable for this starter version because my `Task` model keeps time as a simple string and does not track a start/end range. Exact-match conflict warnings are easy to understand, quick to compute, and still help the owner spot obvious scheduling problems.

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
