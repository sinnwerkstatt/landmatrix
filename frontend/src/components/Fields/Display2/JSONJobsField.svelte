<script lang="ts">
  import { _ } from "svelte-i18n"

  import type { JSONJobsFieldType } from "$lib/types/newtypes"

  import { dateCurrentFormat } from "$components/Fields/Display2/jsonHelpers"

  export let value: JSONJobsFieldType[]
</script>

<ul>
  {#each value as val}
    <li class:font-bold={val.current}>
      {dateCurrentFormat(val)}
      {#if val.jobs}
        <span class="mx-2">
          {val.jobs.toLocaleString("fr")}
          {$_("jobs")}
        </span>
      {/if}
      {#if val.employees}
        <span class="mx-2">
          {val.employees.toLocaleString("fr")}
          {$_("employees")}
        </span>
      {/if}
      {#if val.workers}
        <span class="mx-2">
          {val.workers.toLocaleString("fr")}
          {$_("workers")}
        </span>
      {/if}
    </li>
  {/each}
</ul>
