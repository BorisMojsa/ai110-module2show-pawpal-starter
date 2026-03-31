from datetime import date

from pawpal_system import Owner, Pet, Scheduler, Task


def test_task_mark_complete_sets_completed_true() -> None:
    task = Task(description="Feed", time="07:30", frequency="daily")
    assert task.completed is False
    task.mark_complete()
    assert task.completed is True


def test_pet_add_task_increases_task_count() -> None:
    pet = Pet(name="Milo", species="Cat", age=2)
    assert len(pet.get_tasks()) == 0
    pet.add_task(Task(description="Feed Milo", time="07:30", frequency="daily"))
    assert len(pet.get_tasks()) == 1


def test_scheduler_sorts_by_time_hhmm() -> None:
    owner = Owner("Jordan")
    pet = Pet(name="Milo", species="Cat", age=2)
    pet.add_task(Task(description="Later", time="09:00", frequency="daily", priority="low"))
    pet.add_task(Task(description="Sooner", time="07:30", frequency="daily", priority="low"))
    owner.add_pet(pet)

    scheduler = Scheduler(owner)
    plan = scheduler.generate_daily_plan()
    assert [t.time for t in plan] == ["07:30", "09:00"]


def test_scheduler_sorts_by_priority_then_time() -> None:
    owner = Owner("Jordan")
    pet = Pet(name="Milo", species="Cat", age=2)
    pet.add_task(Task(description="Low first", time="07:30", frequency="daily", priority="low"))
    pet.add_task(Task(description="High later", time="09:00", frequency="daily", priority="high"))
    pet.add_task(Task(description="High sooner", time="08:00", frequency="daily", priority="high"))
    owner.add_pet(pet)

    scheduler = Scheduler(owner)
    plan = scheduler.generate_daily_plan()
    assert [t.description for t in plan] == ["High sooner", "High later", "Low first"]


def test_scheduler_detects_same_time_conflict() -> None:
    owner = Owner("Jordan")
    pet = Pet(name="Milo", species="Cat", age=2)
    pet.add_task(Task(description="Feed", time="07:30", frequency="daily"))
    pet.add_task(Task(description="Med", time="07:30", frequency="daily"))
    owner.add_pet(pet)

    scheduler = Scheduler(owner)
    conflicts = scheduler.detect_conflicts()
    assert len(conflicts) == 1
    assert "Conflict at 07:30" in conflicts[0]


def test_recurrence_daily_creates_next_day_task_on_completion() -> None:
    owner = Owner("Jordan")
    pet = Pet(name="Milo", species="Cat", age=2)
    today = date(2026, 3, 31)
    task = Task(
        description="Feed Milo", time="07:30", frequency="daily", due_date=today, priority="medium"
    )
    pet.add_task(task)
    owner.add_pet(pet)

    scheduler = Scheduler(owner)
    scheduler.mark_task_complete("Milo", task)

    tasks = pet.get_tasks()
    assert len(tasks) == 2

    completed = [t for t in tasks if t.completed]
    upcoming = [t for t in tasks if not t.completed]
    assert len(completed) == 1
    assert len(upcoming) == 1
    assert upcoming[0].due_date == date(2026, 4, 1)
    assert upcoming[0].description == "Feed Milo"
    assert upcoming[0].time == "07:30"


def test_next_available_time_skips_conflicts() -> None:
    owner = Owner("Jordan")
    pet = Pet(name="Milo", species="Cat", age=2)
    pet.add_task(Task(description="Task A", time="08:00", frequency="once"))
    pet.add_task(Task(description="Task B", time="08:15", frequency="once"))
    owner.add_pet(pet)

    scheduler = Scheduler(owner)
    assert scheduler.next_available_time("08:00", step_minutes=15) == "08:30"


def test_generate_daily_plan_handles_pet_with_no_tasks() -> None:
    owner = Owner("Jordan")
    owner.add_pet(Pet(name="Mochi", species="dog", age=3))
    scheduler = Scheduler(owner)
    assert scheduler.generate_daily_plan() == []

