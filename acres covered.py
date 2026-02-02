import streamlit as st
import math

st.set_page_config(
    page_title="Agri Drone Area Coverage (Turn Loss Model)",
    layout="centered"
)

st.title("🚁 Agri Drone Area Coverage Calculator")
st.markdown("Includes **per-turn efficiency loss**")

# ---------------- Inputs ----------------

speed = st.slider(
    "Drone Speed (m/s)",
    min_value=0.5,
    max_value=15.0,
    value=5.0,
    step=0.1
)

spray_width = st.slider(
    "Spray Width (m)",
    min_value=1.0,
    max_value=10.0,
    value=5.5,
    step=0.1
)

pump_discharge = st.slider(
    "Pump Discharge (L/min)",
    min_value=0.5,
    max_value=10.0,
    value=3.13,
    step=0.01
)

tank_capacity = st.slider(
    "Tank Capacity (L)",
    min_value=1.0,
    max_value=50.0,
    value=10.0,
    step=0.5
)

st.markdown("---")

eta_turn = st.slider(
    "η_turn (Per Turn Efficiency)",
    min_value=0.90,
    max_value=1.00,
    value=0.9835,
    step=0.0005,
    help="Efficiency retained per turn (e.g. 0.9835 = 1.65% loss per turn)"
)

num_turns = st.slider(
    "Number of Turns",
    min_value=0,
    max_value=50,
    value=12,
    step=1
)

# ---------------- Calculations ----------------

area_rate_m2_per_s = speed * spray_width
flow_rate_l_per_s = pump_discharge / 60

if area_rate_m2_per_s > 0:
    application_rate_l_per_m2 = flow_rate_l_per_s / area_rate_m2_per_s
    litres_per_acre = application_rate_l_per_m2 * 4047
    ideal_acres = tank_capacity / litres_per_acre
else:
    ideal_acres = 0

turn_efficiency_total = eta_turn ** num_turns
real_acres = ideal_acres * turn_efficiency_total

# ---------------- Output ----------------

st.markdown("---")
st.subheader("📊 Results")

st.metric(
    "Ideal Acres (No Turn Loss)",
    f"{ideal_acres:.2f} acres"
)

st.metric(
    "Real Acres (With Turn Loss)",
    f"{real_acres:.2f} acres"
)

st.caption("Formula: Real Acres = Ideal Acres × (η_turn)ⁿ")

# ---------------- Insights ----------------

loss_percent = (1 - turn_efficiency_total) * 100

st.info(
    f"Total turn-related loss: **{loss_percent:.1f}%** "
    f"over **{num_turns} turns**"
)
