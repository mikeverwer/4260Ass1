import csv

balloon = int(input("How many times bigger should the file be?\n"))
output_filename = f"balloon_{balloon}x.csv"

with open('all_stocks_5yr.csv', 'r', newline='') as file:
    reader = csv.reader(file)
    header = next(reader)

    with open(output_filename, 'w', newline='') as out:
        writer = csv.writer(out)
        writer.writerow(header)

        for row in reader:
            for _ in range(balloon):
                writer.writerow(row)

print("Verifying...")

with open('all_stocks_5yr.csv', 'r', newline='') as file:
    reader = csv.reader(file)
    next(reader)
    row_count = sum(1 for _ in reader)

with open(output_filename, 'r', newline='') as new_file:
    reader = csv.reader(new_file)
    next(reader)
    new_row_count = sum(1 for _ in new_file)

print(f"Original row count: {row_count}\nNew file row count: {new_row_count}\nNew file is {round(new_row_count/row_count)} times larger.")
