"""CLI demo: verify Owner, Pet, Task, and Scheduler without the Streamlit UI."""

from datetime import date

from pawpal_system import Owner, Pet, Scheduler, Task


def format_schedule_line(task: Task) -> str:
    """Single-line display for terminal output."""
    pet = task.pet_name or "?"
    flag = "✓" if task.completed else " "
    return f"  [{flag}] {task.time}  {task.description}  ({pet}, {task.priority})"


def main() -> None:
    today = date.today()
    owner = Owner(name="Jordan")
    mochi = Pet(name="Mochi", species="dog")
    whiskers = Pet(name="Whiskers", species="cat")
    owner.add_pet(mochi)
    owner.add_pet(whiskers)

    # Tasks added out of chronological order on purpose (sorting demo).
    mochi.add_task(
        Task("Evening walk", "18:30", today, duration_minutes=25, priority="high")
    )
    whiskers.add_task(Task("Morning meds", "08:00", today, priority="high"))
    mochi.add_task(Task("Breakfast", "07:30", today, duration_minutes=10, priority="medium"))
    whiskers.add_task(
        Task("Play session", "12:00", today, duration_minutes=15, priority="low")
    )

    scheduler = Scheduler(owner)
    todays = scheduler.tasks_for_date(today)
    ordered = scheduler.sort_by_time(todays)
    pending_only = scheduler.filter_tasks(ordered, completed=False)

    print(f"\n=== PawPal+ — Today's schedule for {owner.name} ({today.isoformat()}) ===\n")
    for task in pending_only:
        print(format_schedule_line(task))

    print("\n--- Sorted all tasks (including completed, if any) ---")
    for task in ordered:
        print(format_schedule_line(task))

    # Conflict demo: same time, different pets
    dup_time = Task("Grooming", "12:00", today, priority="low")
    mochi.add_task(dup_time)
    conflicts = scheduler.detect_conflicts(scheduler.tasks_for_date(today))
    if conflicts:
        print("\n--- Conflict warnings ---")
        for msg in conflicts:
            print(f"  ⚠ {msg}")


if __name__ == "__main__":
    main()
