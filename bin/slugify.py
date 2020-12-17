import csv


f = "local-plans/development-plan.csv"
out_file = "local-plans/development-plan-slug.csv"

reader = csv.DictReader(open(f))

out_fields = reader.fieldnames + ["slug"]

writer = csv.DictWriter(open(out_file, "w"), out_fields)
writer.writeheader()

for row in reader:
    row["slug"] = f"local-plan/{row['development-plan']}"
    writer.writerow(row)
