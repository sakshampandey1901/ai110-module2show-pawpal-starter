"""PawPal+ logic layer — Owner, Pet, Task, and Scheduler."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import List, Optional


def _time_sort_key(clock: str) -> tuple[int, int]:
    """Parse HH:MM into a tuple for stable chronological order."""
    parts = clock.strip().split(":")
    hour = int(parts[0]) if parts else 0
    minute = int(parts[1]) if len(parts) > 1 else 0
    return (hour, minute)


@dataclass
class Task:
    """A single care activity for a pet."""

    description: str
    time: str
    task_date: date
    frequency: str = "once"
    completed: bool = False
    duration_minutes: int = 30
    priority: str = "medium"
    pet_name: Optional[str] = None

    def mark_complete(self) -> Optional[Task]:
        """Mark this task complete; return a follow-up task for recurring schedules, if any."""
        self.completed = True
        if self.frequency == "daily":
            return Task(
                description=self.description,
                time=self.time,
                task_date=self.task_date + timedelta(days=1),
                frequency=self.frequency,
                completed=False,
                duration_minutes=self.duration_minutes,
                priority=self.priority,
                pet_name=self.pet_name,
            )
        if self.frequency == "weekly":
            return Task(
                description=self.description,
                time=self.time,
                task_date=self.task_date + timedelta(weeks=1),
                frequency=self.frequency,
                completed=False,
                duration_minutes=self.duration_minutes,
                priority=self.priority,
                pet_name=self.pet_name,
            )
        return None


@dataclass
class Pet:
    """A pet with a list of care tasks."""

    name: str
    species: str = "other"
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Attach a task to this pet."""
        task.pet_name = self.name
        self.tasks.append(task)

    def complete_task(self, task: Task) -> Optional[Task]:
        """Mark a task done and enqueue the next occurrence when recurring."""
        if task not in self.tasks:
            raise ValueError(f"Task not owned by pet {self.name!r}")
        follow_up = task.mark_complete()
        if follow_up is not None:
            self.add_task(follow_up)
        return follow_up


@dataclass
class Owner:
    """Pet owner managing multiple pets."""

    name: str
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Register a pet with this owner."""
        self.pets.append(pet)

    def get_pet(self, name: str) -> Optional[Pet]:
        """Look up a pet by name."""
        for p in self.pets:
            if p.name == name:
                return p
        return None

    def all_tasks(self) -> List[Task]:
        """All tasks across every pet."""
        combined: List[Task] = []
        for pet in self.pets:
            combined.extend(pet.tasks)
        return combined


class Scheduler:
    """Collects tasks from an owner and applies ordering and checks."""

    def __init__(self, owner: Owner) -> None:
        self.owner = owner

    def tasks_for_date(self, on_date: date) -> List[Task]:
        """Tasks scheduled on a given calendar day (any pet)."""
        return [t for t in self.owner.all_tasks() if t.task_date == on_date]

    def sort_by_time(self, tasks: List[Task]) -> List[Task]:
        """Return tasks ordered by time of day (HH:MM)."""
        return sorted(tasks, key=lambda t: (_time_sort_key(t.time), t.description))

    def filter_tasks(
        self,
        tasks: List[Task],
        *,
        completed: Optional[bool] = None,
        pet_name: Optional[str] = None,
    ) -> List[Task]:
        """Filter by completion and/or pet name."""
        result = tasks
        if completed is not None:
            result = [t for t in result if t.completed is completed]
        if pet_name is not None:
            result = [t for t in result if t.pet_name == pet_name]
        return result

    def detect_conflicts(self, tasks: List[Task]) -> List[str]:
        """Return human-readable warnings when multiple tasks share the same date and time."""
        by_slot: dict[tuple[date, str], List[Task]] = {}
        for task in tasks:
            key = (task.task_date, task.time.strip())
            by_slot.setdefault(key, []).append(task)
        warnings: List[str] = []
        for (day, clock), group in by_slot.items():
            if len(group) < 2:
                continue
            detail = ", ".join(
                f"{t.description!r} ({t.pet_name or '?'})" for t in group
            )
            warnings.append(f"Conflict on {day.isoformat()} at {clock}: {detail}")
        return warnings
