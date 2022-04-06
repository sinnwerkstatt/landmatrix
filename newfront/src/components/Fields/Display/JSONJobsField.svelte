<script lang="ts">
  import { date_and_current } from "$components/Fields/Display/jsonHelpers.ts";

  export let value: boolean;
  let vals = value ? value : [{ name: null, role: null }];
</script>

<div class="jsonjobs_field whitespace-nowrap">
  {#each vals as val}
    <div class={() => (val.current ? "font-bold" : "")}>
      <span>{date_and_current(val)}</span>
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
