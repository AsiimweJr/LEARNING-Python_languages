"""
Graphical blood donor registry with search and a blood-group count chart.

Records are kept in memory and are cleared when the app closes.
"""

from pathlib import Path
import tkinter as tk
from tkinter import messagebox, ttk

from PIL import Image
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

if __package__:
    from .blood_donor_logic import (
        BLOOD_GROUPS,
        add_donor as add_donor_record,
        create_registry,
        delete_donor as delete_donor_record,
        inventory_counts,
        search_donors,
    )
else:
    from blood_donor_logic import (
        BLOOD_GROUPS,
        add_donor as add_donor_record,
        create_registry,
        delete_donor as delete_donor_record,
        inventory_counts,
        search_donors,
    )


def build_form(state):
    """Create the form for entering new donor details."""
    form = ttk.LabelFrame(state["root"], text="Add New Donor", padding=10)
    form.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    image_frame = ttk.Frame(form)
    image_frame.grid(row=0, column=0, columnspan=2, pady=(0, 8))
    state["header_image_canvases"] = []
    image_dir = Path(__file__).resolve().parents[2] / "image"

    for column, filename in enumerate(("homepage.jpg", "homepage.png")):
        figure = Figure(figsize=(1.5, 0.625), dpi=100)
        axis = figure.add_axes((0, 0, 1, 1))
        with Image.open(image_dir / filename) as image:
            axis.imshow(image.copy())
        axis.set_axis_off()

        image_canvas = FigureCanvasTkAgg(figure, master=image_frame)
        image_canvas.draw()
        image_canvas.get_tk_widget().grid(row=0, column=column, padx=3)
        state["header_image_canvases"].append(image_canvas)

    state["name_var"] = tk.StringVar()
    state["age_var"] = tk.StringVar()
    state["group_var"] = tk.StringVar()
    state["contact_var"] = tk.StringVar()

    ttk.Label(form, text="Donor Name:").grid(row=1, column=0, sticky="w", pady=4)
    ttk.Entry(form, textvariable=state["name_var"], width=25).grid(
        row=1, column=1, pady=4
    )

    ttk.Label(form, text="Age:").grid(row=2, column=0, sticky="w", pady=4)
    ttk.Entry(form, textvariable=state["age_var"], width=25).grid(
        row=2, column=1, pady=4
    )

    ttk.Label(form, text="Blood Group:").grid(row=3, column=0, sticky="w", pady=4)
    blood_combo = ttk.Combobox(
        form,
        textvariable=state["group_var"],
        values=BLOOD_GROUPS,
        state="readonly",
        width=22,
    )
    blood_combo.grid(row=3, column=1, pady=4)

    ttk.Label(form, text="Contact Info:").grid(row=4, column=0, sticky="w", pady=4)
    ttk.Entry(form, textvariable=state["contact_var"], width=25).grid(
        row=4, column=1, pady=4
    )

    ttk.Button(
        form, text="Submit Donor", command=lambda: add_donor(state)
    ).grid(row=5, column=0, columnspan=2, pady=12)


def build_table(state):
    """Create the donor table, search box, and delete button."""
    table_frame = ttk.LabelFrame(
        state["root"], text="Registered Donors", padding=10
    )
    table_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

    search_frame = ttk.Frame(table_frame)
    search_frame.grid(row=0, column=0, columnspan=2, pady=(0, 10), sticky="w")
    ttk.Label(search_frame, text="Search Name:").grid(row=0, column=0, padx=5)

    state["search_var"] = tk.StringVar()
    search_entry = ttk.Entry(
        search_frame, textvariable=state["search_var"], width=20
    )
    search_entry.grid(row=0, column=1, padx=5)
    state["search_var"].trace_add(
        "write", lambda *_: filter_table(state)
    )

    columns = ("name", "age", "blood_group", "contact")
    state["tree"] = ttk.Treeview(
        table_frame, columns=columns, show="headings", height=8
    )

    headings = {
        "name": "Name",
        "age": "Age",
        "blood_group": "Blood Group",
        "contact": "Contact",
    }
    for column in columns:
        state["tree"].heading(column, text=headings[column])
        state["tree"].column(column, width=100, anchor="center")

    scrollbar = ttk.Scrollbar(
        table_frame, orient="vertical", command=state["tree"].yview
    )
    state["tree"].configure(yscrollcommand=scrollbar.set)
    state["tree"].grid(row=1, column=0, sticky="nsew")
    scrollbar.grid(row=1, column=1, sticky="ns")

    ttk.Button(
        table_frame,
        text="Delete Selected",
        command=lambda: delete_donor(state),
    ).grid(row=2, column=0, sticky="e", pady=5)


def build_chart(state):
    """Create the chart used to display counts by blood group."""
    chart_frame = ttk.LabelFrame(
        state["root"], text="Inventory Chart", padding=10
    )
    chart_frame.grid(
        row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew"
    )

    state["figure"] = Figure(figsize=(8, 2.5), dpi=100)
    state["axis"] = state["figure"].add_subplot(111)
    state["canvas"] = FigureCanvasTkAgg(state["figure"], master=chart_frame)
    state["canvas"].get_tk_widget().pack(fill="both", expand=True)


def add_donor(state):
    """Read the form, request a donor addition, and refresh the display."""
    donor, error_title, error_message = add_donor_record(
        state["registry"],
        state["name_var"].get(),
        state["age_var"].get(),
        state["group_var"].get(),
        state["contact_var"].get(),
    )
    if donor is None:
        messagebox.showwarning(error_title, error_message)
        return

    filter_table(state)
    refresh_chart(state)
    state["name_var"].set("")
    state["age_var"].set("")
    state["group_var"].set("")
    state["contact_var"].set("")


def delete_donor(state):
    """Delete the selected table row and refresh the display."""
    selection = state["tree"].selection()
    if not selection:
        messagebox.showwarning(
            "Selection Missing", "Click a row in the table first."
        )
        return

    selected_item = selection[0]
    try:
        selected_index = int(selected_item)
    except (TypeError, ValueError):
        selected_index = state["tree"].index(selected_item)

    delete_donor_record(state["registry"], selected_index)
    filter_table(state)
    refresh_chart(state)


def filter_table(state):
    """Display donors whose names contain the current search text."""
    for item in state["tree"].get_children():
        state["tree"].delete(item)

    for index, donor in search_donors(
        state["registry"], state["search_var"].get()
    ):
        state["tree"].insert(
            "",
            tk.END,
            iid=str(index),
            values=(
                donor["name"],
                donor["age"],
                donor["blood"],
                donor["contact"],
            ),
        )


def refresh_chart(state):
    """Redraw the blood-group donor-count chart."""
    inventory = inventory_counts(state["registry"])
    heights = [inventory[group] for group in BLOOD_GROUPS]

    state["axis"].clear()
    state["axis"].bar(BLOOD_GROUPS, heights, color="#d9534f")
    state["axis"].set_ylabel("Donors Count")
    state["axis"].set_title("Registered donors by blood group")
    state["axis"].set_ylim(bottom=0)
    state["canvas"].draw()


def main():
    """Create and run the application window."""
    root = tk.Tk()
    root.title("Blood Donor Registry")
    root.geometry("1000x650")

    state = {
        "root": root,
        "registry": create_registry(),
    }
    build_form(state)
    build_table(state)
    build_chart(state)
    root.columnconfigure(1, weight=1)
    root.rowconfigure(0, weight=1)
    refresh_chart(state)
    root.mainloop()


if __name__ == "__main__":
    main()
