<script lang="ts">
  import { _ } from "svelte-i18n"

  import type { DealVersion2 } from "$lib/types/newtypes"

  import BooleanField from "$components/Fields/Display2/BooleanField.svelte"
  import DecimalField from "$components/Fields/Display2/DecimalField.svelte"
  import JSONJobsField from "$components/Fields/Display2/JSONJobsField.svelte"
  import TextField from "$components/Fields/Display2/TextField.svelte"

  import Subsection from "./Subsection.svelte"

  export let version: DealVersion2
</script>

<section>
  <Subsection
    title={$_("Number of total jobs created")}
    fields={[
      version.total_jobs_created,
      version.total_jobs_planned,
      version.total_jobs_planned_employees,
      version.total_jobs_planned_daily_workers,
      version.total_jobs_current,
      version.total_jobs_created_comment,
    ]}
  >
    <BooleanField
      fieldname="total_jobs_created"
      label={$_("Jobs created (total)")}
      value={version.total_jobs_created}
    />
    <DecimalField
      fieldname="total_jobs_planned"
      label={$_("Planned number of jobs (total)")}
      value={version.total_jobs_planned}
    />
    <DecimalField
      fieldname="total_jobs_planned_employees"
      label={$_("Planned employees (total)")}
      value={version.total_jobs_planned_employees}
    />
    <DecimalField
      fieldname="total_jobs_planned_daily_workers"
      label={$_("Planned daily/seasonal workers (total)")}
      value={version.total_jobs_planned_daily_workers}
    />
    <JSONJobsField
      fieldname="total_jobs_current"
      label={$_("Current total number of jobs/employees/ daily/seasonal workers")}
      value={version.total_jobs_current}
    />
    <TextField
      fieldname="total_jobs_created_comment"
      label={$_("Comment on jobs created (total)")}
      value={version.total_jobs_created_comment}
    />
  </Subsection>

  <Subsection
    title={$_("Number of jobs for foreigners created")}
    fields={[
      version.foreign_jobs_created,
      version.foreign_jobs_planned,
      version.foreign_jobs_planned_employees,
      version.foreign_jobs_planned_daily_workers,
      version.foreign_jobs_current,
      version.foreign_jobs_created_comment,
    ]}
  >
    <BooleanField
      fieldname="foreign_jobs_created"
      label={$_("Jobs created (foreign)")}
      value={version.foreign_jobs_created}
    />
    <DecimalField
      fieldname="foreign_jobs_planned"
      label={$_("Planned number of jobs (foreign)")}
      value={version.foreign_jobs_planned}
    />
    <DecimalField
      fieldname="foreign_jobs_planned_employees"
      label={$_("Planned employees (foreign)")}
      value={version.foreign_jobs_planned_employees}
    />
    <DecimalField
      fieldname="foreign_jobs_planned_daily_workers"
      label={$_("Planned daily/seasonal workers (foreign)")}
      value={version.foreign_jobs_planned_daily_workers}
    />
    <JSONJobsField
      fieldname="foreign_jobs_current"
      label={$_("Current foreign number of jobs/employees/ daily/seasonal workers")}
      value={version.foreign_jobs_current}
    />
    <TextField
      fieldname="foreign_jobs_created_comment"
      label={$_("Comment on jobs created (foreign)")}
      value={version.foreign_jobs_created_comment}
    />
  </Subsection>

  <Subsection
    title={$_("Number of domestic jobs created")}
    fields={[
      version.domestic_jobs_created,
      version.domestic_jobs_planned,
      version.domestic_jobs_planned_employees,
      version.domestic_jobs_planned_daily_workers,
      version.domestic_jobs_current,
      version.domestic_jobs_created_comment,
    ]}
  >
    <BooleanField
      fieldname="domestic_jobs_created"
      label={$_("Jobs created (domestic)")}
      value={version.domestic_jobs_created}
    />
    <DecimalField
      fieldname="domestic_jobs_planned"
      label={$_("Planned number of jobs (domestic)")}
      value={version.domestic_jobs_planned}
    />
    <DecimalField
      fieldname="domestic_jobs_planned_employees"
      label={$_("Planned employees (domestic)")}
      value={version.domestic_jobs_planned_employees}
    />
    <DecimalField
      fieldname="domestic_jobs_planned_daily_workers"
      label={$_("Planned daily/seasonal workers (domestic)")}
      value={version.domestic_jobs_planned_daily_workers}
    />
    <JSONJobsField
      fieldname="domestic_jobs_current"
      label={$_("Current domestic number of jobs/employees/ daily/seasonal workers")}
      value={version.domestic_jobs_current}
    />
    <TextField
      fieldname="domestic_jobs_created_comment"
      label={$_("Comment on jobs created (domestic)")}
      value={version.domestic_jobs_created_comment}
    />
  </Subsection>
</section>
