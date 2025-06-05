import json
import os
import re
import datetime

FILE_PATH = "contacts.json"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def load_data():
    if not os.path.exists(FILE_PATH):
        return []
    try:
        with open(FILE_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def save_data(data):
    with open(FILE_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

def banner(title):
    print("\n" + "=" * 60)
    print(title.center(60))
    print("=" * 60)

def input_with_validation(prompt, pattern, warning):
    while True:
        value = input(prompt).strip()
        if re.fullmatch(pattern, value):
            return value
        print(f"⚠ {warning}")

def input_name():
    return input_with_validation("Name (2-50 letters/spaces): ", r"[A-Za-z ]{2,50}", "Invalid name format.")

def input_phone():
    return input_with_validation("Phone (10 digits): ", r"\d{10}", "Phone must be 10 digits.")

def input_email():
    return input_with_validation("Email: ", r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", "Invalid email format.")

def match_contacts(data, term):
    term = term.lower()
    return [c for c in data if term in c['name'].lower() or term in c['phone'] or term in c['email'].lower()]

def pick_contact(matches):
    for i, c in enumerate(matches, 1):
        print(f"{i}. {c['name']} | 📞 {c['phone']} | 📧 {c['email']}")
    try:
        index = int(input("Choose a number: ")) - 1
        if 0 <= index < len(matches):
            return matches[index]
    except:
        pass
    print("⚠ Invalid selection.")
    return None

def add_entry(data):
    banner("Add Contact")
    name = input_name()
    phone = input_phone()
    email = input_email()
    if any(c['phone'] == phone or c['email'].lower() == email.lower() for c in data):
        print("🚫 Duplicate contact exists!")
        return
    data.append({
        "name": name,
        "phone": phone,
        "email": email,
        "added": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    save_data(data)
    print("✅ Contact added.")

def edit_entry(data):
    banner("Edit Contact")
    term = input("Search by name/phone/email: ").strip()
    matches = match_contacts(data, term)
    if matches:
        selected = pick_contact(matches)
        if selected:
            print(f"Editing {selected['name']}")
            selected['name'] = input_name()
            selected['phone'] = input_phone()
            selected['email'] = input_email()
            selected['added'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            save_data(data)
            print("✅ Updated successfully.")
    else:
        print("🚫 No matches found.")

def remove_entry(data):
    banner("Delete Contact")
    term = input("Search to delete: ").strip()
    matches = match_contacts(data, term)
    if matches:
        selected = pick_contact(matches)
        if selected:
            confirm = input(f"Delete {selected['name']}? (yes/no): ").strip().lower()
            if confirm == 'yes':
                data.remove(selected)
                save_data(data)
                print("🗑 Deleted.")
            else:
                print("❌ Cancelled.")
    else:
        print("🚫 No matches found.")

def search_entry(data):
    banner("Search Contacts")
    term = input("Search: ").strip()
    matches = match_contacts(data, term)
    if matches:
        for i, c in enumerate(matches, 1):
            print(f"{i}. {c['name']} | 📞 {c['phone']} | 📧 {c['email']} | 🕒 {c['added']}")
    else:
        print("📭 No results.")

def show_all(data):
    banner("All Contacts")
    if not data:
        print("📭 No contacts stored.")
        return
    for i, c in enumerate(sorted(data, key=lambda x: x['name'].lower()), 1):
        print(f"{i}. {c['name']} | 📞 {c['phone']} | 📧 {c['email']} | 🕒 {c['added']}")
    print(f"\nTotal: {len(data)} contacts.")

def wipe_all(data):
    banner("Clear All Contacts")
    confirm = input("This will remove everything. Continue? (yes/no): ").strip().lower()
    if confirm == 'yes':
        data.clear()
        save_data(data)
        print("🗑 All contacts deleted.")
    else:
        print("❌ Cancelled.")

def menu():
    banner("ContactMaster - Menu")
    print("1. ➕ Add Contact")
    print("2. ✏ Edit Contact")
    print("3. ❌ Delete Contact")
    print("4. 🔍 Search Contact")
    print("5. 📒 View All")
    print("6. 🗑 Clear All")
    print("7. 🚪 Exit")
    print("=" * 60)

def main():
    contact_list = load_data()
    while True:
        menu()
        choice = input("Choose (1–7): ").strip()
        clear_screen()

        if choice == '1':
            add_entry(contact_list)
        elif choice == '2':
            edit_entry(contact_list)
        elif choice == '3':
            remove_entry(contact_list)
        elif choice == '4':
            search_entry(contact_list)
        elif choice == '5':
            show_all(contact_list)
        elif choice == '6':
            wipe_all(contact_list)
        elif choice == '7':
            print("\n👋 Goodbye from ContactMaster!")
            break
        else:
            print("❌ Invalid input. Choose 1–7.")

        input("\nPress Enter to return...")
        clear_screen()

if __name__ == "__main__":
    main()