<script lang="ts">
  import { _ } from "svelte-i18n"

  import type { JSONJobsFieldType } from "$lib/types/data"

  import { dateCurrentFormat } from "$components/Fields/Display2/jsonHelpers"
  import SourcesDisplayButton from "$components/Quotations/SourcesDisplayButton.svelte"

  interface Props {
    value: JSONJobsFieldType[]
    fieldname?: string
  }

  let { value, fieldname = "" }: Props = $props()
</script>

<ul>
  {#each value ?? [] as val, i}
    <li class:font-bold={val.current}>
      {dateCurrentFormat(val)}
      {#if val.jobs}
        <span class="mx-2">
          {val.jobs.toLocaleString("fr").replace(",", ".")}
          {$_("jobs")}
        </span>
      {/if}
      {#if val.employees}
        <span class="mx-2">
          {val.employees.toLocaleString("fr").replace(",", ".")}
          {$_("employees")}
        </span>
      {/if}
      {#if val.workers}
        <span class="mx-2">
          {val.workers.toLocaleString("fr").replace(",", ".")}
          {$_("workers")}
        </span>
      {/if}

      <SourcesDisplayButton path={[fieldname, i]} />
    </li>
  {/each}
</ul>
