import json
import os
import glob

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
            if name in materialCategorisation[type]:
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
                





materialCategorisation = {
    "Raw":["Carbon",
           "Vanadium",
           "Niobium",
           "Yttrium",
           "Phosphorus",
           "Chromium",
           "Molybdenum",
           "Technetium",
           "Sulphur",
           "Manganese",
           "Cadmium",
           "Ruthenium",
           "Iron",
           "Zinc",
           "Tin",
           "Selenium",
           "Nickel",
           "Germanium",
           "Tungsten",
           "Tellurium",
           "Rhenium",
           "Arsenic",
           "Mercury",
           "Polonium",
           "Lead",
           "Zirconium",
           "Boron",
           "Antimony"],
    "Manufactured":[
            "Chemical Storage Units",
            "Chemical Processors",
            "Chemical Distillery",
            "Chemical Manipulators",
            "Pharmaceutical Isolators",
            "Tempered Alloys",
            "Heat Resistant Ceramics",
            "Precipitated Alloys",
            "Thermic Alloys",
            "Military Grade Alloys",
            "Heat Conduction Wiring",
            "Heat Dispersion Plate",
            "Heat Exchangers",
            "Heat Vanes",
            "Proto Heat Radiators",      
            "Basic Conductors",
            "Conductive Components",
            "Conductive Ceramics",
            "Conductive Polymers",
            "Biotech Conductors",
            "Mechanical Scrap",
            "Mechanical Equipment",
            "Mechanical Components",
            "Configurable Components",
            "Improvised Components", 
            "Grid Resistors",
            "Hybrid Capacitors",
            "Electrochemical Arrays",
            "Polymer Capacitors",
            "Military Supercapacitors",
            "Worn Shield Emitters",
            "Shield Emitters",
            "Shielding Sensors",
            "Compound Shielding",
            "Imperial Shielding",
            "Compact Composites",
            "Filament Composites",
            "High Density Composites",
            "Proprietary Composites",
            "Core Dynamics Composites",
            "Crystal Shards",
            "Flawed Focus Crystals",
            "Focus Crystals",
            "Refined Focus Crystals",
            "Exquisite Focus Crystals",
            "Salvaged Alloys",
            "Galvanising Alloys",
            "Phase Alloys",
            "Proto Light Alloys",
            "Proto Radiolic Alloys"],
    "Encoded":[
            "Exceptional Scrambled Emission Data",
            "Irregular Emission Data",
            "Unexpected Emission Data",
            "Decoded Emission Data",
            "Abnormal Compact Emissions Data",
            "Atypical Disrupted Wake Echoes",
            "Anomalous FSD Telemetry",
            "Strange Wake Solutions",
            "Eccentric Hyperspace Trajectories",
            "Datamined Wake Exceptions",
            "Distorted Shield Cycle Recordings",
            "Inconsistent Shield Soak Analysis",
            "Untypical Shield Scans",
            "Aberrant Shield Pattern Analysis",
            "Peculiar Shield Frequency Data",  
            "Unusual Encrypted Files",
            "Tagged Encryption Codes",
            "Open Symmetric Keys",
            "Atypical Encryption Archives",
            "Adaptive Encryptors Capture",
            "Anomalous Bulk Scan Data",
            "Unidentified Scan Archives",
            "Classified Scan Databanks",
            "Divergent Scan Data",
            "Classified Scan Fragment",
            "Specialised Legacy Firmware",
            "Modified Consumer Firmware",
            "Cracked Industrial Firmware",
            "Security Firmware Patch",
            "Modified Embedded Firmware",]
}
dictOfMaterials = {
    "Raw": {
        "Category 1":{
            "Carbon":1,
            "Vanadium":2,
            "Niobium":3,
            "Yttrium":4,
        },
        "Category 2":{
            "Phosphorus":1,
            "Chromium":2,
            "Molybdenum":3,
            "Technetium":4,
        },
        "Category 3":{
            "Sulphur":1,
            "Manganese":2,
            "Cadmium":3,
            "Ruthenium":4,
        },
        "Category 4":{
            "Iron":1,
            "Zinc":2,
            "Tin":3,
            "Selenium":4,
        },
        "Category 5":{
            "Nickel":1,
            "Germanium":2,
            "Tungsten":3,
            "Tellurium":4,
        },
        "Category 6":{
            "Rhenium":1,
            "Arsenic":2,
            "Mercury":3,
            "Polonium":4,
        },
        "Category 7":{
            "Lead":1,
            "Zirconium":2,
            "Boron":3,
            "Antimony":4,
        },
    },
    "Manufactured": {
        "Chemical":{
            "Chemical Storage Units":1,
            "Chemical Processors": 2,
            "Chemical Distillery": 3,
            "Chemical Manipulators": 4,
            "Pharmaceutical Isolators":5
        },
        "Thermic":{
            "Tempered Alloys":1,
            "Heat Resistant Ceramics":2,
            "Precipitated Alloys":3,
            "Thermic Alloys":4,
            "Military Grade Alloys":5
        },
        "Heat":{
            "Heat Conduction Wiring":1,
            "Heat Dispersion Plate":2,
            "Heat Exchangers":3,
            "Heat Vanes":4,
            "Proto Heat Radiators":5        
        },
        "Conductive":{
            "Basic Conductors":1,
            "Conductive Components":2,
            "Conductive Ceramics":3,
            "Conductive Polymers":4,
            "Biotech Conductors":5 
        },
        "Mechanical Components":{
            "Mechanical Scrap":1,
            "Mechanical Equipment":2,
            "Mechanical Components":3,
            "Configurable Components":4,
            "Improvised Components":5 
        },
        "Capacitors":{
            "Grid Resistors":1,
            "Hybrid Capacitors":2,
            "Electrochemical Arrays":3,
            "Polymer Capacitors":4,
            "Military Supercapacitors":5 
        },
        "Shielding":{
            "Worn Shield Emitters":1,
            "Shield Emitters":2,
            "Shielding Sensors":3,
            "Compound Shielding":4,
            "Imperial Shielding":5 
        },
        "Composite":{
            "Compact Composites":1,
            "Filament Composites":2,
            "High Density Composites":3,
            "Proprietary Composites":4,
            "Core Dynamics Composites":5 
        },
        "Crystals":{
            "Crystal Shards":1,
            "Flawed Focus Crystals":2,
            "Focus Crystals":3,
            "Refined Focus Crystals":4,
            "Exquisite Focus Crystals":5 
        },
        "Alloys":{
            "Salvaged Alloys":1,
            "Galvanising Alloys":2,
            "Phase Alloys":3,
            "Proto Light Alloys":4,
            "Proto Radiolic Alloys":5 
        },
    },
    "Encoded": {
        "Emission Data":{
            "Exceptional Scrambled Emission Data":1,
            "Irregular Emission Data": 2,
            "Unexpected Emission Data": 3,
            "Decoded Emission Data": 4,
            "Abnormal Compact Emissions Data":5
        },
        "Wake Scans":{
            "Atypical Disrupted Wake Echoes":1,
            "Anomalous FSD Telemetry":2,
            "Strange Wake Solutions":3,
            "Eccentric Hyperspace Trajectories":4,
            "Datamined Wake Exceptions":5
        },
        "Shield Data":{
            "Distorted Shield Cycle Recordings":1,
            "Inconsistent Shield Soak Analysis":2,
            "Untypical Shield Scans":3,
            "Aberrant Shield Pattern Analysis":4,
            "Peculiar Shield Frequency Data":5        
        },
        "Encryption Files":{
            "Unusual Encrypted Files":1,
            "Tagged Encryption Codes":2,
            "Open Symmetric Keys":3,
            "Atypical Encryption Archives":4,
            "Adaptive Encryptors Capture":5 
        },
        "Data Archives":{
            "Anomalous Bulk Scan Data":1,
            "Unidentified Scan Archives":2,
            "Classified Scan Databanks":3,
            "Divergent Scan Data":4,
            "Classified Scan Fragment":5 
        },
        "Encoded Firmware":{
            "Specialised Legacy Firmware":1,
            "Modified Consumer Firmware":2,
            "Cracked Industrial Firmware":3,
            "Security Firmware Patch":4,
            "Modified Embedded Firmware":5 
        }
    }
}

if __name__ == "__main__":
    main()