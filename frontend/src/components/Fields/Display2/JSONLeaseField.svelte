<script lang="ts">
  import { _ } from "svelte-i18n"

  import type { JSONLeaseFieldType } from "$lib/types/newtypes"

  import { dateCurrentFormat } from "$components/Fields/Display/jsonHelpers"
  import Label2 from "$components/Fields/Display2/Label2.svelte"
  import CircleNotchIcon from "$components/icons/CircleNotchIcon.svelte"
  import HouseholdIcon from "$components/icons/HouseholdIcon.svelte"
  import TractorIcon from "$components/icons/TractorIcon.svelte"

  export let value: JSONLeaseFieldType = []

  export let fieldname: string
  export let label = ""
  export let wrapperClass = "mb-3 flex flex-wrap leading-5"
  export let labelClass = "md:w-5/12 lg:w-4/12"
  export let valueClass = "text-gray-700 dark:text-white md:w-7/12 lg:w-8/12"
</script>

{#if value}
  <div class={wrapperClass} data-fieldname={fieldname}>
    {#if label}
      <Label2 value={label} class={labelClass} />
    {/if}
    <div class={valueClass}>
      <ul>
        {#each value ?? [] as val}
          <li class:font-bold={val.current}>
            <span>{dateCurrentFormat(val)}</span>
            {#if val.area}
              <span class="mx-2">
                <CircleNotchIcon />
                {val.area.toLocaleString("fr")}
                {$_("ha")}
              </span>
            {/if}
            {#if val.farmers}
              <span class="mx-2">
                <TractorIcon />
                {val.farmers.toLocaleString("fr")}
              </span>
            {/if}
            {#if val.households}
              <span class="mx-2">
                <HouseholdIcon />
                {val.households.toLocaleString("fr")}
              </span>
            {/if}
          </li>
        {/each}
      </ul>
    </div>
  </div>
{/if}
