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
    pet.add_task(Task(description="Later", time="09:00", frequency="daily"))
    pet.add_task(Task(description="Sooner", time="07:30", frequency="daily"))
    owner.add_pet(pet)

    scheduler = Scheduler(owner)
    plan = scheduler.generate_daily_plan()
    assert [t.time for t in plan] == ["07:30", "09:00"]


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

