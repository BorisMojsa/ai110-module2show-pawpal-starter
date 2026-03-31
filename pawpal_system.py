from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional


class Owner:
    name: str
    pets: List[Pet]

    def __init__(self, name: str) -> None:
        """Create an owner with an empty pet list."""
        self.name = name
        self.pets = []

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner."""
        self.pets.append(pet)

    def get_pets(self) -> List[Pet]:
        """Return this owner's pets."""
        return list(self.pets)

    def get_all_tasks(self) -> List[Task]:
        """Return all tasks across all pets."""
        all_tasks: List[Task] = []
        for pet in self.pets:
            all_tasks.extend(pet.get_tasks())
        return all_tasks


@dataclass
class Pet:
    name: str
    species: str
    age: int
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task for this pet."""
        self.tasks.append(task)

    def get_tasks(self) -> List[Task]:
        """Return this pet's tasks."""
        return list(self.tasks)


@dataclass
class Task:
    description: str
    time: str  # "HH:MM"
    frequency: str
    completed: bool = False

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.completed = True


class Scheduler:
    owner: Owner

    def __init__(self, owner: Owner) -> None:
        """Create a scheduler for a specific owner."""
        self.owner = owner

    def get_all_tasks(self) -> List[Task]:
        """Return all tasks across the owner's pets."""
        return self.owner.get_all_tasks()

    def sort_tasks(self, tasks: Optional[List[Task]] = None) -> List[Task]:
        """Return tasks sorted by time (HH:MM)."""
        tasks_to_sort = self.get_all_tasks() if tasks is None else tasks
        return sorted(tasks_to_sort, key=lambda task: task.time)

    def generate_daily_plan(self) -> List[Task]:
        """Generate a daily plan as a sorted task list."""
        return self.sort_tasks()
