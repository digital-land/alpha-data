#! /usr/bin/env python

import csv
import copy
import hashlib

fieldnames = [
    "development-plan",
    "name",
    "development-plan-type",
    "organisations",
    "geographies",
    "notes",
    "description",
    "end-date",
    "entry-date",
    "start-date",
]

f = open("./local-plan-data.csv")
reader = csv.DictReader(f)

plans = {}
documents = {}
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


def hash_(value):
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


# replace old form of national park identifiers with their digital land version
# e.g. government-organisation:OT543 ==> national-park-authority:Q72617890 
def create_organisation_id_mapper():
    mapper = {}
    f = open("./patch/national-park-authority.csv")
    reader = csv.DictReader(f)
    for row in reader:
        if row.get("government-organisation") and row.get("national-park-authority"):
            mapper[f"government-organisation:{row['government-organisation']}"] = f"national-park-authority:{row['national-park-authority']}" 
    return mapper

id_mapper = create_organisation_id_mapper()


for row in reader:
    plan = plans.setdefault(row["plan_id"], dict())

    plan["development-plan"] = row["plan_id"]
    plan["development-plan-type"] = "local-plan"

    check_add(plan, "name", row["plan_title"])
    check_add(plan, "start-date", row["adopted"])
    check_add(plan, "notes", row["notes"])

    check_add(plan, "submitted", row["submitted"])
    check_add(plan, "published", row["published"])
    check_add(plan, "sound", row["found_sound"])
    check_add(plan, "adopted", row["adopted"])

    document_key = hash_(":".join([row["plan_id"], row["planning_authority"]]))
    documents[document_key] = copy.deepcopy(plan)
    documents[document_key]["development-plan-document"] = document_key
    documents[document_key]["organisation"] = id_mapper.get(row["planning_authority"], row["planning_authority"])
    documents[document_key]["document-url"] = row["source_document"]

    # build list of all geographies that this plan applies to
    geographies = plan.setdefault("geographies", [])
    geographies.append(f"statistical-geography:{row['ons_code']}")

    # build list of all orgs that this plan applies to
    organisations = plan.setdefault("organisations", [])
    organisations.append(id_mapper.get(row["planning_authority"], row["planning_authority"]))

f.close()

writer = csv.DictWriter(
    open("./development-plan.csv", "w"), fieldnames, extrasaction="ignore"
)
writer.writeheader()

for plan in plans.values():
    plan["organisations"] = ";".join(plan["organisations"])
    plan["geographies"] = ";".join(plan["geographies"])
    writer.writerow(plan)


document_fieldnames = [
    "development-plan-document",
    "description",
    "development-plan",
    "development-policies",
    "document-url",
    "name",
    "notes",
    "organisation",
    "entry-date",
    "start-date",
    "end-date",
]

writer = csv.DictWriter(
    open("./development-plan-document.csv", "w"),
    document_fieldnames,
    extrasaction="ignore",
)
writer.writeheader()

for document in documents.values():
    writer.writerow(document)


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
            timetable_writer.writerow(
                {
                    "development-plan": plan["development-plan"],
                    "development-plan-status": status,
                    "end-date": plan[status],
                    "entry-date": "2020-07-13",
                }
            )

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
        {"development-plan-status": status, "name": status,}
    )
