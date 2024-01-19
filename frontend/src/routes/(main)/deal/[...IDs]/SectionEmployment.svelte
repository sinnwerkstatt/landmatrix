<script lang="ts">
  import type { DealVersion2 } from "$lib/types/newtypes"

  import DisplayField from "$components/Fields/DisplayField.svelte"

  import Subsection from "./Subsection.svelte"

  export let version: DealVersion2
</script>

<section>
  <Subsection id="total_jobs_created" obj={version}>
    <DisplayField
      fieldname="total_jobs_created"
      showLabel
      value={version.total_jobs_created}
    />
    <DisplayField
      fieldname="total_jobs_planned"
      showLabel
      value={version.total_jobs_planned}
    />
    <DisplayField
      fieldname="total_jobs_planned_employees"
      showLabel
      value={version.total_jobs_planned_employees}
    />
    <DisplayField
      fieldname="total_jobs_planned_daily_workers"
      showLabel
      value={version.total_jobs_planned_daily_workers}
    />
    <DisplayField
      fieldname="total_jobs_current"
      showLabel
      value={version.total_jobs_current}
    />
    <DisplayField
      fieldname="total_jobs_created_comment"
      showLabel
      value={version.total_jobs_created_comment}
    />
  </Subsection>

  <Subsection id="foreign_jobs_created" obj={version}>
    <DisplayField
      fieldname="foreign_jobs_created"
      showLabel
      value={version.foreign_jobs_created}
    />
    <DisplayField
      fieldname="foreign_jobs_planned"
      showLabel
      value={version.foreign_jobs_planned}
    />
    <DisplayField
      fieldname="foreign_jobs_planned_employees"
      showLabel
      value={version.foreign_jobs_planned_employees}
    />
    <DisplayField
      fieldname="foreign_jobs_planned_daily_workers"
      showLabel
      value={version.foreign_jobs_planned_daily_workers}
    />
    <DisplayField
      fieldname="foreign_jobs_current"
      showLabel
      value={version.foreign_jobs_current}
    />
    <DisplayField
      fieldname="foreign_jobs_created_comment"
      showLabel
      value={version.foreign_jobs_created_comment}
    />
  </Subsection>

  <Subsection id="domestic_jobs_created" obj={version}>
    <DisplayField
      fieldname="domestic_jobs_created"
      showLabel
      value={version.domestic_jobs_created}
    />
    <DisplayField
      fieldname="domestic_jobs_planned"
      showLabel
      value={version.domestic_jobs_planned}
    />
    <DisplayField
      fieldname="domestic_jobs_planned_employees"
      showLabel
      value={version.domestic_jobs_planned_employees}
    />
    <DisplayField
      fieldname="domestic_jobs_planned_daily_workers"
      showLabel
      value={version.domestic_jobs_planned_daily_workers}
    />
    <DisplayField
      fieldname="domestic_jobs_current"
      showLabel
      value={version.domestic_jobs_current}
    />
    <DisplayField
      fieldname="domestic_jobs_created_comment"
      showLabel
      value={version.domestic_jobs_created_comment}
    />
  </Subsection>
</section>
