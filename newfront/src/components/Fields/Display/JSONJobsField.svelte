<script lang="ts">
  import {
    date_and_current,
    JSONJobsFieldType,
  } from "$components/Fields/Display/jsonHelpers.ts";

  export let value: JSONJobsFieldType[] = [];
</script>

<div class="jsonjobs_field whitespace-nowrap">
  {#each value as val}
    <div class:font-bold={val.current}>
      {date_and_current(val)}
      {#if val.jobs}
        <span class="mx-2">
          {val.jobs.toLocaleString("fr")} jobs
        </span>
      {/if}{#if val.employees}
        <span class="mx-2">
          {val.employees.toLocaleString("fr")} employees
        </span>
      {/if}{#if val.workers}
        <span class="mx-2">
          {val.workers.toLocaleString("fr")} workers
        </span>
      {/if}
    </div>
  {/each}
</div>
