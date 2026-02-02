import streamlit as st

st.set_page_config(page_title="Agri Drone Area Calculator", layout="centered")
st.title("🚁 Agricultural Drone Area Coverage Calculator")
st.caption("Two-efficiency model: speed + width losses")

st.divider()

# ---------- STATE INITIALIZATION ----------
defaults = {
    "speed": 5.0,
    "width": 5.5,
    "flow": 3.0,
    "tank": 10.0,
    "turns": 12,
    "ks": 0.0060,
    "kw": 0.0040,
}

for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ---------- INPUT HELPERS ----------
def synced_slider_input(label, key, minv, maxv, step, fmt=None):
    col1, col2 = st.columns([2, 1])

    with col1:
        st.slider(
            label,
            min_value=minv,
            max_value=maxv,
            step=step,
            key=key,
        )

    with col2:
        st.number_input(
            " ",
            min_value=minv,
            max_value=maxv,
            step=step,
            format=fmt,
            key=key,
        )

# ---------- INPUTS ----------
synced_slider_input("Speed (m/s)", "speed", 0.5, 15.0, 0.1)
synced_slider_input("Spray width (m)", "width", 0.5, 15.0, 0.1)
synced_slider_input("Flow rate (L/min)", "flow", 0.1, 20.0, 0.01, "%.3f")
synced_slider_input("Tank capacity (L)", "tank", 1.0, 50.0, 0.5)
synced_slider_input("Number of turns", "turns", 0, 200, 1)
synced_slider_input("kₛ (speed loss constant)", "ks", 0.0, 0.05, 0.0001, "%.4f")
synced_slider_input("kᵥ (width loss constant)", "kw", 0.0, 0.05, 0.0001, "%.4f")

st.divider()

# ---------- CALCULATIONS ----------
speed = st.session_state.speed
width = st.session_state.width
flow = st.session_state.flow
tank = st.session_state.tank
turns = st.session_state.turns
ks = st.session_state.ks
kw = st.session_state.kw

# Spray time (seconds)
t_spray = (tank / flow) * 60

# Ideal area (acres)
area_ideal = (speed * width * t_spray) / 4046.86

# Efficiencies
eta_speed = max(0.0, 1 - ks * (turns / speed))
eta_width = max(0.0, 1 - kw * (turns / width))

# Actual area
area_real = area_ideal * eta_speed * eta_width

# ---------- OUTPUT ----------
st.subheader("📊 Results")

col3, col4 = st.columns(2)

with col3:
    st.metric("Ideal Area (acre)", f"{area_ideal:.4f}")
    st.metric("η_speed", f"{eta_speed:.4f}")

with col4:
    st.metric("Actual Area (acre)", f"{area_real:.4f}")
    st.metric("η_width", f"{eta_width:.4f}")

st.caption(
    "Model:\n"
    "A_real = A_ideal × η_speed × η_width\n\n"
    "η_speed = 1 − kₛ · (N / v)\n"
    "η_width = 1 − kᵥ · (N / w)"
)
