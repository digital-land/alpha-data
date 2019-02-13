# Local plans

This is a placeholder register created from a list published by the Planning Inspectorate
[here](https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/777040/LPA_Strategic_Plan_Progress_-_1_February_2019._GOV.UK.pdf)

### Register description

Each row in the file represents the local plan of a planning authority at a specific status showing the progress of the plan from publication through to adoption.

The plan can be in one of the following states:

    published|submitted|validated|adopted|updated

Where these states map to the headings in the original document as follows:

    Last Updated = updated
    Published = published
    Submitted = submitted
    Found Sound = validated
    Adopted = adopted


The fields in this register are:

    entry-number
    local-plan
    organisation
    name
    status
    plan-policy-url
    plan-document-url
    date
    entry-date

**These field names are of course work in progress**

**Note: it seems that plans can be comprised of many documents therefore we'll probably move the plan document url into its own list at some point**


### Field descriptions

| field       | description|
| ------------- |-------------|
| entry-number | Sequential number when record added to register |
| local-plan | Identifier for local plan. The status changes in the plan require new entries which share this identifier |
| organisation | The planning authority publishing the plan. Identifiers should eventually come from organisation register |
| name | planning authority name|
| status | The status of the plan as one of published, submitted, accepted, adopted, updated |
| plan-policy-url | Main page on planning authority with links to local plan documents |
| plan-document-url | The url of a specific planning document |
| date | The date on which the plan reached the given status |
| entry-date | The date this row/record was written to the register |
