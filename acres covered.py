import streamlit as st

st.set_page_config(page_title="Agri Drone Area Calculator", layout="centered")
st.title("🚁 Agricultural Drone Area Coverage Calculator")
st.caption("Single-turn efficiency model (η_turn per turn)")

st.divider()

# Defaults
defaults = {
    "speed": 5.0,      # m/s
    "width": 5.5,      # m
    "flow": 3.0,       # L/min
    "tank": 10.0,      # L
    "turns": 12,       # number of turns
    "eta_turn": 0.98, # per-turn efficiency (calibrated to ~1 acre)
}

for k, v in defaults.items():
    st.session_state.setdefault(k, v)
    st.session_state.setdefault(f"{k}_slider", v)
    st.session_state.setdefault(f"{k}_input", v)

# -----------------------
# Sync functions
# -----------------------
def slider_changed(name):
    val = st.session_state[f"{name}_slider"]
    st.session_state[name] = val
    st.session_state[f"{name}_input"] = val

def input_changed(name):
    val = st.session_state[f"{name}_input"]
    st.session_state[name] = val
    st.session_state[f"{name}_slider"] = val

# -----------------------
# Synced input widget
# -----------------------
def synced_input(label, name, minv, maxv, step, fmt=None):
    c1, c2 = st.columns([2, 1])
    with c1:
        st.slider(
            label,
            min_value=minv,
            max_value=maxv,
            step=step,
            value=st.session_state[name],
            key=f"{name}_slider",
            on_change=slider_changed,
            args=(name,)
        )
    with c2:
        st.number_input(
            " ",
            min_value=minv,
            max_value=maxv,
            step=step,
            format=fmt,
            value=st.session_state[name],
            key=f"{name}_input",
            on_change=input_changed,
            args=(name,)
        )

# -----------------------
# Inputs
# -----------------------
synced_input("Speed (m/s)", "speed", 0.5, 15.0, 0.1)
synced_input("Spray width (m)", "width", 0.5, 15.0, 0.1)
synced_input("Flow rate (L/min)", "flow", 0.1, 20.0, 0.001, "%.4f")
synced_input("Tank capacity (L)", "tank", 1.0, 50.0, 0.5)
synced_input("Number of turns", "turns", 0, 200, 1)
synced_input("η_turn (per turn)", "eta_turn", 0.95, 1.0, 0.0001, "%.4f")

st.divider()

# -----------------------
# Calculations
# -----------------------
v = st.session_state.speed
w = st.session_state.width
flow = st.session_state.flow
tank = st.session_state.tank
N = st.session_state.turns
eta_turn = st.session_state.eta_turn

# Spray time (seconds)
t_spray = (tank / flow) * 60

# Ideal area (acres)
A_ideal = (v * w * t_spray) / 4046.86

# Real area with single-turn efficiency
A_real = A_ideal * (eta_turn ** N)

# -----------------------
# Output
# -----------------------
st.subheader("📊 Results")

c1, c2 = st.columns(2)


with c2:
    st.metric("Actual Area (acre)", f"{A_real:.4f}")

st.caption(
    "Model:\n"
    "A_real = A_ideal × (η_turn ^ N)\n\n"
    "η_turn is per-turn efficiency factor capturing all turn/edge losses.\n"
    "Adjust η_turn to match practical field observations (~1 acre)."
)


