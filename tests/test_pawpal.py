"""Tests for PawPal+ core behaviors."""

from datetime import date

from pawpal_system import Pet, Task


def test_mark_complete_sets_status() -> None:
    t = Task("Walk", "09:00", date.today(), frequency="once")
    assert not t.completed
    t.mark_complete()
    assert t.completed


def test_add_task_increases_pet_task_count() -> None:
    pet = Pet(name="Mochi", species="dog")
    assert len(pet.tasks) == 0
    pet.add_task(Task("Feed", "08:00", date.today()))
    assert len(pet.tasks) == 1
    pet.add_task(Task("Walk", "17:00", date.today()))
    assert len(pet.tasks) == 2
