"""
Star (Y) Connection Calculator
------------------------------
A menu-driven program for engineering students to analyse a three-phase
star-connected system.

Key relations (balanced star connection):
    Line voltage     VL = sqrt(3) * Vph
    Line current     IL = Iph
    Phase voltage    Vph = VL / sqrt(3)
    Phase current    Iph = Vph / Zph

    Apparent power   S = 3 * Vph * Iph = sqrt(3) * VL * IL     (VA)
    Active power    P = sqrt(3) * VL * IL * cos(phi)           (W)
    Reactive power  Q = sqrt(3) * VL * IL * sin(phi)           (VAR)

    Neutral current (balanced load) = 0

Unbalanced 4-wire star:
    Ia = Van / Za,  Ib = Vbn / Zb,  Ic = Vcn / Zc
    Neutral current  In = Ia + Ib + Ic   (phasor sum)

Star-delta conversion (balanced):
    Z_star = Z_delta / 3        Z_delta = 3 * Z_star
"""

import cmath
import math

SQRT3 = math.sqrt(3)


# ---------------------------------------------------------------- input helpers
def get_positive_float(prompt):
    """Keep asking until the user enters a valid positive number."""
    while True:
        try:
            value = float(input(prompt))
            if value <= 0:
                print("  Please enter a value greater than zero.")
                continue
            return value
        except ValueError:
            print("  Invalid input. Please enter a number.")


def get_float(prompt):
    """Ask for any number (zero and negative values allowed)."""
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("  Invalid input. Please enter a number.")


def get_impedance(label):
    """Ask for resistance and reactance of one phase and return complex Z.
    Reactance: positive for inductive, negative for capacitive."""
    r = get_positive_float(f"  Phase {label}: resistance R (ohm): ")
    x = get_float(f"  Phase {label}: reactance X (ohm, - for capacitive): ")
    return complex(r, x)


# ------------------------------------------------------------------ core maths
def line_voltage(v_ph):
    """VL = sqrt(3) * Vph"""
    return SQRT3 * v_ph


def phase_voltage(v_l):
    """Vph = VL / sqrt(3)"""
    return v_l / SQRT3


def balanced_powers(v_l, i_l, pf):
    """Return S, P, Q for a balanced three-phase load."""
    s = SQRT3 * v_l * i_l
    p = s * pf
    q = s * math.sqrt(max(1 - pf ** 2, 0))
    return s, p, q


def delta_to_star(z_delta):
    """Z_star = Z_delta / 3"""
    return z_delta / 3


def star_to_delta(z_star):
    """Z_delta = 3 * Z_star"""
    return 3 * z_star


# ------------------------------------------------------------------- display
def show_polar(name, value, unit):
    """Print a complex quantity in polar form."""
    mag, ang = cmath.polar(value)
    print(f"  {name} = {mag:.3f} < {math.degrees(ang):.2f} deg {unit}")


def line_from_phase():
    v_ph = get_positive_float("Phase voltage Vph (V): ")
    i_ph = get_positive_float("Phase current Iph (A): ")
    print("\n  ----- Results -----")
    print(f"  Line voltage VL = sqrt(3) x {v_ph:.2f} = {line_voltage(v_ph):.3f} V")
    print(f"  Line current IL = Iph = {i_ph:.3f} A")


def phase_from_line():
    v_l = get_positive_float("Line voltage VL (V): ")
    i_l = get_positive_float("Line current IL (A): ")
    print("\n  ----- Results -----")
    print(f"  Phase voltage Vph = {v_l:.2f} / sqrt(3) = {phase_voltage(v_l):.3f} V")
    print(f"  Phase current Iph = IL = {i_l:.3f} A")


def balanced_load():
    v_l = get_positive_float("Line voltage VL (V): ")
    r = get_positive_float("Resistance per phase R (ohm): ")
    x = get_float("Reactance per phase X (ohm, - for capacitive): ")

    z = complex(r, x)
    v_ph = phase_voltage(v_l)
    i_ph = v_ph / abs(z)
    pf = r / abs(z)
    s, p, q = balanced_powers(v_l, i_ph, pf)

    print("\n  ----- Balanced Star Load -----")
    print(f"  Phase voltage Vph       = {v_ph:.3f} V")
    print(f"  Impedance per phase Zph = {abs(z):.3f} ohm")
    print(f"  Phase current Iph = IL  = {i_ph:.4f} A")
    print(f"  Power factor            = {pf:.4f} {'lagging' if x > 0 else 'leading' if x < 0 else '(unity)'}")
    print(f"  Apparent power S        = {s:,.2f} VA")
    print(f"  Active power P          = {p:,.2f} W")
    print(f"  Reactive power Q        = {q:,.2f} VAR")
    print("  Neutral current         = 0 A (balanced load)")


def unbalanced_load():
    v_l = get_positive_float("Line voltage VL (V): ")
    v_ph = phase_voltage(v_l)
    print("\n  Enter the impedance of each phase:")
    za, zb, zc = get_impedance("A"), get_impedance("B"), get_impedance("C")

    # Phase voltages (A as reference, ABC sequence)
    van = cmath.rect(v_ph, 0)
    vbn = cmath.rect(v_ph, math.radians(-120))
    vcn = cmath.rect(v_ph, math.radians(120))

    ia, ib, ic = van / za, vbn / zb, vcn / zc
    i_n = ia + ib + ic
    total_p = (abs(ia) ** 2 * za.real) + (abs(ib) ** 2 * zb.real) + (abs(ic) ** 2 * zc.real)

    print("\n  ----- Unbalanced 4-wire Star Load -----")
    show_polar("Line current Ia", ia, "A")
    show_polar("Line current Ib", ib, "A")
    show_polar("Line current Ic", ic, "A")
    show_polar("Neutral current In", i_n, "A")
    print(f"  Total active power P = {total_p:,.2f} W")


def conversion():
    print("  1. Delta to star")
    print("  2. Star to delta")
    while True:
        pick = input("  Enter 1 or 2: ").strip()
        if pick in ("1", "2"):
            break
        print("  Please enter 1 or 2.")

    z = get_impedance("(balanced)")
    if pick == "1":
        zs = delta_to_star(z)
        print(f"\n  Z_star  = {zs.real:.3f} + j{zs.imag:.3f} ohm per phase")
    else:
        zd = star_to_delta(z)
        print(f"\n  Z_delta = {zd.real:.3f} + j{zd.imag:.3f} ohm per phase")


def menu():
    print("\n" + "=" * 52)
    print("         STAR CONNECTION CALCULATOR")
    print("=" * 52)
    print(" 1. Line values from phase values")
    print(" 2. Phase values from line values")
    print(" 3. Balanced star load (current and power)")
    print(" 4. Unbalanced 4-wire star load (neutral current)")
    print(" 5. Star-delta impedance conversion")
    print(" 0. Exit")
    print("-" * 52)


def main():
    while True:
        menu()
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            line_from_phase()
        elif choice == "2":
            phase_from_line()
        elif choice == "3":
            balanced_load()
        elif choice == "4":
            unbalanced_load()
        elif choice == "5":
            conversion()
        elif choice == "0":
            print("\nThank you for using the calculator. Goodbye!")
            break
        else:
            print("  Invalid choice. Please select from the menu.")


if __name__ == "__main__":
    main()
