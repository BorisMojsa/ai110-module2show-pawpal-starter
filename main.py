from pawpal_system import Owner, Pet, Task, Scheduler

owner = Owner("Boris")

dog = Pet("Bella", "Dog", 3)
cat = Pet("Milo", "Cat", 2)

# Add tasks out of order (to prove sorting works).
task1 = Task("Feed Bella", "09:00", "daily")
task2 = Task("Morning walk", "08:00", "daily")
task3 = Task("Feed Milo", "07:30", "daily")
task4 = Task("Brush Milo", "08:00", "weekly")  # same time as Morning walk (conflict)

dog.add_task(task1)
dog.add_task(task2)
cat.add_task(task3)
cat.add_task(task4)

owner.add_pet(dog)
owner.add_pet(cat)

scheduler = Scheduler(owner)

def print_schedule(title: str, rows: list[tuple[str, str, str, str, bool]]) -> None:
    print(title)
    print("-" * len(title))
    print(f"{'Date':<10}  {'Time':<5}  {'Pet':<5}  {'Task':<13}  Status")
    for due_date, time, pet_name, description, completed in rows:
        status = "[x]" if completed else "[ ]"
        print(f"{due_date:<10}  {time:<5}  {pet_name:<5}  {description:<13}  {status}")
    print()

# 1) Sorted daily plan (time order)
rows_all = []
for pet in owner.get_pets():
    for task in pet.get_tasks():
        rows_all.append(
            (task.due_date.isoformat(), task.time, pet.name, task.description, task.completed)
        )

rows_all_sorted = sorted(rows_all, key=lambda r: Scheduler._time_to_minutes(r[1]))
print_schedule("PawPal+ — Today's Schedule", rows_all_sorted)

# 1b) Conflicts (lightweight warnings)
conflicts = scheduler.detect_conflicts()
if conflicts:
    print("Warnings")
    print("--------")
    for message in conflicts:
        print(f"- {message}")
    print()

# 2) Filtering examples (using Scheduler.filter_tasks)
milo_tasks = scheduler.filter_tasks(pet_name="Milo")
milo_rows = sorted(
    [(t.due_date.isoformat(), t.time, "Milo", t.description, t.completed) for t in milo_tasks],
    key=lambda r: Scheduler._time_to_minutes(r[1]),
)
print_schedule("Filtered — Milo only", milo_rows)

incomplete_tasks = scheduler.filter_tasks(completed=False)
incomplete_rows = []
for pet in owner.get_pets():
    for task in pet.get_tasks():
        if task in incomplete_tasks:
            incomplete_rows.append(
                (task.due_date.isoformat(), task.time, pet.name, task.description, task.completed)
            )

incomplete_rows = sorted(incomplete_rows, key=lambda r: Scheduler._time_to_minutes(r[1]))
print_schedule("Filtered — Incomplete only", incomplete_rows)

# 3) Recurring tasks demo: completing a daily task auto-creates the next day
scheduler.mark_task_complete("Milo", task3)
milo_plan = scheduler.generate_daily_plan(pet_name="Milo", include_completed=True, day_of_week="monday")
milo_plan_rows = []
for task in milo_plan:
    milo_plan_rows.append(
        (task.due_date.isoformat(), task.time, "Milo", task.description, task.completed)
    )
milo_plan_rows = sorted(milo_plan_rows, key=lambda r: (r[0], Scheduler._time_to_minutes(r[1])))
print_schedule("Recurring demo — Milo after completion", milo_plan_rows)
