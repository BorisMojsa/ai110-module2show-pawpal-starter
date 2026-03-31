from pawpal_system import Pet, Task


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

