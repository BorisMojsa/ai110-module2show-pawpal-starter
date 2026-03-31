from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, timedelta
import json
from pathlib import Path
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

    def save_to_json(self, path: str = "data.json") -> None:
        """Save this owner, pets, and tasks to a JSON file."""
        data = {
            "owner": {
                "name": self.name,
                "pets": [
                    {
                        "name": pet.name,
                        "species": pet.species,
                        "age": pet.age,
                        "tasks": [
                            {
                                "description": task.description,
                                "time": task.time,
                                "frequency": task.frequency,
                                "due_date": task.due_date.isoformat(),
                                "priority": task.priority,
                                "completed": task.completed,
                            }
                            for task in pet.get_tasks()
                        ],
                    }
                    for pet in self.get_pets()
                ],
            }
        }
        Path(path).write_text(json.dumps(data, indent=2), encoding="utf-8")

    @staticmethod
    def load_from_json(path: str = "data.json") -> "Owner":
        """Load an owner, pets, and tasks from a JSON file (or return a blank owner)."""
        file_path = Path(path)
        if not file_path.exists():
            return Owner("Jordan")

        raw = json.loads(file_path.read_text(encoding="utf-8"))
        owner_raw = raw.get("owner", {})
        owner = Owner(owner_raw.get("name", "Jordan"))

        for pet_raw in owner_raw.get("pets", []):
            pet = Pet(
                name=pet_raw.get("name", "Unknown"),
                species=pet_raw.get("species", "other"),
                age=int(pet_raw.get("age", 0)),
            )
            for task_raw in pet_raw.get("tasks", []):
                due_date_str = task_raw.get("due_date")
                due = date.fromisoformat(due_date_str) if due_date_str else date.today()
                pet.add_task(
                    Task(
                        description=task_raw.get("description", ""),
                        time=task_raw.get("time", "00:00"),
                        frequency=task_raw.get("frequency", "once"),
                        due_date=due,
                        priority=task_raw.get("priority", "medium"),
                        completed=bool(task_raw.get("completed", False)),
                    )
                )
            owner.add_pet(pet)

        return owner


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
    due_date: date = field(default_factory=date.today)
    priority: str = "medium"  # "low" | "medium" | "high"
    completed: bool = False

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.completed = True

    def create_next_occurrence(self) -> Optional["Task"]:
        """Create the next recurring task instance (or None if not recurring)."""
        freq = self.frequency.strip().lower()
        if freq == "daily":
            next_date = self.due_date + timedelta(days=1)
        elif freq == "weekly":
            next_date = self.due_date + timedelta(days=7)
        else:
            return None

        return Task(
            description=self.description,
            time=self.time,
            frequency=self.frequency,
            due_date=next_date,
            priority=self.priority,
            completed=False,
        )


class Scheduler:
    owner: Owner

    def __init__(self, owner: Owner) -> None:
        """Create a scheduler for a specific owner."""
        self.owner = owner

    @staticmethod
    def _time_to_minutes(time_str: str) -> int:
        """Convert 'HH:MM' into minutes since midnight (invalid -> large)."""
        try:
            hh_str, mm_str = time_str.split(":")
            hh = int(hh_str)
            mm = int(mm_str)
            if 0 <= hh <= 23 and 0 <= mm <= 59:
                return hh * 60 + mm
        except Exception:
            pass
        return 24 * 60 + 1

    def get_all_tasks(self) -> List[Task]:
        """Return all tasks across the owner's pets."""
        return self.owner.get_all_tasks()

    def filter_tasks(
        self, pet_name: Optional[str] = None, completed: Optional[bool] = None
    ) -> List[Task]:
        """Return tasks filtered by pet name and/or completion status."""
        tasks: List[Task] = []
        for pet in self.owner.get_pets():
            if pet_name is not None and pet.name != pet_name:
                continue
            for task in pet.get_tasks():
                if completed is not None and task.completed != completed:
                    continue
                tasks.append(task)
        return tasks

    def mark_task_complete(self, pet_name: str, task: Task) -> None:
        """Mark a task complete and auto-create the next recurring instance."""
        task.mark_complete()
        next_task = task.create_next_occurrence()
        if next_task is None:
            return

        for pet in self.owner.get_pets():
            if pet.name == pet_name:
                pet.add_task(next_task)
                return

    def sort_tasks(self, tasks: Optional[List[Task]] = None) -> List[Task]:
        """Return tasks sorted by priority (high->low), then by time (HH:MM)."""
        tasks_to_sort = self.get_all_tasks() if tasks is None else tasks
        priority_rank = {"high": 0, "medium": 1, "low": 2}
        return sorted(
            tasks_to_sort,
            key=lambda task: (
                priority_rank.get(task.priority.strip().lower(), 99),
                self._time_to_minutes(task.time),
            ),
        )

    def detect_conflicts(self, tasks: Optional[List[Task]] = None) -> List[str]:
        """Return conflict messages for tasks that share the same time."""
        tasks_to_check = self.get_all_tasks() if tasks is None else tasks
        by_time: dict[str, List[Task]] = {}
        for task in tasks_to_check:
            by_time.setdefault(task.time, []).append(task)

        conflicts: List[str] = []
        for time, bucket in sorted(
            by_time.items(), key=lambda item: self._time_to_minutes(item[0])
        ):
            if len(bucket) > 1:
                descriptions = ", ".join(t.description for t in bucket)
                conflicts.append(f"Conflict at {time}: {descriptions}")
        return conflicts

    def next_available_time(
        self, desired_time: str, *, step_minutes: int = 15, tasks: Optional[List[Task]] = None
    ) -> str:
        """Suggest the next available time that doesn't conflict with existing tasks."""
        tasks_to_check = self.get_all_tasks() if tasks is None else tasks
        taken = {t.time for t in tasks_to_check}

        current = self._time_to_minutes(desired_time)
        if current >= 24 * 60:
            current = 0

        for _ in range((24 * 60) // max(step_minutes, 1)):
            hh = current // 60
            mm = current % 60
            candidate = f"{hh:02d}:{mm:02d}"
            if candidate not in taken:
                return candidate
            current = (current + step_minutes) % (24 * 60)

        return desired_time

    def generate_daily_plan(
        self,
        *,
        pet_name: Optional[str] = None,
        include_completed: bool = False,
        day_of_week: Optional[str] = None,
    ) -> List[Task]:
        """Generate a sorted daily plan with simple recurring rules."""
        tasks = self.filter_tasks(
            pet_name=pet_name, completed=None if include_completed else False
        )

        if day_of_week is not None:
            day_of_week = day_of_week.strip().lower()

        def should_include(task: Task) -> bool:
            freq = task.frequency.strip().lower()
            if freq in ("daily", "once"):
                return True
            if freq == "weekly":
                return day_of_week is not None
            return True

        filtered = [t for t in tasks if should_include(t)]
        return self.sort_tasks(filtered)
