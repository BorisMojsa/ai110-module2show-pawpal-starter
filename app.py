import streamlit as st

from pawpal_system import Owner, Pet, Scheduler, Task

DATA_PATH = "data.json"

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

with st.expander("📸 Screenshots (Project Gallery)"):
    st.caption("These are the screenshots included with the project submission.")
    st.image(
        [
            "assets/screenshot_1.png",
            "assets/screenshot_2.png",
            "assets/screenshot_3.png",
        ],
        caption=["Overview", "Mid-page controls", "Schedule area"],
        use_container_width=True,
    )

st.subheader("App Memory (Session)")

owner_name = st.text_input("Owner name", value="Jordan")
if "owner" not in st.session_state:
    st.session_state["owner"] = Owner.load_from_json(DATA_PATH)

owner: Owner = st.session_state["owner"]
owner.name = owner_name
owner.save_to_json(DATA_PATH)

st.markdown("### Add a Pet")
with st.form("add_pet_form", clear_on_submit=True):
    pet_name = st.text_input("Pet name", value="Mochi")
    species = st.selectbox("Species", ["dog", "cat", "other"])
    age = st.number_input("Age", min_value=0, max_value=50, value=2)
    submitted = st.form_submit_button("Add pet")

if submitted and pet_name.strip():
    owner.add_pet(Pet(name=pet_name.strip(), species=species, age=int(age)))
    st.success(f"Added pet: {pet_name.strip()}")
    owner.save_to_json(DATA_PATH)

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
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=1)
        task_submitted = st.form_submit_button("Add task")

    if task_submitted and description.strip() and time.strip():
        selected_pet.add_task(
            Task(
                description=description.strip(),
                time=time.strip(),
                frequency=frequency,
                priority=priority,
            )
        )
        st.success(f"Added task for {selected_pet.name}: {description.strip()}")
        owner.save_to_json(DATA_PATH)
else:
    st.info("Add a pet first to start scheduling tasks.")

if pets:
    st.write("Current tasks:")
    task_rows = []
    for p in pets:
        for t in p.get_tasks():
            status = "[x]" if t.completed else "[ ]"
            pr = t.priority.strip().lower()
            pr_icon = "🔴" if pr == "high" else "🟡" if pr == "medium" else "🟢"
            task_rows.append(
                {
                    "date": t.due_date.isoformat(),
                    "time": t.time,
                    "pet": p.name,
                    "priority": f"{pr_icon} {t.priority}",
                    "task": t.description,
                    "status": status,
                }
            )
    if task_rows:
        st.table(sorted(task_rows, key=lambda r: Scheduler._time_to_minutes(r["time"])))
    else:
        st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("Generate a daily plan using your Scheduler (sorted, filterable, with warnings).")

col_a, col_b, col_c = st.columns(3)
with col_a:
    filter_pet = st.selectbox(
        "Filter by pet",
        options=["(all)"] + [p.name for p in pets] if pets else ["(all)"],
    )
with col_b:
    show_completed = st.checkbox("Include completed", value=False)
with col_c:
    day_of_week = st.selectbox(
        "Day (for weekly tasks)",
        ["(none)", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"],
        index=0,
    )

if st.button("Generate schedule"):
    scheduler = Scheduler(owner)

    selected_pet_name = None if filter_pet == "(all)" else filter_pet
    selected_day = None if day_of_week == "(none)" else day_of_week

    plan = scheduler.generate_daily_plan(
        pet_name=selected_pet_name,
        include_completed=show_completed,
        day_of_week=selected_day,
    )

    conflicts = scheduler.detect_conflicts()
    if conflicts:
        st.warning(
            "Potential time conflicts detected. Consider moving one of the tasks to reduce stress for you and your pet."
        )
        for message in conflicts:
            st.write(f"- {message}")
        suggestion = scheduler.next_available_time("08:00")
        st.info(f"Next available slot suggestion: **{suggestion}**")

    rows = []
    for task in plan:
        pr = task.priority.strip().lower()
        pr_icon = "🔴" if pr == "high" else "🟡" if pr == "medium" else "🟢"
        rows.append(
            (
                task.due_date.isoformat(),
                task.time,
                task.priority,
                pr_icon,
                task.description,
                task.completed,
            )
        )

    rows = sorted(
        rows,
        key=lambda r: (
            {"high": 0, "medium": 1, "low": 2}.get(r[2].strip().lower(), 99),
            Scheduler._time_to_minutes(r[1]),
        ),
    )

    if not rows:
        st.info("No tasks found yet. Add a pet and at least one task.")
    else:
        st.markdown("**PawPal+ — Today's Schedule**")
        st.table(
            [
                {
                    "Date": due_date,
                    "Time": time,
                    "Priority": f"{pr_icon} {priority}",
                    "Task": description,
                    "Status": "[x]" if completed else "[ ]",
                }
                for due_date, time, priority, pr_icon, description, completed in rows
            ]
        )
