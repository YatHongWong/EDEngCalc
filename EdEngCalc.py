import json
import os
import glob
import sqlite3

def main():
    with sqlite3.connect("EDEC.db") as con:
        cur = con.cursor()
        cur.execute("UPDATE materials SET needed = 0") # Reset needed column in database
        con.commit()
    owned, required = load()
    print(required)
    for type in ["Raw", "Manufactured", "Encoded"]:
        compare(owned[type], required[type])
    display()
    input()

def load():
    "Returns a dictionary of owned materials and required materials"
    logs = []
    logsPath = "C:/Users/User/Saved Games/Frontier Developments/Elite Dangerous" # Edit this to your directory
    logsList = glob.glob(logsPath+"/*.log")
    latestLog = max(logsList, key=os.path.getctime)
    # Store logs into list
    with open(latestLog,"r") as f:
        for line in f:
            logs.append(json.loads(line))

    # List of dictionaries of materials 
    # e.g. {'Name': 'pharmaceuticalisolators', 'Name_Localised': 'Pharmaceutical Isolators', 'Count': 5}
    # e.g. {'Name': 'iron', 'Count': 300}
    ownedMaterials = {"Raw": reformat_logs(logs[2]["Raw"]), "Manufactured": reformat_logs(logs[2]["Manufactured"]), "Encoded": reformat_logs(logs[2]["Encoded"])}
    requiredMaterials = {"Raw": load_required("Raw"), "Manufactured": load_required("Manufactured"), "Encoded": load_required("Encoded")}
    return ownedMaterials, requiredMaterials


def reformat_logs(logs):
    reformatted_logs = {}
    for entry in logs:
        if entry.get("Name_Localised") == None:
            reformatted_logs[entry.get("Name").capitalize()] = entry.get("Count")
        else:
            reformatted_logs[entry.get("Name_Localised")] = entry.get("Count")
    return reformatted_logs


def load_required(type):
    required_dict = {}
    with open("engineering.txt") as required:
        for line in required:
            name, count = line.split(": ")
            with sqlite3.connect("EDEC.db") as con:
                cur = con.cursor()
                cur.execute("SELECT * FROM Materials WHERE name = ? AND type = ?", (name,type))
                if cur.fetchone() != None:
                    required_dict[name] = count.replace("\n", "")
        return required_dict


def compare(owned, required):
    for name in required:
        count = int(required[name])
        if owned.get(name) == None:
            needed = 0
        else:
            needed = count - owned[name]
        if needed > 0:
            with sqlite3.connect("EDEC.db") as con:
                cur = con.cursor()
                print("Updated", name, needed)
                cur.execute("UPDATE materials SET needed = ? WHERE name = ?", (needed, name))
                con.commit()
    return
        
def display():
    for type in ["Raw", "Manufactured", "Encoded"]:
        print("\n------------------ " + type + " Material -------------------\n")
        with sqlite3.connect("EDEC.db") as con:
                cur = con.cursor()
                cur.execute("SELECT DISTINCT category FROM materials WHERE type = ?", (type,))
                categories = cur.fetchall()
                for category in categories:
                    cur.execute("SELECT grade, name, needed FROM materials WHERE category = ? AND needed IS NOT 0 ORDER BY grade DESC", category)
                    res = cur.fetchall()
                    if res != []:
                        print("--" + category[0] + "--")

                    for row in res:
                        grade, name, amount = row
                        print(f"G{grade} | {name}: {amount}")


if __name__ == "__main__":
    main()