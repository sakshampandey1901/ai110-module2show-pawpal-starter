"""PawPal+ logic layer — Owner, Pet, Task, and Scheduler (skeleton phase)."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import List, Optional


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
        """Mark complete and return a follow-up task for recurring schedules, if any."""
        raise NotImplementedError


@dataclass
class Pet:
    """A pet with a list of care tasks."""

    name: str
    species: str = "other"
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Attach a task to this pet."""
        raise NotImplementedError

    def complete_task(self, task: Task) -> Optional[Task]:
        """Mark a task done and enqueue the next occurrence when recurring."""
        raise NotImplementedError


@dataclass
class Owner:
    """Pet owner managing multiple pets."""

    name: str
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Register a pet with this owner."""
        raise NotImplementedError

    def get_pet(self, name: str) -> Optional[Pet]:
        """Look up a pet by name."""
        raise NotImplementedError

    def all_tasks(self) -> List[Task]:
        """All tasks across every pet."""
        raise NotImplementedError


class Scheduler:
    """Collects tasks from an owner and applies ordering and checks."""

    def __init__(self, owner: Owner) -> None:
        self.owner = owner

    def tasks_for_date(self, on_date: date) -> List[Task]:
        """Tasks scheduled on a given calendar day (any pet)."""
        raise NotImplementedError

    def sort_by_time(self, tasks: List[Task]) -> List[Task]:
        """Return tasks ordered by time of day (HH:MM)."""
        raise NotImplementedError

    def filter_tasks(
        self,
        tasks: List[Task],
        *,
        completed: Optional[bool] = None,
        pet_name: Optional[str] = None,
    ) -> List[Task]:
        """Filter by completion and/or pet name."""
        raise NotImplementedError

    def detect_conflicts(self, tasks: List[Task]) -> List[str]:
        """Return human-readable warnings for tasks sharing the same date and time."""
        raise NotImplementedError
