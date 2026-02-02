import streamlit as st

st.set_page_config(
    page_title="Agri Drone Area Coverage (Turn Loss Model)",
    layout="centered"
)

st.title("🚁 Agri Drone Area Coverage Calculator")
st.markdown("Slider **or** type exact values — both stay synchronized")

# ---------------- Helper function ----------------

def synced_input(label, key, min_val, max_val, default, step, fmt=None):
    col1, col2 = st.columns([1, 1])

    with col1:
        num = st.number_input(
            f"{label} (Type)",
            min_value=min_val,
            max_value=max_val,
            value=st.session_state.get(key, default),
            step=step,
            format=fmt,
            key=f"{key}_num"
        )

    with col2:
        slider = st.slider(
            f"{label} (Slide)",
            min_value=min_val,
            max_value=max_val,
            value=num,
            step=step,
            key=f"{key}_slider"
        )

    # Sync logic
    st.session_state[key] = slider

    return slider

# ---------------- Inputs ----------------

speed = synced_input(
    "Drone Speed (m/s)", "speed",
    0.5, 15.0, 5.0, 0.1
)

spray_width = synced_input(
    "Spray Width (m)", "spray_width",
    1.0, 10.0, 5.5, 0.1
)

pump_discharge = synced_input(
    "Pump Discharge (L/min)", "pump",
    0.5, 10.0, 3.33, 0.01
)

tank_capacity = synced_input(
    "Tank Capacity (L)", "tank",
    1.0, 50.0, 10.0, 0.5
)

st.markdown("---")

eta_turn = synced_input(
    "η_turn (Per-Turn Efficiency)", "eta",
    0.9000, 1.0000, 0.9868, 0.0001,
    fmt="%.4f"
)

num_turns = synced_input(
    "Number of Turns", "turns",
    0, 50, 12, 1
)

# ---------------- Calculations ----------------

area_rate = speed * spray_width          # m²/s
flow_rate = pump_discharge / 60          # L/s

if area_rate > 0:
    app_rate = flow_rate / area_rate     # L/m²
    litres_per_acre = app_rate * 4047
    ideal_acres = tank_capacity / litres_per_acre
else:
    ideal_acres = 0

turn_efficiency_total = eta_turn ** int(num_turns)
real_acres = ideal_acres * turn_efficiency_total

# ---------------- Output ----------------

st.markdown("---")
st.subheader("📊 Results")

st.metric(
    "Ideal Acres (No Turn Loss)",
    f"{ideal_acres:.3f} acres"
)

st.metric(
    "Real Acres (With Turn Loss)",
    f"{real_acres:.3f} acres"
)

loss_pct = (1 - turn_efficiency_total) * 100

st.info(
    f"Total turn loss: **{loss_pct:.2f}%** "
    f"over **{int(num_turns)} turns**"
)

st.caption("Real Acres = Ideal Acres × (η_turn)ⁿ")
