from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional


class Owner:
    name: str
    pets: List[Pet]

    def __init__(self, name: str) -> None:
        self.name = name
        self.pets = []

    def add_pet(self, pet: Pet) -> None:
        pass

    def get_pets(self) -> List[Pet]:
        pass

    def get_all_tasks(self) -> List[Task]:
        pass


@dataclass
class Pet:
    name: str
    species: str
    age: int
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        pass

    def get_tasks(self) -> List[Task]:
        pass


@dataclass
class Task:
    description: str
    time: str
    duration: int
    priority: int
    completed: bool = False

    def mark_complete(self) -> None:
        pass


class Scheduler:
    owner: Owner

    def __init__(self, owner: Owner) -> None:
        self.owner = owner

    def get_all_tasks(self) -> List[Task]:
        pass

    def sort_tasks(self, tasks: Optional[List[Task]] = None) -> List[Task]:
        pass

    def generate_daily_plan(self) -> List[Task]:
        pass
