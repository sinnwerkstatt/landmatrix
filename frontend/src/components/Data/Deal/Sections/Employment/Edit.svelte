<script lang="ts">
  import { slide } from "svelte/transition"

  import type { DealHull } from "$lib/types/data"

  import EditSubsection from "$components/Data/EditSubsection.svelte"
  import EditField from "$components/Fields/EditField.svelte"

  interface Props {
    deal: DealHull
  }

  let { deal = $bindable() }: Props = $props()
</script>

<form id="employment" class="pb-52">
  <EditSubsection id="total_jobs_created">
    <EditField
      fieldname="total_jobs_created"
      showLabel
      bind:value={deal.selected_version.total_jobs_created}
    />
    {#if deal.selected_version.total_jobs_created === true}
      <div class="pl-4" transition:slide={{ duration: 300 }}>
        <EditField
          fieldname="total_jobs_planned"
          showLabel
          bind:value={deal.selected_version.total_jobs_planned}
        />
        <EditField
          fieldname="total_jobs_planned_employees"
          showLabel
          bind:value={deal.selected_version.total_jobs_planned_employees}
        />
        <EditField
          fieldname="total_jobs_planned_daily_workers"
          showLabel
          bind:value={deal.selected_version.total_jobs_planned_daily_workers}
        />
        <EditField
          fieldname="total_jobs_current"
          showLabel
          bind:value={deal.selected_version.total_jobs_current}
        />
      </div>
    {/if}
    <EditField
      fieldname="total_jobs_created_comment"
      showLabel
      bind:value={deal.selected_version.total_jobs_created_comment}
    />
  </EditSubsection>

  <EditSubsection id="foreign_jobs_created">
    <EditField
      fieldname="foreign_jobs_created"
      showLabel
      bind:value={deal.selected_version.foreign_jobs_created}
    />
    {#if deal.selected_version.foreign_jobs_created === true}
      <div class="pl-4" transition:slide={{ duration: 300 }}>
        <EditField
          fieldname="foreign_jobs_planned"
          showLabel
          bind:value={deal.selected_version.foreign_jobs_planned}
        />
        <EditField
          fieldname="foreign_jobs_planned_employees"
          showLabel
          bind:value={deal.selected_version.foreign_jobs_planned_employees}
        />
        <EditField
          fieldname="foreign_jobs_planned_daily_workers"
          showLabel
          bind:value={deal.selected_version.foreign_jobs_planned_daily_workers}
        />
        <EditField
          fieldname="foreign_jobs_current"
          showLabel
          bind:value={deal.selected_version.foreign_jobs_current}
        />
      </div>
    {/if}
    <EditField
      fieldname="foreign_jobs_created_comment"
      showLabel
      bind:value={deal.selected_version.foreign_jobs_created_comment}
    />
  </EditSubsection>

  <EditSubsection id="domestic_jobs_created">
    <EditField
      fieldname="domestic_jobs_created"
      showLabel
      bind:value={deal.selected_version.domestic_jobs_created}
    />
    {#if deal.selected_version.domestic_jobs_created === true}
      <div class="pl-4" transition:slide={{ duration: 300 }}>
        <EditField
          fieldname="domestic_jobs_planned"
          showLabel
          bind:value={deal.selected_version.domestic_jobs_planned}
        />
        <EditField
          fieldname="domestic_jobs_planned_employees"
          showLabel
          bind:value={deal.selected_version.domestic_jobs_planned_employees}
        />
        <EditField
          fieldname="domestic_jobs_planned_daily_workers"
          showLabel
          bind:value={deal.selected_version.domestic_jobs_planned_daily_workers}
        />
        <EditField
          fieldname="domestic_jobs_current"
          showLabel
          bind:value={deal.selected_version.domestic_jobs_current}
        />
      </div>
    {/if}
    <EditField
      fieldname="domestic_jobs_created_comment"
      showLabel
      bind:value={deal.selected_version.domestic_jobs_created_comment}
    />
  </EditSubsection>
</form>
