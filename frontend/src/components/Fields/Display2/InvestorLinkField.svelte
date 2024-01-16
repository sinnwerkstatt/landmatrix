<script lang="ts">
  import { onMount } from "svelte"
  import { _ } from "svelte-i18n"

  import type { InvestorHull } from "$lib/types/newtypes"

  import { LABEL_CLASS, VALUE_CLASS, WRAPPER_CLASS } from "$components/Fields/consts"
  import Label2 from "$components/Fields/Display2/Label2.svelte"

  export let value: InvestorHull | number | null
  export let fieldname: string
  export let label = ""
  export let wrapperClass = WRAPPER_CLASS
  export let labelClass = LABEL_CLASS
  export let valueClass = VALUE_CLASS

  let investor: InvestorHull | null
  async function fetchInvestor() {
    if (value === null) return
    if (typeof value === "number") {
      const ret = await fetch(`/api/investors/${value}/`)
      investor = await ret.json()
    } else {
      investor = value
    }
  }
  onMount(() => {
    fetchInvestor()
  })
</script>

{#if investor}
  <div class={wrapperClass} data-fieldname={fieldname}>
    {#if label}
      <Label2 value={label} class={labelClass} />
    {/if}
    <div class={valueClass}>
      <a href="/investor/{investor.id}/">
        {#if investor.selected_version.name_unknown}
          <span class="italic">[{$_("unknown investor")}]</span>
        {:else}
          {investor.selected_version.name}
        {/if}
        #{investor.id}
        {#if investor.selected_version.country}
          - {investor.selected_version.country.name}
        {/if}
      </a>
    </div>
  </div>
{/if}
