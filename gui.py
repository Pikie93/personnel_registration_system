import tkinter as tk
from tkinter import ttk, messagebox
from KMS_1_01_LE_06_Down import PersonData, confirm_info, change_values
class PersonnelInfoUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Personnel Info")

        self.container = ttk.Frame(self.root)
        self.container.pack(fill="both", expand=True)

        self.frames = {}
        for f in (MainMenu, AddNew):#, #ViewData, EditData, Bdays, DelData):
            frame = f(self.container, self)
            self.frames[f] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(MainMenu)

    def show_frame(self, fr):
        fr = self.frames[fr]
        fr.tkraise()

class MainMenu(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self,parent)
        self.controller = controller

        label = ttk.Label(self, text="Main Menu")
        label.pack(pady=10, padx=10)

        buttons = [
            ("Add Person", AddNew)#,
            #("View Data", ViewData),
            #("Edit Data", EditData),
            #("Birthdays", Bdays),
            #("Delete Data", DelData)
        ]

        for text, page in buttons:
            ttk.Button(self, text=text, command=lambda p=page: controller.show_frame(p)).pack(pady=5)

class AddNew(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller

        label = ttk.Label(self, text="Add Person")
        label.grid(row=0, column=0, columnspan=2, pady=10, padx=10)

        self.entries = {}
        entry_fields = [
            ("Name", "name"),
            ("Address", "address"),
            ("Date of Birth", "dob"),
            ("Phone Number", "phone"),
            ("Email", "email")
        ]

        for i, (field_label, field_name) in enumerate(entry_fields, start=1):
            ttk.Label(self, text=f"{field_label}:").grid(row=i, column=0, sticky="e", padx=5, pady=5)
            self.entries[field_name] = ttk.Entry(self)
            self.entries[field_name].grid(row=i, column=1, padx=5, pady=5)

        ttk.Label(self, text="Status:").grid(row=len(entry_fields)+1, column=0, sticky="e", padx=5, pady=5)
        self.status_var = tk.StringVar()
        self.status_dropdown = ttk.Combobox(self, textvariable=self.status_var, values=["Employee", "Visitor"], state="readonly")
        self.status_dropdown.grid(row=len(entry_fields)+1, column=1, padx=5, pady=5)
        self.status_dropdown.set("Select Status")

        ttk.Button(self, text="Add Person", command=self.add_person).grid(row=len(entry_fields)+2, column=0, columnspan=2, pady=10)

        ttk.Button(self, text="Back to Main Menu", command=lambda:controller.show_frame(MainMenu)).grid(row=len(entry_fields)+3, column=0, columnspan=2, pady=10)

    def add_person(self):
        person_preview = PersonData("", "", "", "", "", "", "", "")

        validations = [
            (person_preview.set_name, self.entries["name"].get(), self.controller.people_data),
            (person_preview.set_address, self.entries["address"].get()),
            (person_preview.set_dob, self.entries["dob"].get()),
            (person_preview.set_phone_number, self.entries["phone"].get()),
            (person_preview.set_email, self.entries["email"].get()),
            (person_preview.set_status, self.status_var.get())
        ]

        for validation_func, *args in validations:
            success, message = validation_func(*args)
            if not success:
                messagebox.showerror("Error", message)
                return

        new_person = PersonData(person_preview.get_name(), person_preview.get_first_name(), person_preview.get_last_name(),
                                person_preview.get_status(), person_preview.get_address(), person_preview.get_dob(),
                                person_preview.get_phone_number(), person_preview.get_email())

        self.show_confirmation(new_person)

    def show_confirmation(self, person_data):
        confirm_window = tk.Toplevel(self)
        confirm_window.title("Confirm Information")

        ttk.Label(confirm_window, text="Please confirm the entered information:").pack(pady=10)
        ttk.Label(confirm_window, text=str(person_data), justify=tk.LEFT).pack(padx=20, pady=10)

        def on_confirm():
            confirm_window.destroy()
            result = confirm_info(person_data)
            if result == "add":
                self.finalize(person_data)
            elif result == "redo":
                pass
            elif result == "exit":
                self.clear_entries()

        def on_edit():
            confirm_window.destroy()

        def on_cancel():
            confirm_window.destroy()
            self.clear_entries()

        ttk.Button(confirm_window, text="Confirm", command=on_confirm).pack(side=tk.LEFT, padx=10, pady=10)
        ttk.Button(confirm_window, text="Edit", command=on_edit).pack(side=tk.LEFT, padx=10, pady=10)
        ttk.Button(confirm_window, text="Cancel", command=on_cancel).pack(side=tk.LEFT, padx=10, pady=10)

    def finalize(self, person_data):
        if person_data.get_name() not in self.controller.people_data:
            self.controller.people_data[person_data.get_name()] = person_data
            messagebox.showinfo("Success", f"Added {person_data.get_name()} to the database.")
        else:
            messagebox.showerror("Error", "This name already exists in the records")

    def clear_entries(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)
        self.status_dropdown.set("Select Status")

def run_gui():
    root = tk.Tk()
    app = PersonnelInfoUI(root)
    root.mainloop()

if __name__ == "__main__":
    run_gui()
