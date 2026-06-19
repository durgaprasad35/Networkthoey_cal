import streamlit as st
import math

st.set_page_config(
    page_title="Circuit Calculator",
    page_icon="⚡",
    layout="wide"
)

st.title("⚡ Circuit Calculator")
st.markdown("Arduino Circuit Calculator converted to Streamlit")

# ---------------- BASIC FUNCTIONS ----------------

def series(a, b):
    return a + b


def parallel(a, b):
    if (a + b) == 0:
        return 0
    return (a * b) / (a + b)


# ---------------- EQUIVALENT RESISTANCE ----------------

def equivalent_resistance():
    st.header("Equivalent Resistance")

    if "eq_res" not in st.session_state:
        st.session_state.eq_res = None

    if st.session_state.eq_res is None:
        r1 = st.number_input(
            "Enter R1",
            min_value=0.0,
            value=0.0,
            key="r1_eq"
        )

        if st.button("Start Calculation"):
            st.session_state.eq_res = r1
            st.rerun()

    else:
        st.success(
            f"Current Equivalent Resistance = "
            f"{st.session_state.eq_res:.2f} Ω"
        )

        choice = st.radio(
            "Connection Type",
            ["Series", "Parallel"]
        )

        r = st.number_input(
            "Enter next Resistance",
            min_value=0.0,
            value=0.0,
            key="next_r"
        )

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Add Resistor"):
                if choice == "Series":
                    st.session_state.eq_res = series(
                        st.session_state.eq_res,
                        r
                    )
                else:
                    st.session_state.eq_res = parallel(
                        st.session_state.eq_res,
                        r
                    )

                st.rerun()

        with col2:
            if st.button("Finish"):
                st.info(
                    f"Final Equivalent Resistance = "
                    f"{st.session_state.eq_res:.2f} Ω"
                )

    return st.session_state.eq_res


# ---------------- THEVENIN ----------------

def thevenin_theorem():
    st.header("Thevenin Theorem")

    rth = st.number_input(
        "Equivalent Resistance (Rth)",
        min_value=0.0
    )

    vth = st.number_input(
        "Enter Vth",
        value=0.0
    )

    rl = st.number_input(
        "Enter RL",
        min_value=0.0,
        value=0.0
    )

    if st.button("Calculate IL"):
        il = vth / (rth + rl)
        st.success(f"Load Current (IL) = {il:.2f} A")


# ---------------- NORTON ----------------

def norton_theorem():
    st.header("Norton Theorem")

    rn = st.number_input(
        "Equivalent Resistance (Rn)",
        min_value=0.0
    )

    vth = st.number_input(
        "Enter Vth",
        value=0.0,
        key="nvth"
    )

    rl = st.number_input(
        "Enter RL",
        min_value=0.0,
        value=0.0,
        key="nrl"
    )

    if st.button("Calculate Norton"):
        if rn == 0:
            st.error("Rn cannot be zero.")
            return

        inn = vth / rn
        il = inn * (rn / (rn + rl))

        st.success(f"Load Current (IL) = {il:.2f} A")


# ---------------- MAX POWER ----------------

def max_power_theorem():
    st.header("Maximum Power Transfer Theorem")

    voltage = st.number_input(
        "Enter Voltage",
        value=0.0
    )

    r1 = st.number_input(
        "Enter R1",
        value=0.0
    )

    r2 = st.number_input(
        "Enter R2",
        value=0.0
    )

    rth = st.number_input(
        "Enter Equivalent Resistance (Rth)",
        value=0.0
    )

    rl = st.number_input(
        "Enter RL",
        value=0.0
    )

    if st.button("Calculate Maximum Power"):
        if (r1 + r2) == 0:
            vth = 0
        else:
            vth = voltage * (r2 / (r1 + r2))

        il = vth / (rth + rl)

        st.success(f"Load Current (IL) = {il:.2f} A")

        if abs(rth - rl) < 0.01:
            st.success("Maximum Power Condition Verified")
        else:
            st.warning("Not Maximum Power Condition")


# ---------------- SUPERPOSITION ----------------

def superposition_theorem():
    st.header("Superposition Theorem")

    n = st.number_input(
        "Number of Sources",
        min_value=1,
        step=1
    )

    r_count = st.number_input(
        "Number of Resistors",
        min_value=1,
        step=1
    )

    total_resistance = 0

    st.subheader("Resistors")

    for i in range(int(r_count)):
        r = st.number_input(
            f"R{i+1}",
            value=0.0,
            key=f"res{i}"
        )
        total_resistance += r

    total_current = 0

    st.subheader("Sources")

    currents = []

    for i in range(int(n)):
        v = st.number_input(
            f"V{i+1}",
            value=0.0,
            key=f"v{i}"
        )

        if total_resistance == 0:
            current = 0
        else:
            current = v / total_resistance

        currents.append(current)
        total_current += current

    if st.button("Calculate Superposition"):
        for i, current in enumerate(currents):
            st.info(
                f"I{i+1} = {current:.2f} A"
            )

        st.success(
            f"Total Current = "
            f"{total_current:.2f} A"
        )


# ---------------- KCL ----------------

def kcl_law():
    st.header("Kirchhoff's Current Law (KCL)")

    n = st.number_input(
        "Number of Currents",
        min_value=1,
        step=1
    )

    total = 0

    for i in range(int(n)):
        current = st.number_input(
            f"I{i+1}",
            value=0.0,
            key=f"kcl{i}"
        )
        total += current

    if st.button("Calculate KCL"):
        st.success(
            f"Sum of Currents = "
            f"{total:.2f}"
        )


# ---------------- KVL ----------------

def kvl_law():
    st.header("Kirchhoff's Voltage Law (KVL)")

    n = st.number_input(
        "Number of Voltages",
        min_value=1,
        step=1
    )

    total = 0

    for i in range(int(n)):
        voltage = st.number_input(
            f"V{i+1}",
            value=0.0,
            key=f"kvl{i}"
        )
        total += voltage

    if st.button("Calculate KVL"):
        if abs(total) < 0.01:
            st.success(
                f"KVL Verified\n\n"
                f"Sum = {total:.2f}"
            )
        else:
            st.warning(
                f"Not Verified\n\n"
                f"Sum = {total:.2f}"
            )


# ---------------- INDUCTOR ----------------

def inductor_equivalent():
    st.header("Equivalent Inductance")

    l1 = st.number_input(
        "Enter L1",
        value=0.0
    )

    n = st.number_input(
        "Number of Additional Inductors",
        min_value=0,
        step=1
    )

    eq = l1

    for i in range(int(n)):
        choice = st.selectbox(
            f"Connection Type {i+1}",
            ["Series", "Parallel"],
            key=f"ind{i}"
        )

        l = st.number_input(
            f"L{i+2}",
            value=0.0,
            key=f"l{i}"
        )

        if choice == "Series":
            eq = eq + l
        else:
            if (eq + l) == 0:
                eq = 0
            else:
                eq = (eq * l) / (eq + l)

    if st.button("Calculate Inductance"):
        st.success(
            f"Equivalent Inductance = "
            f"{eq:.2f} H"
        )


# ---------------- CAPACITOR ----------------

def capacitor_equivalent():
    st.header("Equivalent Capacitance")

    c1 = st.number_input(
        "Enter C1",
        value=0.0
    )

    n = st.number_input(
        "Number of Additional Capacitors",
        min_value=0,
        step=1
    )

    eq = c1

    for i in range(int(n)):
        choice = st.selectbox(
            f"Connection Type {i+1}",
            ["Series", "Parallel"],
            key=f"cap{i}"
        )

        c = st.number_input(
            f"C{i+2}",
            value=0.0,
            key=f"c{i}"
        )

        if choice == "Series":
            if (eq + c) == 0:
                eq = 0
            else:
                eq = (eq * c) / (eq + c)
        else:
            eq = eq + c

    if st.button("Calculate Capacitance"):
        st.success(
            f"Equivalent Capacitance = "
            f"{eq:.2f} F"
        )


# ---------------- AC ANALYSIS ----------------

def inductive_reactance():
    st.header("Inductive Reactance")

    frequency = st.number_input(
        "Frequency",
        value=0.0
    )

    inductance = st.number_input(
        "Inductance",
        value=0.0
    )

    if st.button("Calculate XL"):
        xl = 2 * 3.1416 * frequency * inductance
        st.success(f"XL = {xl:.2f} Ω")


def capacitive_reactance():
    st.header("Capacitive Reactance")

    frequency = st.number_input(
        "Frequency",
        value=0.0
    )

    capacitance = st.number_input(
        "Capacitance",
        value=0.0
    )

    if st.button("Calculate XC"):
        if frequency == 0 or capacitance == 0:
            st.error("Frequency and Capacitance cannot be zero.")
            return

        xc = 1 / (
            2 * 3.1416 * frequency * capacitance
        )

        st.success(f"XC = {xc:.2f} Ω")


def impedance_calc():
    st.header("Impedance")

    r = st.number_input(
        "R",
        value=0.0
    )

    xl = st.number_input(
        "XL",
        value=0.0
    )

    xc = st.number_input(
        "XC",
        value=0.0
    )

    if st.button("Calculate Impedance"):
        z = math.sqrt(
            r * r +
            (xl - xc) * (xl - xc)
        )

        st.success(f"Z = {z:.2f} Ω")


def resonance_calc():
    st.header("Resonance Frequency")

    l = st.number_input(
        "L",
        value=0.0
    )

    c = st.number_input(
        "C",
        value=0.0
    )

    if st.button("Calculate Resonance"):
        if l == 0 or c == 0:
            st.error("L and C cannot be zero.")
            return

        f0 = 1 / (
            2 * 3.1416 *
            math.sqrt(l * c)
        )

        st.success(
            f"Resonance Frequency = "
            f"{f0:.2f} Hz"
        )


# ---------------- SIDEBAR MENU ----------------

menu = st.sidebar.radio(
    "Main Menu",
    [
        "Equivalent Resistance",
        "Thevenin",
        "Norton",
        "Maximum Power",
        "Superposition",
        "KCL",
        "KVL",
        "Inductor Equivalent",
        "Capacitor Equivalent",
        "Inductive Reactance",
        "Capacitive Reactance",
        "Impedance",
        "Resonance"
    ]
)

if menu == "Equivalent Resistance":
    equivalent_resistance()

elif menu == "Thevenin":
    thevenin_theorem()

elif menu == "Norton":
    norton_theorem()

elif menu == "Maximum Power":
    max_power_theorem()

elif menu == "Superposition":
    superposition_theorem()

elif menu == "KCL":
    kcl_law()

elif menu == "KVL":
    kvl_law()

elif menu == "Inductor Equivalent":
    inductor_equivalent()

elif menu == "Capacitor Equivalent":
    capacitor_equivalent()

elif menu == "Inductive Reactance":
    inductive_reactance()

elif menu == "Capacitive Reactance":
    capacitive_reactance()

elif menu == "Impedance":
    impedance_calc()

elif menu == "Resonance":
    resonance_calc()