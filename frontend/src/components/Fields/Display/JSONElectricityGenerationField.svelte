<script lang="ts">
  import { _ } from "svelte-i18n"

  import { dateCurrentFormat } from "$components/Fields/Display/jsonHelpers"
  import type { FormField } from "$components/Fields/fields"
  import CircleNotchIcon from "$components/icons/CircleNotchIcon.svelte"
  import PlaneIcon from "$components/icons/PlaneIcon.svelte"
  import RenewableEnergyIcon from "$components/icons/RenewableEnergyIcon.svelte"

  interface JSONElectricityGenerationField {
    current?: boolean
    date?: string
    area?: number
    choices?: string[]
    export?: number
    windfarm_count?: number
    current_capacity?: number
    intended_capacity?: number
  }

  export let formfield: FormField
  export let value: JSONElectricityGenerationField[] = []
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
        <span class="mx-2">
          <CircleNotchIcon />
          {val.area.toLocaleString("fr")}
          {$_("ha")}
        </span>
      {/if}
      {#if val.export}
        <span class="mx-2">
          <PlaneIcon />
          {val.export.toLocaleString("fr")} %
        </span>
      {/if}
      <br />
      {#if val.windfarm_count}
        <span class="mr-2">
          <RenewableEnergyIcon />
          {$_("Number of turbines")}:
          {val.windfarm_count}
        </span>
      {/if}
      {#if val.current_capacity}
        <span class="mx-2">
          {$_("Currently installed capacity")}: {val.current_capacity.toLocaleString(
            "fr",
          )}
          {$_("MW")}
        </span>
      {/if}
      {#if val.intended_capacity}
        <span class="mx-2">
          {$_("Intended capacity")}: {val.intended_capacity.toLocaleString("fr")}
          {$_("MW")}
        </span>
      {/if}
    </li>
  {/each}
</ul>
