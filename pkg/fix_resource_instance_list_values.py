import csv

files = [
    "business_data/all-3d-panels.csv",
]

for f in files:
    outrows = []
    with open(f, 'r') as o:
        reader = csv.reader(o)
        outrows.append(next(reader))
        for row in reader:
            images_val = row[8]
            if images_val:
                images_dicts = [{
                    "resourceId": f"{i}",
                    "ontologyProperty": "",
                    "inverseOntologyProperty": ""
                } for i in images_val.split(",")]
                images_val = str(images_dicts)
            drawings_val = row[9]
            if drawings_val:
                drawings_dicts = [{
                    "resourceId": f"{i}",
                    "ontologyProperty": "",
                    "inverseOntologyProperty": ""
                } for i in drawings_val.split(",")]
                drawings_val = str(drawings_dicts)
            newrow = row[:8] + [images_val] + [drawings_val] + row[-1:]
            outrows.append(newrow)
    
    with open(f.replace(".csv", "_v6.csv"), "w") as o:
        writer = csv.writer(o)
        writer.writerows(outrows)