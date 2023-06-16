<script lang="ts">
  import { _ } from "svelte-i18n"

  import { dateCurrentFormat } from "$components/Fields/Display/jsonHelpers"
  import type { FormField } from "$components/Fields/fields"

  type JSONJobsFieldType = {
    current?: boolean
    date: string
    jobs?: string
    employees?: string
    workers?: string
    choices?: Array<{ [key: string]: string }>
  }

  export let formfield: FormField
  export let value: JSONJobsFieldType[] = []
</script>

<ul>
  {#each value ?? [] as val}
    <li class:font-bold={val.current}>
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
    </li>
  {/each}
</ul>
