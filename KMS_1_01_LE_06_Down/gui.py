import tkinter as tk
import calendar, person_data_class
from tkinter import ttk, messagebox, simpledialog
from KMS_1_01_LE_06_Down import change_values, read_from, write_to, delete_data, birthdays, filter_view



class PersonnelInfoUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Personnel Info")
        self.root.geometry("435x475")
        self.root.resizable(False, False)

        self.filename = "personnel_data.json"
        try:
            self.people_data = read_from(self.filename)
        except Exception as e:
            messagebox.showerror("Error", str(e))

        self.container = ttk.Frame(self.root)
        self.container.pack(fill="both", expand=True)

        self.frames = {}
        for f in (MainMenu, AddNew, ViewData, EditData, Bdays, DelData):
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
        label.pack(padx=10, pady=10)

        buttons = [
            ("Add Person", AddNew),
            ("View Data", ViewData),
            ("Edit Data", EditData),
            ("Birthdays", Bdays),
            ("Delete Data", DelData)
        ]

        for text, page in buttons:
            ttk.Button(self, text=text, command=lambda p=page: controller.show_frame(p)).pack(pady=5)

class AddNew(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        label = ttk.Label(self, text="Add Person")
        label.grid(row=0, column=0, columnspan=2, padx=10,pady=10)

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
            self.entries[field_name].grid(row=i, column=1, sticky="w", padx=5, pady=5)

        self.entries["phone"].insert(0, "+43")

        ttk.Label(self, text="Status:").grid(row=len(entry_fields)+1, column=0, sticky="e", padx=5, pady=5)
        self.status_var = tk.StringVar()
        self.status_dropdown = ttk.Combobox(self, textvariable=self.status_var, values=["Employee", "Visitor"], state="readonly")
        self.status_dropdown.grid(row=len(entry_fields)+1, column=1, sticky="w", padx=5, pady=5)
        self.status_dropdown.set("Select Status")

        ttk.Button(self, text="Add Person", command=self.add_person).grid(row=len(entry_fields)+2, column=0, columnspan=2, pady=10)

        ttk.Button(self, text="Back to Main Menu", command=lambda:controller.show_frame(MainMenu)).grid(row=len(entry_fields)+3, column=0, columnspan=2, pady=10)

    def add_person(self):
        try:
            person_preview = person_data_class.PersonData("", "", "", "", "", "", "", "")
            person_preview.set_name(self.entries["name"].get(), self.controller.people_data)
            person_preview.set_address(self.entries["address"].get())
            person_preview.set_dob(self.entries["dob"].get())
            person_preview.set_phone_number(self.entries["phone"].get())
            person_preview.set_email(self.entries["email"].get())
            person_preview.set_status(self.status_var.get())

            if not all([person_preview.get_name(), person_preview.get_address(), person_preview.get_dob(), person_preview.get_phone_number(), person_preview.get_email(), person_preview.get_status()]):
                raise ValueError("Not all fields were set correctly.")

            new_person = person_data_class.PersonData(person_preview.get_name(),
                                    person_preview.get_first_name(),
                                    person_preview.get_last_name(),
                                    person_preview.get_status(),
                                    person_preview.get_address(),
                                    person_preview.get_dob(),
                                    person_preview.get_phone_number(),
                                    person_preview.get_email())

            self.show_confirmation(new_person)

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def show_confirmation(self, person_data):
        result = messagebox.askyesnocancel("Confirm Information", f"{person_data}\n\nPress Yes to confirm and add to records.\nPress No to redo the entry.\nPress Cancel to exit.")

        if result is True:
            self.finalize(person_data)
        elif result is False:
            pass
        else:
            self.clear_entries()

    def finalize(self, person_data):
        try:
            self.controller.people_data[person_data.get_name()] = person_data
            write_to(self.controller.filename, self.controller.people_data)
            messagebox.showinfo("Success", f"Added {person_data.get_name()} to the database.")
            self.clear_entries()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def clear_entries(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)
        self.entries["phone"].insert(0, "+43")
        self.status_dropdown.set("Select Status")

class ViewData(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        label = ttk.Label(self, text="View Data")
        label.pack(padx=10, pady=10)

        self.options = [
            "View all Data",
            "View Full Names",
            "View First Names",
            "View Last Names",
            "View Employees",
            "View Visitors",
            "View Addresses",
            "View Dates of Birth",
            "View Phone Numbers"
        ]
        self.combo = ttk.Combobox(self, values=self.options, state="readonly")
        self.combo.set("Select an option")
        self.combo.pack(pady=10)
        self.combo.bind("<<ComboboxSelected>>", self.on_select)

        text_frame = ttk.Frame(self)
        text_frame.pack(expand=True, fill="both", padx=10, pady=10)

        self.text_area = tk.Text(text_frame, wrap=tk.WORD, width=50, height=20)
        self.text_area.pack(side=tk.LEFT, expand=True, fill="both")

        scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=self.text_area.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.text_area.configure(yscrollcommand=scrollbar.set)

        ttk.Button(self, text="Back to Main Menu", command=lambda:controller.show_frame(MainMenu)).pack(pady=10)

    def on_select(self, _):
        selection = self.combo.get()
        data = filter_view(selection, self.controller.people_data)
        self.display_data(data)

    def display_data(self, data):
        self.text_area.delete("1.0", tk.END)
        self.text_area.insert(tk.END, data)

class EditData(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller

        label = ttk.Label(self, text="Edit Data")
        label.pack(padx=10, pady=10)

        self.person_var = tk.StringVar()
        self.person_dropdown = ttk.Combobox(self, textvariable=self.person_var, state="readonly")
        self.person_dropdown["values"] = list(self.controller.people_data.keys())
        self.person_dropdown.set("Select a person")
        self.person_dropdown.pack(pady=5)

        self.attribute_var = tk.StringVar()
        self.attribute_dropdown = ttk.Combobox(self, textvariable=self.attribute_var, state="readonly")
        self.attribute_dropdown["values"] = [
            "Full Name",
            "First Name",
            "Last Name",
            "Status",
            "Address",
            "Date of Birth",
            "Phone Number",
            "Email Address"
        ]
        self.attribute_dropdown.set("Select an attribute to edit")
        self.attribute_dropdown.pack(pady=5)

        ttk.Button(self, text="Update", command=self.update_value).pack(pady=5)

        ttk.Button(self, text="Back to Main Menu", command=lambda: controller.show_frame(MainMenu)).pack(pady=10)

    def update_value(self):
        selected_person = self.person_var.get()
        selected_attribute = self.attribute_var.get()

        if not selected_person or selected_person == "Select a person":
            messagebox.showerror("Error", "Please select a person.")
            return

        if not selected_attribute or selected_attribute == "Select an attribute to edit":
            messagebox.showerror("Error", "Please select an attribute.")
            return

        person = self.controller.people_data[selected_person]

        new_value = simpledialog.askstring("Input", f"Enter a new value for {selected_attribute}: ")

        if new_value is None:
            return

        result = change_values(person, selected_attribute, new_value, self.controller.people_data, self.controller.filename)

        messagebox.showinfo("Update Result", result)

        self.person_var.set("Select a person")
        self.attribute_var.set("Select an attribute")

        self.controller.people_data = read_from(self.controller.filename)
        print(self.controller.people_data)
        self.person_dropdown["values"] = list(self.controller.people_data.keys())

class Bdays(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller

        label = ttk.Label(self, text="Birthdays")
        label.pack(padx=10, pady=10)

        self.month_select = ttk.Combobox(self, values=list(calendar.month_name[1:]), state="readonly")
        self.month_select.set("Select a month")
        self.month_select.pack(pady=10)
        self.month_select.bind("<<ComboboxSelected>>", self.on_select)

        text_frame = ttk.Frame(self)
        text_frame.pack(expand=True, fill="both", padx=10, pady=10)

        self.text_area = tk.Text(text_frame, wrap=tk.WORD, width=50, height=20)
        self.text_area.pack(side=tk.LEFT, expand=True, fill="both")

        scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=self.text_area.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.text_area.configure(yscrollcommand=scrollbar.set)

        ttk.Button(self, text="Back to Main Menu", command=lambda: controller.show_frame(MainMenu)).pack(pady=10)

    def on_select(self, _):
        selection = self.month_select.get()
        data = birthdays(selection, self.controller.people_data)
        self.display_data(data)

    def display_data(self, data):
        self.text_area.delete("1.0", tk.END)
        self.text_area.insert(tk.END, data)

class DelData(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller

        label = ttk.Label(self, text="Delete Data")
        label.pack(padx=10, pady=10)

        ttk.Button(self, text="Delete All Data", command=self.delete_all_data).pack(pady=5)

        ttk.Button(self, text="Delete Entry", command=self.delete_entry).pack(pady=5)

        ttk.Button(self, text="Back to Main Menu", command=lambda: controller.show_frame(MainMenu)).pack(pady=10)

    def delete_all_data(self):
        if messagebox.askyesno("Confirm", "Are you sure you want to delete all data?"):
            try:
                delete_data(self.controller.filename)
                result = self.controller.people_data.clear()
                messagebox.showinfo("Success", result)
            except Exception as e:
                messagebox.showerror("Error", str(e))


    def delete_entry(self):
        del_window = tk.Toplevel(self)
        del_window.title("Delete Entry")
        del_window.geometry("300x150")
        x = self.winfo_rootx() + 50
        y = self.winfo_rooty() + 50

        del_window.geometry(f"+{x}+{y}")

        person_var = tk.StringVar()
        person_dropdown = ttk.Combobox(del_window, textvariable=person_var, state="readonly")
        person_dropdown["values"] = list(self.controller.people_data.keys())
        person_dropdown.set("Select a person")
        person_dropdown.pack(pady=5)

        def confirm_delete():
            selected_person = person_var.get()
            if selected_person and selected_person != "Select a person":
                if messagebox.askyesno("Confirm", f"Are you sure you want to delete the data for {selected_person}?"):
                    try:
                        result = delete_data(self.controller.filename, selected_person)
                        self.controller.people_data = read_from(self.controller.filename)

                        messagebox.showinfo("Delete Result", result)

                        person_dropdown["values"] = list(self.controller.people_data.keys())
                        person_var.set("Select a person")

                    except Exception as e:
                        messagebox.showerror("Error", str(e))

        ttk.Button(del_window, text="Delete", command=confirm_delete).pack(pady=5)

def run_gui():
    root = tk.Tk()
    _ = PersonnelInfoUI(root)
    root.mainloop()

if __name__ == "__main__":
    run_gui()

