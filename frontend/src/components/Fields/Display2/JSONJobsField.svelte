<script lang="ts">
  import { _ } from "svelte-i18n"

  import type { JSONJobsFieldType } from "$lib/types/newtypes"

  import { dateCurrentFormat } from "$components/Fields/Display/jsonHelpers"
  import Label2 from "$components/Fields/Display2/Label2.svelte"

  export let value: JSONJobsFieldType = []

  export let fieldname: string
  export let label = ""
  export let wrapperClass = "mb-3 flex flex-wrap leading-5"
  export let labelClass = "md:w-5/12 lg:w-4/12"
  export let valueClass = "text-lm-dark dark:text-white md:w-7/12 lg:w-8/12"
</script>

{#if value?.length > 0}
  <div class={wrapperClass} data-fieldname={fieldname}>
    {#if label}
      <Label2 value={label} class={labelClass} />
    {/if}
    <div class={valueClass}>
      <ul>
        {#each value ?? [] as val}
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
    </div>
  </div>
{/if}
