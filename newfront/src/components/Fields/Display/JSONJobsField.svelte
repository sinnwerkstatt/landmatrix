<script lang="ts">
  import { _ } from "svelte-i18n";
  import { dateCurrentFormat } from "$components/Fields/Display/jsonHelpers";

  type JSONJobsFieldType = {
    current?: boolean;
    date: string;
    jobs?: string;
    employees?: string;
    workers?: string;
    choices?: Array<{ [key: string]: string }>;
  };

  export let value: JSONJobsFieldType[] = [];
</script>

<div class="jsonjobs_field whitespace-nowrap">
  {#each value as val}
    <div class:font-bold={val.current}>
      {dateCurrentFormat(val)}
      {#if val.jobs}
        <span class="mx-2">
          {val.jobs.toLocaleString("fr")}
          {$_("jobs")}
        </span>
      {/if}{#if val.employees}
        <span class="mx-2">
          {val.employees.toLocaleString("fr")}
          {$_("employees")}
        </span>
      {/if}{#if val.workers}
        <span class="mx-2">
          {val.workers.toLocaleString("fr")}
          {$_("workers")}
        </span>
      {/if}
    </div>
  {/each}
</div>
