import csv
import yaml

settings = yaml.load(open('config.yaml'), Loader=yaml.FullLoader)
colleges = list(settings["colleges"])
traits_list = list(settings["traits"])

input_path = settings["input_path"]
output_path = settings["output_path"]

input_file = csv.DictReader(open('college_info.csv', 'r'))
output_file = csv.writer(open('output_data.csv', 'w'))

output_file.writerow(["college"]+traits_list)

for row in input_file:
    if row["name"] in colleges:
        write_row = [row["name"]]

        for trait in traits_list:
            try:
                write_row.append(row[trait])
            except KeyError:
                print("Could not find key: " + trait)
                write_row.append("")

        output_file.writerow(write_row)

print(f"Okay all the stuff is saved in {output_path}")
