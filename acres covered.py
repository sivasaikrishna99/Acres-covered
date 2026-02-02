import streamlit as st

st.set_page_config(page_title="Agri Drone Area Calculator", layout="centered")

st.title("🚁 Agricultural Drone Area Coverage Calculator")

st.markdown("Adjust the parameters below (you can **slide or type values**)")

# ---- Inputs ----
speed = st.slider(
    "Drone Speed (m/s)",
    min_value=0.5,
    max_value=15.0,
    value=5.0,
    step=0.1
)

spray_width = st.slider(
    "Spray Width (meters)",
    min_value=1.0,
    max_value=10.0,
    value=4.0,
    step=0.1
)

pump_discharge = st.slider(
    "Pump Discharge (litres/min)",
    min_value=0.5,
    max_value=10.0,
    value=2.0,
    step=0.1
)

tank_capacity = st.slider(
    "Tank Capacity (litres)",
    min_value=1.0,
    max_value=50.0,
    value=10.0,
    step=0.5
)

# ---- Calculations ----
area_rate_m2_per_s = speed * spray_width
flow_rate_l_per_s = pump_discharge / 60

if area_rate_m2_per_s > 0:
    application_rate_l_per_m2 = flow_rate_l_per_s / area_rate_m2_per_s
    litres_per_acre = application_rate_l_per_m2 * 4047
    acres_covered = tank_capacity / litres_per_acre
else:
    acres_covered = 0

# ---- Output ----
st.markdown("---")
st.subheader("📊 Results")

st.metric(
    label="Acres Covered per Tank",
    value=f"{acres_covered:.2f} acres"
)

st.caption("4047 m² = 1 acre")