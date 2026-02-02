import streamlit as st

st.set_page_config("Agri Drone Area Coverage", layout="centered")
st.title("🚁 Agri Drone Area Coverage Calculator (Turn-Time Model)")

# ----------------- Helper for synced slider + type input -----------------
def sync_from_num(key):
    st.session_state[f"{key}_slider"] = st.session_state[f"{key}_num"]

def sync_from_slider(key):
    st.session_state[f"{key}_num"] = st.session_state[f"{key}_slider"]

def synced_input(label, key, minv, maxv, default, step, fmt=None):
    if f"{key}_num" not in st.session_state:
        st.session_state[f"{key}_num"] = default
        st.session_state[f"{key}_slider"] = default

    col1, col2 = st.columns([1,1])

    with col1:
        st.number_input(
            f"{label} (Type)",
            min_value=minv,
            max_value=maxv,
            value=st.session_state[f"{key}_num"],
            step=step,
            format=fmt,
            key=f"{key}_num",
            on_change=sync_from_num,
            args=(key,)
        )

    with col2:
        st.slider(
            f"{label} (Slide)",
            min_value=minv,
            max_value=maxv,
            value=st.session_state[f"{key}_slider"],
            step=step,
            key=f"{key}_slider",
            on_change=sync_from_slider,
            args=(key,)
        )

    return st.session_state[f"{key}_num"]

# ----------------- Inputs -----------------
speed = synced_input("Drone Speed (m/s)", "speed", 0.5, 15.0, 5.0, 0.1)
width = synced_input("Spray Width (m)", "width", 1.0, 10.0, 5.5, 0.1)
flow = synced_input("Flow Rate (L/min)", "flow", 0.5, 10.0, 3.13, 0.01)
tank = synced_input("Tank Capacity (L)", "tank", 1.0, 50.0, 10.0, 0.5)

turn_duration = synced_input("Turn Duration per Turn (s)", "turn_dur", 0.5, 20.0, 3.0, 0.1)
turns = int(synced_input("Number of Turns", "turns", 0, 50, 12, 1))

# ----------------- Calculations -----------------
area_rate = speed * width                # m²/s
flow_rate = flow / 60                    # L/s

if area_rate > 0:
    app_rate = flow_rate / area_rate    # L/m²/s
    lpa = app_rate * 4047               # L/acre
    ideal_acres = tank / lpa
else:
    ideal_acres = 0

# Total spray time (s)
total_spray_time = tank / flow_rate

# Fraction of mission lost to turns
f_turn = (turn_duration * turns) / total_spray_time
f_turn = min(f_turn, 1.0)  # Cap at 100%

real_acres = ideal_acres * (1 - f_turn)

# ----------------- Output -----------------
st.markdown("---")
st.subheader("📊 Results")

st.metric("Ideal Area (acres)", f"{ideal_acres:.3f}")
st.metric("Real Area (acres)", f"{real_acres:.3f}")

st.info(f"Fraction of mission lost to turns: **{f_turn*100:.2f}%**")
st.caption("Real Acres = Ideal Acres × (1 - Fraction of Mission Lost to Turns)")

