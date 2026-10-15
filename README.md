# Blood Bank Directory

This directory contains a small donor-management project built with Python, Tkinter, and Matplotlib. It is designed to register blood donors, display them in a table, and visualize donor counts by blood group.

## Overview

The project includes:

- a graphical desktop app for adding and viewing donors
- a search box to filter donor names
- a donor inventory chart grouped by blood type
- a simple text-based console version for quick testing

## Folder contents

- `scripts/blood_donor_app.py` – main GUI application
- `scripts/blood_donor_logic.py` – functions for donor validation, registry operations, search, and inventory counts

## Features

- Add donor details: name, age, blood group, and contact information
- Validate required fields and age input
- Filter the donor list by name
- Delete a selected donor from the table
- Update the blood group chart automatically after each change

## Requirements

- Python 3
- Tkinter
- Matplotlib

On Linux, Tkinter may need to be installed separately:

```bash
sudo apt install python3-tk
```

## Run the graphical application

From the repository root:

```bash
python3 blood_bank/scripts/blood_donor_app.py
```

Or, from inside the `blood_bank` directory:

```bash
cd blood_bank
python3 scripts/blood_donor_app.py
```

## Install dependencies

If Matplotlib is not installed in your environment:

```bash
python3 -m pip install matplotlib
```

## Notes

- Donor data is stored only in memory while the program is running.
- The app does not currently save records to a file or database.
- The accepted blood groups are: A+, A-, B+, B-, AB+, AB-, O+, and O-.
