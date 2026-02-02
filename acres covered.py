import streamlit as st

st.set_page_config(page_title="Agri Drone Area Calculator", layout="centered")

st.title("🚁 Agricultural Drone Area Coverage Calculator")
st.caption("Two-efficiency model: speed loss + width loss")

st.divider()

# ----------- INPUTS -----------
col1, col2 = st.columns(2)

with col1:
    speed = st.number_input(
        "Drone speed (m/s)",
        min_value=0.5,
        max_value=15.0,
        value=5.0,
        step=0.1,
    )

    spray_width = st.number_input(
        "Spray width (m)",
        min_value=0.5,
        max_value=15.0,
        value=5.5,
        step=0.1,
    )

    flow_rate = st.number_input(
        "Flow rate (L/min)",
        min_value=0.1,
        max_value=20.0,
        value=3.0,
        step=0.01,
        format="%.3f",
    )

with col2:
    tank_capacity = st.number_input(
        "Tank capacity (L)",
        min_value=1.0,
        max_value=50.0,
        value=10.0,
        step=0.5,
    )

    turns = st.number_input(
        "Number of turns",
        min_value=0,
        max_value=200,
        value=12,
        step=1,
    )

    ks = st.number_input(
        "kₛ (speed loss constant)",
        min_value=0.0,
        max_value=0.05,
        value=0.006,
        step=0.0001,
        format="%.4f",
    )

    kw = st.number_input(
        "kᵥ (width loss constant)",
        min_value=0.0,
        max_value=0.05,
        value=0.004,
        step=0.0001,
        format="%.4f",
    )

st.divider()

# ----------- CALCULATIONS -----------

# Spray time (seconds)
t_spray = (tank_capacity / flow_rate) * 60

# Ideal area (acres)
area_ideal = (speed * spray_width * t_spray) / 4046.86

# Efficiencies
eta_speed = max(0.0, 1 - ks * (turns / speed))
eta_width = max(0.0, 1 - kw * (turns / spray_width))

# Final area
area_real = area_ideal * eta_speed * eta_width

# ----------- OUTPUTS -----------

st.subheader("📊 Results")

col3, col4 = st.columns(2)

with col3:
    st.metric("Ideal Area (acre)", f"{area_ideal:.4f}")
    st.metric("η_speed", f"{eta_speed:.4f}")

with col4:
    st.metric("Actual Area (acre)", f"{area_real:.4f}")
    st.metric("η_width", f"{eta_width:.4f}")

st.divider()

st.caption(
    "Notes:\n"
    "- η_speed captures accel/decel losses\n"
    "- η_width captures geometric / edge losses\n"
    "- kₛ and kᵥ are drone-specific constants"
)
