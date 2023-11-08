<script lang="ts">
  import { _ } from "svelte-i18n"

  import { dateCurrentFormat } from "$components/Fields/Display/jsonHelpers"
  import type { FormField } from "$components/Fields/fields"
  import CircleNotchIcon from "$components/icons/CircleNotchIcon.svelte"

  interface JSONCarbonSequestrationField {
    current?: boolean
    date?: string
    area?: number
    choices?: string[]
    projected_lifetime_sequestration?: number
    projected_annual_sequestration?: number
    certification_standard: boolean | null
    certification_standard_name: string
    certification_standard_comment: string
  }

  export let formfield: FormField
  export let value: JSONCarbonSequestrationField[] = []
</script>

<ul>
  {#each value ?? [] as val}
    <li class:font-bold={val.current}>
      <span>{dateCurrentFormat(val)}</span>
      {#if val.choices}
        <!-- The literal translation strings are defined in apps/landmatrix/models/choices.py -->
        {val.choices.map(v => $_(formfield.choices[v])).join(", ")}
      {/if}
      {#if val.area}
        (<CircleNotchIcon /> {val.area.toLocaleString("fr")} {$_("ha")})
      {/if}
      {#if val.projected_lifetime_sequestration}
        <div>
          {$_("Projected carbon sequestration during project lifetime")}:
          {val.projected_lifetime_sequestration.toLocaleString("fr")}
          {$_("tCO2e")}
        </div>
      {/if}
      {#if val.projected_annual_sequestration}
        <div>
          {$_("Projected annual carbon sequestration")}:
          {val.projected_annual_sequestration.toLocaleString("fr")}
          {$_("tCO2e")}
        </div>
      {/if}

      <span class="mr-2">
        {$_("Certification standard")}: {#if val.certification_standard}
          {$_("Yes")}{:else if val.certification_standard === false}
          {$_("No")}{:else}—{/if}
      </span>
      {#if val.certification_standard_name}
        <span class="mr-2">
          {$_("Name of certification standard")}:
          {val.certification_standard_name}
        </span>
      {/if}
      {#if val.certification_standard_comment}
        <div>
          {$_("Comment on certification standard")}:
          {val.certification_standard_comment}
        </div>
      {/if}
    </li>
  {/each}
</ul>
