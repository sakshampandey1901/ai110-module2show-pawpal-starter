"""Tests for PawPal+ core behaviors."""

from datetime import date, timedelta

from pawpal_system import Owner, Pet, Scheduler, Task


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


def test_sort_by_time_chronological() -> None:
    d = date(2026, 4, 1)
    owner = Owner(name="A")
    p = Pet(name="P", species="dog")
    owner.add_pet(p)
    p.add_task(Task("Late", "18:00", d))
    p.add_task(Task("Early", "07:00", d))
    p.add_task(Task("Noon", "12:30", d))
    sched = Scheduler(owner)
    raw = sched.tasks_for_date(d)
    ordered = sched.sort_by_time(raw)
    assert [t.description for t in ordered] == ["Early", "Noon", "Late"]


def test_daily_recurrence_after_complete() -> None:
    d = date(2026, 4, 1)
    pet = Pet(name="Mochi", species="dog")
    t = Task("Meds", "08:00", d, frequency="daily")
    pet.add_task(t)
    pet.complete_task(t)
    assert t.completed
    next_days = [x for x in pet.tasks if x.task_date == d + timedelta(days=1) and not x.completed]
    assert len(next_days) == 1
    assert next_days[0].description == "Meds"
    assert next_days[0].frequency == "daily"


def test_conflict_detection_duplicate_time() -> None:
    d = date(2026, 4, 1)
    owner = Owner(name="A")
    p1 = Pet(name="A", species="dog")
    p2 = Pet(name="B", species="cat")
    owner.add_pet(p1)
    owner.add_pet(p2)
    p1.add_task(Task("One", "10:00", d))
    p2.add_task(Task("Two", "10:00", d))
    sched = Scheduler(owner)
    warnings = sched.detect_conflicts(sched.tasks_for_date(d))
    assert len(warnings) == 1
    assert "10:00" in warnings[0]
    assert "One" in warnings[0]
    assert "Two" in warnings[0]


def test_pet_with_no_tasks_sorts_empty() -> None:
    owner = Owner(name="Lonely")
    owner.add_pet(Pet(name="Solo", species="dog"))
    sched = Scheduler(owner)
    assert sched.sort_by_time(sched.tasks_for_date(date.today())) == []
