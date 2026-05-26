import re
import tkinter as tk
from tkinter import ttk


class OPCalcGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("GB Overprime Calculator")
        self.geometry("900x450")

        # Variables
        self.correct_string_var = tk.StringVar()
        self.discount_string_var = tk.StringVar()
        self.owner_var = tk.StringVar(value="31860")
        self.overprime_var = tk.StringVar(value="33810")
        self.difference_var = tk.StringVar(value="0")

        # Row 7 (Original Values)
        self.orig_vars = {
            "P5": tk.StringVar(value="0"),
            "P4": tk.StringVar(value="0"),
            "P3": tk.StringVar(value="0"),
            "P2": tk.StringVar(value="0"),
            "P1": tk.StringVar(value="0"),
        }

        # Row 8 (Discount Values)
        self.disc_vars = {
            "P5": tk.StringVar(value="0"),
            "P4": tk.StringVar(value="0"),
            "P3": tk.StringVar(value="0"),
            "P2": tk.StringVar(value="0"),
            "P1": tk.StringVar(value="0"),
        }

        # Row 9 (Profit/Reduction)
        self.profit_vars = {
            "P5": tk.StringVar(value="0"),
            "P4": tk.StringVar(value="0"),
            "P3": tk.StringVar(value="0"),
            "P2": tk.StringVar(value="0"),
            "P1": tk.StringVar(value="0"),
        }

        self.create_widgets()
        self.setup_bindings()

        # Initial calculation
        self.correct_string_var.set(
            "Pawly 🐊 Arc 162 → 163 P5(48) P4(257) P3(1026) P2(3078) P1(6147)"
        )
        self.parse_and_calculate()

    def create_widgets(self):
        # Main container
        main_frame = ttk.Frame(self, padding="15")
        main_frame.grid(row=0, column=0, sticky="nsew")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # Row 1: Header
        header_lbl = ttk.Label(
            main_frame, text="GB Overprime Calculator", font=("Arial", 16, "bold")
        )
        header_lbl.grid(row=0, column=0, columnspan=8, sticky="w", pady=(0, 5))

        # Row 2: Sub-header
        sub_lbl = ttk.Label(
            main_frame,
            text="Calculate discount values, update discount string and paste it into the FOE 1.9 thread",
            font=("Arial", 10, "italic"),
        )
        sub_lbl.grid(row=1, column=0, columnspan=8, sticky="w", pady=(0, 15))

        # Row 3: Correct String
        ttk.Label(main_frame, text="Correct String", font=("Arial", 10, "bold")).grid(
            row=2, column=0, sticky="w", pady=5, padx=(0, 10)
        )
        self.entry_correct = ttk.Entry(
            main_frame, textvariable=self.correct_string_var, width=80
        )
        self.entry_correct.grid(row=2, column=1, columnspan=7, sticky="we", pady=5)

        # Row 4: Discount String
        ttk.Label(main_frame, text="Discount String", font=("Arial", 10, "bold")).grid(
            row=3, column=0, sticky="w", pady=5, padx=(0, 10)
        )
        self.entry_discount = ttk.Entry(
            main_frame,
            textvariable=self.discount_string_var,
            width=80,
            state="readonly",
        )
        self.entry_discount.grid(row=3, column=1, columnspan=7, sticky="we", pady=5)

        # Row 5: Target Info
        ttk.Label(main_frame, text="Target Info", font=("Arial", 10, "bold")).grid(
            row=4, column=0, sticky="w", pady=15
        )

        ttk.Label(main_frame, text="Owner").grid(row=4, column=1, sticky="e", padx=5)
        self.entry_owner = ttk.Entry(
            main_frame, textvariable=self.owner_var, width=10
        )
        self.entry_owner.grid(row=4, column=2, sticky="w", padx=5)

        ttk.Label(main_frame, text="Overprime").grid(
            row=4, column=3, sticky="e", padx=5
        )
        self.entry_overprime = ttk.Entry(
            main_frame, textvariable=self.overprime_var, width=10
        )
        self.entry_overprime.grid(row=4, column=4, sticky="w", padx=5)

        ttk.Label(main_frame, text="Difference").grid(
            row=4, column=5, sticky="e", padx=5
        )
        lbl_diff = ttk.Label(
            main_frame,
            textvariable=self.difference_var,
            font=("Arial", 10, "bold"),
            foreground="red",
        )
        lbl_diff.grid(row=4, column=6, sticky="w", padx=5)

        # Row 6: Labels for Reward Spots
        spots = ["P5", "P4", "P3", "P2", "P1"]
        for idx, spot in enumerate(spots):
            ttk.Label(
                main_frame, text=spot, font=("Arial", 10, "bold"), anchor="center"
            ).grid(row=5, column=idx + 1, pady=(15, 5), sticky="we")

        # Row 7: Original Values
        ttk.Label(main_frame, text="Original Values").grid(
            row=6, column=0, sticky="w", pady=5
        )
        for idx, spot in enumerate(spots):
            ttk.Label(
                main_frame,
                textvariable=self.orig_vars[spot],
                anchor="center",
                relief="sunken",
                width=10,
            ).grid(row=6, column=idx + 1, pady=5, padx=2)

        # Row 8: Discount Values
        ttk.Label(main_frame, text="Discount Values").grid(
            row=7, column=0, sticky="w", pady=5
        )
        for idx, spot in enumerate(spots):
            ttk.Label(
                main_frame,
                textvariable=self.disc_vars[spot],
                anchor="center",
                relief="sunken",
                width=10,
            ).grid(row=7, column=idx + 1, pady=5, padx=2)

        # Row 9: Profit/Reduction
        ttk.Label(main_frame, text="Profit/Reduction").grid(
            row=8, column=0, sticky="w", pady=5
        )
        for idx, spot in enumerate(spots):
            ttk.Label(
                main_frame,
                textvariable=self.profit_vars[spot],
                anchor="center",
                relief="sunken",
                width=10,
            ).grid(row=8, column=idx + 1, pady=5, padx=2)

        # Reset Button
        btn_reset = ttk.Button(main_frame, text="Reset (Ctrl+r)", command=self.reset)
        btn_reset.grid(row=9, column=1, columnspan=2, pady=20, sticky="w")

    def setup_bindings(self):
        self.correct_string_var.trace_add("write", lambda *args: self.parse_and_calculate())
        self.owner_var.trace_add("write", lambda *args: self.parse_and_calculate())
        self.overprime_var.trace_add("write", lambda *args: self.parse_and_calculate())
        self.bind("<Control-r>", lambda event: self.reset())
        self.bind("<Control-R>", lambda event: self.reset())

    def parse_and_calculate(self):
        input_str = self.correct_string_var.get()

        # Extract original values using regex
        spots = ["P5", "P4", "P3", "P2", "P1"]
        extracted_vals = {}
        for spot in spots:
            match = re.search(rf"{spot}\((\d+)\)", input_str)
            if match:
                extracted_vals[spot] = int(match.group(1))
            else:
                extracted_vals[spot] = 0

        # Update Row 7 UI
        for spot in spots:
            self.orig_vars[spot].set(str(extracted_vals[spot]))

        # Calculate Difference
        try:
            owner_val = int(self.owner_var.get()) if self.owner_var.get() else 0
            overprime_val = int(self.overprime_var.get()) if self.overprime_var.get() else 0
        except ValueError:
            owner_val = 0
            overprime_val = 0

        difference = overprime_val - owner_val
        self.difference_var.set(str(difference))

        # Calculate distribution
        total_spots = sum(extracted_vals.values())

        profits = {spot: 0 for spot in spots}
        discounts = {spot: extracted_vals[spot] for spot in spots}

        if total_spots > 0 and difference > 0:
            # Distribute difference proportionally
            allocated_profit = 0
            for spot in spots:
                orig_val = extracted_vals[spot]
                profit = round(difference * (orig_val / total_spots))
                profits[spot] = profit
                allocated_profit += profit

            # Handle rounding discrepancies by adjusting the largest spot (P1)
            discrepancy = difference - allocated_profit
            if discrepancy != 0:
                profits["P1"] += discrepancy

            # Calculate discount values
            for spot in spots:
                discounts[spot] = max(0, extracted_vals[spot] - profits[spot])

        # Update Row 8 and Row 9 UI
        for spot in spots:
            self.profit_vars[spot].set(str(profits[spot]))
            self.disc_vars[spot].set(str(discounts[spot]))

        # Generate Output String
        output_str = input_str
        for spot in spots:
            output_str = re.sub(
                rf"{spot}\(\d+\)", f"{spot}({discounts[spot]})", output_str
            )

        self.discount_string_var.set(output_str)

    def reset(self):
        self.correct_string_var.set("")
        self.discount_string_var.set("")
        self.owner_var.set("")
        self.overprime_var.set("")
        self.difference_var.set("0")
        for spot in ["P5", "P4", "P3", "P2", "P1"]:
            self.orig_vars[spot].set("0")
            self.disc_vars[spot].set("0")
            self.profit_vars[spot].set("0")


if __name__ == "__main__":
    app = OPCalcGUI()
    app.mainloop()
