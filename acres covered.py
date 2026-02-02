import streamlit as st

st.set_page_config("Agri Drone Area (Turn Loss)", layout="centered")
st.title("🚁 Agri Drone Area Coverage Calculator")

# ---------- Sync helper ----------

def sync_from_num(key):
    st.session_state[f"{key}_slider"] = st.session_state[f"{key}_num"]

def sync_from_slider(key):
    st.session_state[f"{key}_num"] = st.session_state[f"{key}_slider"]

def synced_input(label, key, minv, maxv, default, step, fmt=None):
    if f"{key}_num" not in st.session_state:
        st.session_state[f"{key}_num"] = default
        st.session_state[f"{key}_slider"] = default

    c1, c2 = st.columns(2)

    with c1:
        st.number_input(
            f"{label} (Type)",
            min_value=minv,
            max_value=maxv,
            step=step,
            format=fmt,
            key=f"{key}_num",
            on_change=sync_from_num,
            args=(key,)
        )

    with c2:
        st.slider(
            f"{label} (Slide)",
            min_value=minv,
            max_value=maxv,
            step=step,
            key=f"{key}_slider",
            on_change=sync_from_slider,
            args=(key,)
        )

    return st.session_state[f"{key}_num"]

# ---------- Inputs ----------

speed = synced_input("Speed (m/s)", "speed", 0.5, 15.0, 5.0, 0.1)
width = synced_input("Spray Width (m)", "width", 1.0, 10.0, 5.5, 0.1)
flow = synced_input("Flow Rate (L/min)", "flow", 0.5, 10.0, 3.13, 0.01)
tank = synced_input("Tank Capacity (L)", "tank", 1.0, 50.0, 10.0, 0.5)

eta_turn = synced_input(
    "η_turn (per turn)", "eta", 0.90, 1.00, 0.9850, 0.0001, "%.4f"
)

turns = int(synced_input("Number of Turns", "turns", 0, 50, 12, 1))

# ---------- Calculations ----------

area_rate = speed * width
flow_rate = flow / 60

if area_rate > 0:
    lpm2 = flow_rate / area_rate
    lpa = lpm2 * 4047
    ideal_area = tank / lpa
else:
    ideal_area = 0

real_area = ideal_area * (eta_turn ** turns)

# ---------- Output ----------

st.markdown("---")
st.metric("Ideal Area (acres)", f"{ideal_area:.3f}")
st.metric("Real Area (acres)", f"{real_area:.3f}")

loss = (1 - eta_turn ** turns) * 100
st.info(f"Total turn loss: **{loss:.2f}%** over {turns} turns")
