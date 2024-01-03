<script lang="ts">
  import { _ } from "svelte-i18n"

  import type { InvestorHull } from "$lib/types/newtypes"

  import { LABEL_CLASS, VALUE_CLASS, WRAPPER_CLASS } from "$components/Fields/consts"
  import Label2 from "$components/Fields/Display2/Label2.svelte"

  export let value: InvestorHull | null
  export let fieldname: string
  export let label = ""
  export let wrapperClass = WRAPPER_CLASS
  export let labelClass = LABEL_CLASS
  export let valueClass = VALUE_CLASS
</script>

{#if value}
  <div class={wrapperClass} data-fieldname={fieldname}>
    {#if label}
      <Label2 value={label} class={labelClass} />
    {/if}
    <div class={valueClass}>
      <a href="/investor/{value.id}/">
        {#if value.selected_version.name_unknown}
          <span class="italic">[{$_("unknown investor")}]</span>
        {:else}
          {value.selected_version.name}
        {/if}
        #{value.id}
        {#if value.selected_version.country}
          - {value.selected_version.country.name}
        {/if}
      </a>
    </div>
  </div>
{/if}
