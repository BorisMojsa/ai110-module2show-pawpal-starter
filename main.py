from pawpal_system import Owner, Pet, Task, Scheduler

owner = Owner("Boris")

dog = Pet("Bella", "Dog", 3)
cat = Pet("Milo", "Cat", 2)

task1 = Task("Morning walk", "08:00", "daily")
task2 = Task("Feed Bella", "09:00", "daily")
task3 = Task("Feed Milo", "07:30", "daily")

dog.add_task(task1)
dog.add_task(task2)
cat.add_task(task3)

owner.add_pet(dog)
owner.add_pet(cat)

scheduler = Scheduler(owner)

plan = scheduler.generate_daily_plan()

print("PawPal+ — Today's Schedule")
print("-" * 26)
print(f"{'Time':<5}  {'Pet':<5}  {'Task':<13}  Status")

rows = []
for pet in owner.get_pets():
    for task in pet.get_tasks():
        rows.append((task.time, pet.name, task.description, task.completed))

rows = sorted(rows, key=lambda r: r[0])

for time, pet_name, description, completed in rows:
    status = "[x]" if completed else "[ ]"
    print(f"{time:<5}  {pet_name:<5}  {description:<13}  {status}")
