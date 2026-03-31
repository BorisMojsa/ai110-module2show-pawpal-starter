import streamlit as st

from pawpal_system import Owner, Pet, Scheduler, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("App Memory (Session)")

owner_name = st.text_input("Owner name", value="Jordan")
if "owner" not in st.session_state:
    st.session_state["owner"] = Owner(owner_name)

owner: Owner = st.session_state["owner"]
owner.name = owner_name

st.markdown("### Add a Pet")
with st.form("add_pet_form", clear_on_submit=True):
    pet_name = st.text_input("Pet name", value="Mochi")
    species = st.selectbox("Species", ["dog", "cat", "other"])
    age = st.number_input("Age", min_value=0, max_value=50, value=2)
    submitted = st.form_submit_button("Add pet")

if submitted and pet_name.strip():
    owner.add_pet(Pet(name=pet_name.strip(), species=species, age=int(age)))
    st.success(f"Added pet: {pet_name.strip()}")

pets = owner.get_pets()
if pets:
    st.write("Current pets:")
    st.table([{"name": p.name, "species": p.species, "age": p.age} for p in pets])
else:
    st.info("No pets yet. Add one above.")

st.markdown("### Add a Task")
st.caption('Task time should be in "HH:MM" format (example: 07:30).')

if pets:
    pet_names = [p.name for p in pets]
    selected_pet_name = st.selectbox("Which pet is this for?", pet_names)
    selected_pet = next(p for p in pets if p.name == selected_pet_name)

    with st.form("add_task_form", clear_on_submit=True):
        description = st.text_input("Task description", value="Morning walk")
        time = st.text_input("Time (HH:MM)", value="08:00")
        frequency = st.selectbox("Frequency", ["daily", "weekly", "once"], index=0)
        task_submitted = st.form_submit_button("Add task")

    if task_submitted and description.strip() and time.strip():
        selected_pet.add_task(
            Task(description=description.strip(), time=time.strip(), frequency=frequency)
        )
        st.success(f"Added task for {selected_pet.name}: {description.strip()}")
else:
    st.info("Add a pet first to start scheduling tasks.")

if pets:
    st.write("Current tasks:")
    task_rows = []
    for p in pets:
        for t in p.get_tasks():
            status = "[x]" if t.completed else "[ ]"
            task_rows.append(
                {"time": t.time, "pet": p.name, "task": t.description, "status": status}
            )
    if task_rows:
        st.table(sorted(task_rows, key=lambda r: r["time"]))
    else:
        st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("Generate a daily plan using your Scheduler.")

if st.button("Generate schedule"):
    scheduler = Scheduler(owner)
    plan = scheduler.generate_daily_plan()

    rows = []
    for p in owner.get_pets():
        for t in p.get_tasks():
            rows.append((t.time, p.name, t.description, t.completed))

    rows = sorted(rows, key=lambda r: r[0])

    if not rows:
        st.info("No tasks found yet. Add a pet and at least one task.")
    else:
        st.markdown("**PawPal+ — Today's Schedule**")
        st.table(
            [
                {
                    "Time": time,
                    "Pet": pet_name,
                    "Task": description,
                    "Status": "[x]" if completed else "[ ]",
                }
                for time, pet_name, description, completed in rows
            ]
        )
