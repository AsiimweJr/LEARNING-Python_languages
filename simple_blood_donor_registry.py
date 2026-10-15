# Simple Blood Donor Registry
# This beginner project lets you add, view, search, and delete donors.

donors = []

def add_donor():
    name = input("Enter donor name: ").strip()
    age_text = input("Enter donor age: ").strip()
    blood_group = input("Enter blood group (A+, A-, B+, B-, AB+, AB-, O+, O-): ").upper().strip()
    contact = input("Enter contact number: ").strip()

    if not name or not age_text or not blood_group or not contact:
        print("Please fill in all details.")
        return

    if not age_text.isdigit() or int(age_text) <= 0:
        print("Age must be a positive whole number.")
        return

    valid_groups = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
    if blood_group not in valid_groups:
        print("That is not a valid blood group.")
        return

    donor = {
        "name": name,
        "age": int(age_text),
        "blood_group": blood_group,
        "contact": contact
    }

    donors.append(donor)
    print("Donor added successfully!")


def view_donors():
    if not donors:
        print("No donors have been registered yet.")
        return

    print("\n--- Registered Donors ---")
    for number, donor in enumerate(donors, start=1):
        print(f"{number}. {donor['name']} | Age: {donor['age']} | "
              f"Blood group: {donor['blood_group']} | Contact: {donor['contact']}")


def search_donor():
    search_name = input("Enter the name to search for: ").strip().lower()
    matches = [donor for donor in donors if search_name in donor["name"].lower()]

    if matches:
        print("\n--- Search Results ---")
        for donor in matches:
            print(f"{donor['name']} | Age: {donor['age']} | "
                  f"Blood group: {donor['blood_group']} | Contact: {donor['contact']}")
    else:
        print("No matching donor found.")


def delete_donor():
    view_donors()
    if not donors:
        return

    choice = input("Enter the donor number to delete: ").strip()
    if not choice.isdigit():
        print("Please enter a valid number.")
        return

    index = int(choice) - 1
    if 0 <= index < len(donors):
        removed = donors.pop(index)
        print(f"{removed['name']} has been deleted.")
    else:
        print("That donor number does not exist.")


def count_by_blood_group():
    groups = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
    print("\n--- Donor Count by Blood Group ---")
    for group in groups:
        count = sum(1 for donor in donors if donor["blood_group"] == group)
        print(f"{group}: {count}")


def main():
    while True:
        print("\n===== BLOOD DONOR REGISTRY =====")
        print("1. Add donor")
        print("2. View all donors")
        print("3. Search donor by name")
        print("4. Delete donor")
        print("5. Count donors by blood group")
        print("6. Exit")

        choice = input("Choose an option (1-6): ").strip()

        if choice == "1":
            add_donor()
        elif choice == "2":
            view_donors()
        elif choice == "3":
            search_donor()
        elif choice == "4":
            delete_donor()
        elif choice == "5":
            count_by_blood_group()
        elif choice == "6":
            print("Thank you life saverS!")
            break
        else:
            print("Invalid choice. Please choose from 1 to 6.")


if __name__ == "__main__":
    main()
