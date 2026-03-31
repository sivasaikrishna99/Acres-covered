import streamlit as st

st.set_page_config(page_title="Agri Drone Flow Calculator", layout="centered")
st.title("🚁 Spray Flow Rate Calculator")
st.caption("Mixed units supported • Output always in L/min")

st.divider()

# -----------------------
# Defaults
# -----------------------
defaults = {
    "liquid": 10.0,
    "area": 1.0,
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
# Safe synced input
# -----------------------
def synced_input(label, name, minv, maxv, step):
    # Clamp value to avoid Streamlit crash
    val = st.session_state.get(name, minv)

    if val < minv:
        val = minv
    elif val > maxv:
        val = maxv

    st.session_state[name] = val
    st.session_state[f"{name}_slider"] = val
    st.session_state[f"{name}_input"] = val

    c1, c2 = st.columns([2, 1])

    with c1:
        st.slider(
            label,
            min_value=minv,
            max_value=maxv,
            step=step,
            value=val,
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
            value=val,
            key=f"{name}_input",
            on_change=input_changed,
            args=(name,)
        )

# -----------------------
# Inputs + Units
# -----------------------

# Liquid
c1, c2 = st.columns([3, 1])
with c1:
    synced_input("Total Liquid", "liquid", 0.1, 200.0, 0.1)
with c2:
    liquid_unit = st.selectbox("Unit", ["L", "Gallon"])

# Area
c1, c2 = st.columns([3, 1])
with c1:
    synced_input("Area", "area", 0.1, 50.0, 0.1)
with c2:
    area_unit = st.selectbox(" ", ["Acre", "Hectare"])

# Speed
c1, c2 = st.columns([3, 1])
with c1:
    synced_input("Flight Speed", "speed", 0.5, 30.0, 0.1)
with c2:
    speed_unit = st.selectbox("  ", ["m/s", "km/h", "ft/s"])

# Spacing
c1, c2 = st.columns([3, 1])
with c1:
    synced_input("Line Spacing", "spacing", 0.5, 20.0, 0.1)
with c2:
    spacing_unit = st.selectbox("   ", ["m", "ft"])

# Height
c1, c2 = st.columns([3, 1])
with c1:
    synced_input("Height", "height", 0.5, 20.0, 0.1)
with c2:
    height_unit = st.selectbox("    ", ["m", "ft"])

st.divider()

# -----------------------
# Unit Conversions (to SI)
# -----------------------

# Liquid → Litres
liquid = st.session_state.liquid
if liquid_unit == "Gallon":
    liquid *= 3.78541  # US gallon

# Area → m²
area = st.session_state.area
if area_unit == "Acre":
    area_m2 = area * 4046.86
else:
    area_m2 = area * 10000

# Speed → m/s
speed = st.session_state.speed
if speed_unit == "km/h":
    speed /= 3.6
elif speed_unit == "ft/s":
    speed *= 0.3048

# Spacing → m
spacing = st.session_state.spacing
if spacing_unit == "ft":
    spacing *= 0.3048

# Height → m (not used yet)
height = st.session_state.height
if height_unit == "ft":
    height *= 0.3048

# -----------------------
# Calculations
# -----------------------

if area_m2 > 0:
    app_rate = liquid / (area_m2 / 4046.86)  # L/acre
else:
    app_rate = 0

flow_rate = (app_rate * speed * spacing * 60) / 4046.86

# -----------------------
# Output
# -----------------------
st.subheader("📊 Results")

c1, c2 = st.columns(2)

with c1:
    st.metric("Flow Rate (L/min)", f"{flow_rate:.4f}")

st.caption(
    "All inputs converted internally to SI units.\n"
    "Flow = (Application Rate × Speed × Spacing × 60) / 4046.86\n"
    "Output always in L/min."
)
