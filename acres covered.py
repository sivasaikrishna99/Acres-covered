import streamlit as st

st.set_page_config(page_title="Agri Drone Area Calculator", layout="centered")
st.title("🚁 Agricultural Drone Area Coverage Calculator")
st.caption("Single-turn efficiency model (Turn loss % per turn)")

st.divider()

# Defaults
defaults = {
    "speed": 5.0,      # m/s
    "width": 5.5,      # m
    "flow": 3.0,       # kg/min
    "tank": 10.0,      # kg
    "turns": 12,       # number of turns (N)
    "turn_loss": 2.0,  # % loss per turn
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
synced_input("Swath width (m)", "width", 0.5, 15.0, 0.1)
synced_input("Flow rate (kg/min)", "flow", 0.1, 20.0, 0.001, "%.4f")
synced_input("Total Dispense weight (kg)", "tank", 1.0, 50.0, 0.5)
synced_input("Number of turns (N)", "turns", 0, 200, 1)
synced_input("Turn loss per turn (%)", "turn_loss", 0.0, 20.0, 0.1)

st.divider()

# -----------------------
# Calculations
# -----------------------
v = st.session_state.speed
w = st.session_state.width
flow = st.session_state.flow
tank = st.session_state.tank
N = st.session_state.turns
turn_loss_percent = st.session_state.turn_loss

# Spray time (seconds)
t_spray = (tank / flow) * 60

# Ideal area (acres)
A_ideal = (v * w * t_spray) / 4046.86

# Real area using % loss per turn
efficiency_per_turn = 1 - (turn_loss_percent / 100)
A_real = A_ideal * (efficiency_per_turn ** N)

# -----------------------
# Output
# -----------------------
st.subheader("📊 Results")

c1, c2 = st.columns(2)

with c2:
    st.metric("Actual Area (acre)", f"{A_real:.4f}")

st.caption(
    "Model:\n"
    "A_real = A_ideal × (1 - TurnLoss%) ^ N\n\n"
    "Turn loss (%) represents area loss per turn."
)
