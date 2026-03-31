import streamlit as st

st.set_page_config(page_title="Agri Drone Flow Rate Calculator", layout="centered")
st.title("🚁 Spray Flow Rate Calculator")
st.caption("Based on application rate, speed, and spacing")

st.divider()

# Defaults
defaults = {
    "app_rate": 5.0,   # L/acre
    "speed": 5.0,      # m/s
    "spacing": 5.5,    # m
    "height": 2.0,     # m (not used in formula yet)
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
synced_input("Application rate (L/acre)", "app_rate", 0.1, 50.0, 0.1)
synced_input("Flight speed (m/s)", "speed", 0.5, 15.0, 0.1)
synced_input("Line spacing (m)", "spacing", 0.5, 15.0, 0.1)
synced_input("Height (m)", "height", 0.5, 10.0, 0.1)

st.divider()

# -----------------------
# Calculation
# -----------------------
R = st.session_state.app_rate
v = st.session_state.speed
S = st.session_state.spacing

# Flow rate (L/min ≈ kg/min)
flow_rate = (R * v * S * 60) / 4046.86

# -----------------------
# Output
# -----------------------
st.subheader("📊 Result")

st.metric("Required Flow Rate (kg/min)", f"{flow_rate:.4f}")

st.caption(
    "Formula:\n"
    "Flow = (Application Rate × Speed × Line Spacing × 60) / 4046.86\n\n"
    "Assuming 1 L ≈ 1 kg"
)
