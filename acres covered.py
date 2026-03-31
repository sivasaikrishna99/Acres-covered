import streamlit as st

st.set_page_config(page_title="Agri Drone Flow Rate Calculator", layout="centered")
st.title("🚁 Spray Flow Rate Calculator")
st.caption("Calculate required flow rate from field inputs")

st.divider()

# -----------------------
# Defaults
# -----------------------
defaults = {
    "litres": 10.0,
    "acres": 1.0,
    "speed": 5.0,
    "spacing": 5.5,
    "height": 2.0,
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
synced_input("Total Liquid (L)", "litres", 0.1, 100.0, 0.1)
synced_input("Area to Cover (acre)", "acres", 0.1, 20.0, 0.1)
synced_input("Flight speed (m/s)", "speed", 0.5, 15.0, 0.1)
synced_input("Line spacing (m)", "spacing", 0.5, 15.0, 0.1)
synced_input("Height (m)", "height", 0.5, 10.0, 0.1)

st.divider()

# -----------------------
# Calculations
# -----------------------
litres = st.session_state.litres
acres = st.session_state.acres
v = st.session_state.speed
S = st.session_state.spacing

# Avoid division error
if acres > 0:
    app_rate = litres / acres  # L/acre
else:
    app_rate = 0

# Flow rate (L/min ≈ kg/min)
flow_rate = (app_rate * v * S * 60) / 4046.86

# -----------------------
# Output
# -----------------------
st.subheader("📊 Results")

c1, c2 = st.columns(2)

with c1:
    st.metric("Application Rate (L/acre)", f"{app_rate:.2f}")

with c2:
    st.metric("Required Flow Rate (kg/min)", f"{flow_rate:.4f}")

st.caption(
    "Formula:\n"
    "Application Rate = Litres / Acres\n"
    "Flow = (Application Rate × Speed × Line Spacing × 60) / 4046.86\n\n"
    "Assuming 1 L ≈ 1 kg"
)
