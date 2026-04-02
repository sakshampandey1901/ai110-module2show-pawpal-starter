"""PawPal+ Streamlit UI wired to pawpal_system."""

from datetime import date

import streamlit as st

from pawpal_system import Owner, Pet, Scheduler, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

KEY_OWNER = "pawpal_owner"


def get_owner() -> Owner:
    """Return the persistent Owner from session state."""
    if KEY_OWNER not in st.session_state:
        st.session_state[KEY_OWNER] = Owner(name="Jordan")
    return st.session_state[KEY_OWNER]


def get_scheduler(owner: Owner) -> Scheduler:
    return Scheduler(owner)


st.title("🐾 PawPal+")
st.caption("Smart pet care routines — backend powered by pawpal_system.py")

owner = get_owner()
sched = get_scheduler(owner)

with st.expander("Scenario", expanded=False):
    st.markdown(
        """
**PawPal+** helps you plan feedings, walks, medications, and appointments with sorting,
filtering, recurrence, and simple time-slot conflict warnings.
"""
    )

st.subheader("Owner")
new_owner_name = st.text_input("Owner name", value=owner.name, key="owner_name_input")
if new_owner_name.strip():
    owner.name = new_owner_name.strip()

st.subheader("Pets")
pc1, pc2 = st.columns(2)
with pc1:
    new_pet_name = st.text_input("New pet name", key="new_pet_name")
with pc2:
    new_pet_species = st.selectbox("Species", ["dog", "cat", "other"], key="new_pet_species")

if st.button("Add pet"):
    name = (new_pet_name or "").strip()
    if not name:
        st.warning("Enter a pet name.")
    elif owner.get_pet(name):
        st.warning(f"You already have a pet named {name!r}.")
    else:
        owner.add_pet(Pet(name=name, species=new_pet_species))
        st.success(f"Added {name} ({new_pet_species}).")
        st.rerun()

if owner.pets:
    st.write("Your pets:", ", ".join(f"{p.name} ({p.species})" for p in owner.pets))
else:
    st.info("Add at least one pet to schedule tasks.")

st.divider()
st.subheader("Add task")

task_date = st.date_input("Task date", value=date.today())
task_time = st.text_input("Time (HH:MM)", value="09:00")
task_title = st.text_input("Task description", value="Morning walk")
task_duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
task_priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
task_frequency = st.selectbox("Frequency", ["once", "daily", "weekly"])

pet_names = [p.name for p in owner.pets]
task_pet = st.selectbox("Pet", pet_names) if pet_names else None

if st.button("Add task") and pet_names and task_pet:
    pet = owner.get_pet(task_pet)
    assert pet is not None
    pet.add_task(
        Task(
            description=task_title.strip() or "Task",
            time=task_time.strip(),
            task_date=task_date,
            frequency=task_frequency,
            duration_minutes=int(task_duration),
            priority=task_priority,
        )
    )
    st.success("Task added.")
    st.rerun()

st.divider()
st.subheader("Today's schedule")

view_date = st.date_input("Schedule date", value=date.today(), key="schedule_view_date")

filter_pet = st.selectbox("Filter by pet", ["(all)"] + pet_names) if pet_names else "(all)"
show_completed = st.checkbox("Show completed tasks", value=False)

day_tasks = sched.tasks_for_date(view_date)
if filter_pet != "(all)":
    day_tasks = sched.filter_tasks(day_tasks, pet_name=filter_pet)
if not show_completed:
    day_tasks = sched.filter_tasks(day_tasks, completed=False)

ordered = sched.sort_by_time(day_tasks)
conflicts = sched.detect_conflicts(sched.tasks_for_date(view_date))

if conflicts:
    for line in conflicts:
        st.warning(line)

if ordered:
    rows = []
    for t in ordered:
        rows.append(
            {
                "Time": t.time,
                "Task": t.description,
                "Pet": t.pet_name or "",
                "Priority": t.priority,
                "Frequency": t.frequency,
                "Done": t.completed,
                "Duration (min)": t.duration_minutes,
            }
        )
    st.table(rows)
else:
    st.info("No tasks for this view. Add tasks above or adjust filters.")

st.subheader("Mark complete")
if pet_names:
    complete_pet = st.selectbox("Pet (complete task)", pet_names, key="complete_pet")
    pet_obj = owner.get_pet(complete_pet)
    open_tasks = [t for t in (pet_obj.tasks if pet_obj else []) if not t.completed]
    if open_tasks:
        labels = [f"{t.time} — {t.description} ({t.task_date})" for t in open_tasks]
        choice = st.selectbox("Task to complete", range(len(open_tasks)), format_func=lambda i: labels[i])
        if st.button("Mark selected task complete"):
            target = open_tasks[choice]
            pet_obj.complete_task(target)
            st.success("Marked complete." + (" Next occurrence added for recurring task." if target.frequency in ("daily", "weekly") else ""))
            st.rerun()
    else:
        st.caption("No open tasks for this pet.")
else:
    st.caption("Add a pet first.")
