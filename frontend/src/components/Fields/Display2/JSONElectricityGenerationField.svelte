<script lang="ts">
  import { _ } from "svelte-i18n"

  import { dealChoices } from "$lib/fieldChoices"
  import type { JSONElectricityGenerationFieldType } from "$lib/types/data"

  import { dateCurrentFormat } from "$components/Fields/Display2/jsonHelpers"
  import CircleNotchIcon from "$components/icons/CircleNotchIcon.svelte"
  import PlaneIcon from "$components/icons/PlaneIcon.svelte"
  import RenewableEnergyIcon from "$components/icons/RenewableEnergyIcon.svelte"
  import SourcesDisplayButton from "$components/Quotations/SourcesDisplayButton.svelte"

  interface Props {
    value?: JSONElectricityGenerationFieldType[]
    fieldname?: string
  }

  let { value = [], fieldname = "" }: Props = $props()

  const getLabel = (value: string) =>
    $dealChoices.electricity_generation.find(c => value === c.value)?.label ?? value
</script>

<ul>
  {#each value ?? [] as val, i}
    <li class:font-bold={val.current}>
      <span>{dateCurrentFormat(val)}</span>

      {#if val.choices && $dealChoices.electricity_generation.length}
        <span>
          {val.choices.map(getLabel).join(", ")}
        </span>
      {/if}

      {#if val.area}
        <span class="mx-2">
          <CircleNotchIcon />
          {val.area.toLocaleString("fr").replace(",", ".")}
          {$_("ha")}
        </span>
      {/if}
      {#if val.export}
        <span class="mx-2">
          <PlaneIcon />
          {val.export.toLocaleString("fr").replace(",", ".")} %
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
          {$_("Intended capacity")}: {val.intended_capacity
            .toLocaleString("fr")
            .replace(",", ".")}
          {$_("MW")}
        </span>
      {/if}

      <SourcesDisplayButton path={[fieldname, i]} />
    </li>
  {/each}
</ul>
