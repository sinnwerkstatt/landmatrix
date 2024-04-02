<script lang="ts">
  import { _ } from "svelte-i18n"

  import { fieldChoices } from "$lib/stores"
  import type { JSONCarbonSequestrationFieldType } from "$lib/types/newtypes"

  import { dateCurrentFormat } from "$components/Fields/Display2/jsonHelpers"
  import CircleNotchIcon from "$components/icons/CircleNotchIcon.svelte"

  export let value: JSONCarbonSequestrationFieldType[] = []

  const getLabel = (value: string) =>
    $fieldChoices.deal.carbon_sequestration.find(c => value === c.value)?.label ?? value
</script>

<ul>
  {#each value ?? [] as val}
    <li class:font-bold={val.current}>
      <span>{dateCurrentFormat(val)}</span>
      {#if val.choices && $fieldChoices.deal.carbon_sequestration.length}
        <span>
          {val.choices.map(getLabel).join(", ")}
        </span>
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

      <div class="mr-2">
        {$_("Certification standard")}: {#if val.certification_standard}
          {$_("Yes")}{:else if val.certification_standard === false}
          {$_("No")}{:else}—{/if}
      </div>
      {#if val.certification_standard_name}
        <div class="mr-2">
          {$_("Name of certification standard")}:
          {$fieldChoices.deal.carbon_sequestration_certs.find(
            i => i.value === val.certification_standard_name,
          )?.label ?? "--"}
        </div>
      {/if}
      {#if val.certification_standard_id}
        <div class="mr-2">
          {$_("ID of certification standard/mechanism")}:
          {val.certification_standard_id}
        </div>
      {/if}
      {#if val.certification_standard_comment}
        <div>
          {$_("Comment on certification standard / mechanism")}:
          {val.certification_standard_comment}
        </div>
      {/if}
    </li>
  {/each}
</ul>
