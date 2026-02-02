import streamlit as st

st.set_page_config(page_title="Agri Drone Area Calculator", layout="centered")

st.title("🚁 Agricultural Drone Area Coverage Calculator")
st.caption("Symmetric efficiency model: speed loss + width loss")

st.divider()

# =======================
# STATE INITIALIZATION
# =======================
defaults = {
    "speed": 5.0,     # m/s
    "width": 5.5,     # m
    "flow": 3.0,      # L/min
    "tank": 10.0,     # L
    "turns": 12,      # count
    "ks": 0.0060,     # speed-loss constant
    "kw": 0.0040,     # width-loss constant
}

for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# =======================
# SYNC CALLBACKS
# =======================
def sync_from_slider(name):
    st.session_state[name] = st.session_state[f"{name}_slider"]

def sync_from_input(name):
    st.session_state[name] = st.session_state[f"{name}_input"]

# =======================
# SYNCED INPUT WIDGET
# =======================
def synced_input(label, name, minv, maxv, step, fmt=None):
    col1, col2 = st.columns([2, 1])

    with col1:
        st.slider(
            label,
            min_value=minv,
            max_value=maxv,
            step=step,
            value=st.session_state[name],
            key=f"{name}_slider",
            on_change=sync_from_slider,
            args=(name,),
        )

    with col2:
        st.number_input(
            " ",
            min_value=minv,
            max_value=maxv,
            step=step,
            value=st.session_state[name],
            format=fmt,
            key=f"{name}_input",
            on_change=sync_from_input,
            args=(name,),
        )

# =======================
# INPUTS
# =======================
synced_input("Speed (m/s)", "speed", 0.5, 15.0, 0.1)
synced_input("Spray width (m)", "width", 0.5, 15.0, 0.1)
synced_input("Flow rate (L/min)", "flow", 0.1, 20.0, 0.01, "%.3f")
synced_input("Tank capacity (L)", "tank", 1.0, 50.0, 0.5)
synced_input("Number of turns", "turns", 0, 200, 1)

synced_input("kₛ – speed loss constant", "ks", 0.0, 0.05, 0.0001, "%.4f")
synced_input("kᵥ – width loss constant", "kw", 0.0, 0.05, 0.0001, "%.4f")

st.divider()

# =======================
# CALCULATIONS
# =======================
v = st.session_state.speed
w = st.session_state.width
flow = st.session_state.flow
tank = st.session_state.tank
N = st.session_state.turns
ks = st.session_state.ks
kw = st.session_state.kw

# Spray time (seconds)
t_spray = (tank / flow) * 60.0

# Ideal area (acres)
A_ideal = (v * w * t_spray) / 4046.86

# Efficiencies
eta_speed = max(0.0, 1.0 - ks * (N / v))
eta_width = max(0.0, 1.0 - kw * (N / w))

# Actual area
A_real = A_ideal * eta_speed * eta_width

# =======================
# OUTPUT
# =======================
st.subheader("📊 Results")

col3, col4 = st.columns(2)

with col3:
    st.metric("Ideal Area (acre)", f"{A_ideal:.4f}")
    st.metric("η_speed", f"{eta_speed:.4f}")

with col4:
    st.metric("Actual Area (acre)", f"{A_real:.4f}")
    st.metric("η_width", f"{eta_width:.4f}")

st.divider()

st.caption(
    "Model used:\n\n"
    "A_real = A_ideal × η_speed × η_width\n\n"
    "η_speed = 1 − kₛ · (N / v)\n"
    "η_width = 1 − kᵥ · (N / w)\n\n"
    "Assumptions:\n"
    "• Constant flow rate\n"
    "• Continuous spraying\n"
    "• Losses captured via ks & kw\n"
)
