from json import loads
from os import path
from glob import glob
from sqlite3 import connect
from tkinter import Tk, Text, Button, Label, Entry, filedialog, Scrollbar, Frame, TOP, X, LEFT

def main():
    root = Tk()
    root.title("EDEC")
    root.geometry("550x400")
    root.resizable(False, False)
    saved_materials_list = ""
    saved_logs_path = ""
    try:
        with open("state", "r") as f:
            line_count = sum(1 for line in f)
            f.seek(0)
            if line_count > 1:
                saved_logs_path = f.readline()[:-1]
                saved_materials_list = f.read()

    except FileNotFoundError:
        with open("state", "w") as f:
            pass

    show_calculate(root, saved_materials_list, saved_logs_path)
    root.mainloop()


def show_frame(frame, root):
    # Hide all frames except the one to be shown
    for child in root.winfo_children():
        if child != frame:
            child.pack_forget()
    
    # Navbar does not work correctly
    #create_navbar(root)
    
    # Show the selected frame
    frame.pack(expand=True, fill="both")


def show_calculate(root, saved_materials_list, saved_logs_path):
    calculate_frame = Frame(root)
    materials_list_title_label = Label(calculate_frame, text="Enter materials list from coriolis.io")
    materials_list_text = Text(calculate_frame, height=15, width=50)
    entry_and_button_frame = Frame(calculate_frame)
    logs_path_entry = Entry(entry_and_button_frame, width=50)
    select_logs_path = Button(entry_and_button_frame, text="Browse", command=lambda: select_directory(logs_path_entry))
    calculate_button = Button(calculate_frame, text="Calculate", command=lambda: calculate(root, materials_list_text, logs_path_entry))
    
    logs_path_entry.insert(0, saved_logs_path)
    materials_list_text.insert("1.0", saved_materials_list)

    materials_list_title_label.pack()
    materials_list_text.pack(pady=(0,10))
    entry_and_button_frame.pack(pady=10)
    logs_path_entry.pack(side="left", padx=3)
    select_logs_path.pack(side="left", padx=3)
    calculate_button.pack(pady=10)

    show_frame(calculate_frame, root)


def show_results(root, results, materials_list_text, logs_path_entry):
    results_frame = Frame(root)
        
    results_text = Text(results_frame, wrap="word", height=30, width=60, padx=20)
    results_text.insert("1.0", results)
    # Make text read only
    results_text.configure(state="disabled")
    scrollbar = Scrollbar(results_frame, command=results_text.yview)
    results_text.configure(yscrollcommand=scrollbar.set)
    refresh_button = Button(results_frame, text="Refresh", command=lambda: calculate(root, materials_list_text, logs_path_entry))
    
    results_text.grid(row=0, column=1, sticky="nsew")
    scrollbar.grid(row=0, column=2, sticky="ns")
    refresh_button.grid(row=1, column=1, columnspan=3, pady=10)

    results_frame.grid_rowconfigure(0, weight=1)
    results_frame.grid_columnconfigure(1, weight=0)

    show_frame(results_frame, root)


def show_settings(root):
    pass


def create_navbar(root):
    navbar_frame = Frame(root, bg="lightgray", pady=5)
    navbar_frame.pack(side=TOP, fill=X)

    calculate_button = Button(navbar_frame, text="Calculate", command=lambda: show_calculate(root))
    calculate_button.pack(side=LEFT, padx=10)

    settings_button = Button(navbar_frame, text="Settings", command=lambda: show_settings(root))
    settings_button.pack(side=LEFT, padx=10)


def select_directory(logs_path_entry):
    directory_path = filedialog.askdirectory()
    if directory_path:
        logs_path_entry.delete(0, "end")
        logs_path_entry.insert(0, directory_path)
        


def calculate(root, materials_list_text, logs_path_entry):
    # Get data
    materials_list = materials_list_text.get("1.0", "end-1c").strip()
    logs_path = logs_path_entry.get().strip()
    save_info(materials_list, logs_path)
    reset_database()
    owned, required = load(logs_path, materials_list)
    for type in ["Raw", "Manufactured", "Encoded"]:
        compare(owned[type], required[type])
    results = generate_results()
    show_results(root, results, materials_list_text, logs_path_entry)


def save_info(materials_list, logs_path):
    with open("state", "w") as f:
        f.write(logs_path + "\n")
        f.write(materials_list)


def generate_results():
    result_lines = []

    for material_type in ["Raw", "Manufactured", "Encoded"]:
        result_lines.append(f"\n■ {material_type} Material\n")
        with connect("EDEC.db") as con:
            cur = con.cursor()
            cur.execute("  SELECT DISTINCT category FROM materials WHERE type = ?", (material_type,))
            categories = cur.fetchall()
            for category in categories:
                cur.execute("SELECT grade, name, needed FROM materials WHERE category = ? AND needed IS NOT 0 ORDER BY grade DESC", category)
                res = cur.fetchall()
                if res:
                    result_lines.append(f"  {category[0]}\n")

                for row in res:
                    grade, name, amount = row
                    result_lines.append(f"      G{grade} | {name.ljust(40)} {amount}\n")

    results = "".join(result_lines)
    return results


def compare(owned, required):
    for name in required:
        count = int(required[name])
        if owned.get(name) == None:
            needed = 0
        else:
            needed = count - owned[name]
        if needed > 0:
            with connect("EDEC.db") as con:
                cur = con.cursor()
                cur.execute("UPDATE materials SET needed = ? WHERE name = ?", (needed, name))
                con.commit()
    return


def reset_database():
    with connect("EDEC.db") as con:
        cur = con.cursor()
        cur.execute("UPDATE materials SET needed = 0") # Reset needed column in database
        con.commit()


def load(logs_path, materials_list):
    "Returns a dictionary of owned materials and required materials"
    logs = []
    logs_list = glob(logs_path+"/*.log")
    latest_log = max(logs_list, key=path.getctime)
    # Store logs into list
    with open(latest_log,"r") as f:
        for line in f:
            logs.append(loads(line))

    # List of dictionaries of materials 
    # e.g. {'Name': 'pharmaceuticalisolators', 'Name_Localised': 'Pharmaceutical Isolators', 'Count': 5}
    # e.g. {'Name': 'iron', 'Count': 300}
    owned_materials = {"Raw": reformat_logs(logs[2]["Raw"]), "Manufactured": reformat_logs(logs[2]["Manufactured"]), "Encoded": reformat_logs(logs[2]["Encoded"])}
    required_materials = {"Raw": load_required("Raw", materials_list), "Manufactured": load_required("Manufactured", materials_list), "Encoded": load_required("Encoded", materials_list)}
    return owned_materials, required_materials


def reformat_logs(logs):
    reformatted_logs = {}
    for entry in logs:
        if entry.get("Name_Localised") == None:
            reformatted_logs[entry.get("Name").capitalize()] = entry.get("Count")
        else:
            reformatted_logs[entry.get("Name_Localised")] = entry.get("Count")
    return reformatted_logs


def load_required(type, materials_list):
    required_dict = {}
    lines = materials_list.split("\n")
    for line in lines:
        name, count = line.split(": ")
        with connect("EDEC.db") as con:
            cur = con.cursor()
            cur.execute("SELECT * FROM Materials WHERE name = ? AND type = ?", (name,type))
            if cur.fetchone() != None:
                required_dict[name] = count.replace("\n", "")
    return required_dict


if __name__ == "__main__":
    main()