"""
main.py

User entry point for the Planck program.
Example parameters are provided and may be overwritten by the user.

This module calls the numerical driver and prints the result.
"""

from planck_driver import run_planck


def main():
    # --------------------------------------------------------------
    # Example parameters (user may overwrite)
    # --------------------------------------------------------------
    n_steps = 20000          # accuracy parameter
    output_type = "maximum"  # "maximum" or "area"

    # --------------------------------------------------------------
    # Run the Planck computation
    # --------------------------------------------------------------
    result = run_planck(n_steps, output_type)

    # --------------------------------------------------------------
    # Display results
    # --------------------------------------------------------------
    if output_type == "maximum":
        print("Location of maximum of Planck function:")
        print(f"x_peak = {result['x_peak']}")
        print(f"y_peak = {result['y_peak']}")
    else:
        print("Area under the Planck curve:")
        print(f"area = {result['area']}")


if __name__ == "__main__":
    main()
