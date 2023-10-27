import json
import os
import glob
import sqlite3

def main():
    owned, required = load()
    needed_materials = {"Raw": compare(owned["Raw"], required["Raw"]), "Manufactured": compare(owned["Manufactured"], required["Manufactured"]), "Encoded": compare(owned["Encoded"], required["Encoded"])}
    display(needed_materials)
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
    difference = {}
    for name in required:
        count = int(required[name])
        if owned.get(name) == None:
            difference[name] = count
        else:
            difference[name] = count - owned[name]
    return difference
        
def display(needed_materials):
    for type in needed_materials:
        print("------------------ " + type + " Material -------------------")
        for material in needed_materials[type]:
            if needed_materials[type][material] > 0:
                print(material + ":", needed_materials[type][material])
                

if __name__ == "__main__":
    main()