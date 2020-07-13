#! /usr/bin/env python

import csv
import hashlib

fieldnames = [
    "description",
    "development-plan",
    "development-plan-type",
    "development-policies",
    "geographies",
    "name",
    "notes",
    "organisations",
    "end-date",
    "entry-date",
    "start-date",
    "document-url",
]

f = open("./local-plan-data.csv")
reader = csv.DictReader(f)

plans = {}
timetables = {}

def check_add(plan, field, value):
    if field not in plan:
        plan[field] = value
        return

    if plan[field] != value:
        raise ValueError(
            "value '%s' for field %s does not match existing '%s'"
            % (value, field, plan[field])
        )


for row in reader:
    plan = plans.setdefault(row["plan_id"], dict())

    plan["development-plan"] = row["plan_id"]
    plan["development-plan-type"] = "local-plan"

    check_add(plan, "name", row["plan_title"])
    check_add(plan, "start-date", row["adopted"])
    check_add(plan, "document-url", row["source_document"])
    check_add(plan, "notes", row["notes"])

    check_add(plan, "submitted", row["submitted"])
    check_add(plan, "published", row["published"])
    check_add(plan, "sound", row["found_sound"])
    check_add(plan, "adopted", row["adopted"])

    geographies = plan.setdefault("geographies", [])
    geographies.append(f"statistical-geography:{row['ons_code']}")

    # build list of all orgs that this plan applies to
    organisations = plan.setdefault("organisations", [])
    organisations.append(row["planning_authority"])

f.close()

writer = csv.DictWriter(
    open("./development-plan.csv", "w"), fieldnames, extrasaction="ignore"
)
writer.writeheader()

for plan in plans.values():
    plan["organisations"] = ";".join(plan["organisations"])
    plan["geographies"] = ";".join(plan["geographies"])
    writer.writerow(plan)


timetable_fieldnames = [
    "development-plan",
    "development-plan-status",
    "notes",
    "end-date",
    "entry-date",
    "start-date",
]

timetable_writer = csv.DictWriter(
    open("./development-plan-timetable.csv", "w"), timetable_fieldnames
)
timetable_writer.writeheader()

for plan in plans.values():
    for status in ["submitted", "published", "sound", "adopted"]:
        if plan[status]:
            timetable_writer.writerow({
                "development-plan": plan["development-plan"],
                "development-plan-status": status,
                "end-date": plan[status],
                "entry-date": "2020-07-13",
            })

status_fieldnames = [
    "development-plan-status",
    "name",
    "end-date",
    "entry-date",
    "start-date",
]

status_writer = csv.DictWriter(
    open("./development-plan-status.csv", "w"), status_fieldnames
)
status_writer.writeheader()

for status in ["submitted", "published", "sound", "adopted"]:
    status_writer.writerow(
        {
            "development-plan-status": status,
            "name": status,
        }
    )

# def hash(value):
#     return hashlib.sha256(value.encode("utf-8")).hexdigest()
