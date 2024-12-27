<script lang="ts">
  import { _ } from "svelte-i18n"

  import type { components } from "$lib/openAPI"
  import { fieldChoices } from "$lib/stores"

  import { dateCurrentFormatStartEnd } from "$components/Fields/Display2/jsonHelpers"
  import CircleNotchIcon from "$components/icons/CircleNotchIcon.svelte"

  interface Props {
    value?: components["schemas"]["CarbonSequestrationItem"][]
  }

  let { value = [] }: Props = $props()

  const getLabel = (value: string) =>
    $fieldChoices.deal.carbon_sequestration.find(c => value === c.value)?.label ?? value
</script>

<ul class="flex flex-col gap-2">
  {#each value ?? [] as val}
    <li class:font-bold={val.current}>
      <span>{dateCurrentFormatStartEnd(val)}</span>
      {#if val.choices && $fieldChoices.deal.carbon_sequestration.length}
        <span>
          {val.choices.map(getLabel).join(", ")}
        </span>
      {/if}
      {#if val.area}
        (<CircleNotchIcon />
        {val.area.toLocaleString("fr").replace(",", ".")}
        {$_("ha")})
      {/if}
      {#if val.projected_lifetime_sequestration}
        <div>
          {$_("Estimated emission reduction/removal during project lifetime")}:
          {val.projected_lifetime_sequestration.toLocaleString("fr").replace(",", ".")}
          {$_("tCO2e")}
        </div>
      {/if}
      {#if val.projected_annual_sequestration}
        <div>
          {$_("Estimated annual emission reduction/removal")}:
          {val.projected_annual_sequestration.toLocaleString("fr").replace(",", ".")}
          {$_("tCO2e")}
        </div>
      {/if}
      {#if val.project_proponents}
        <div>
          {$_("Project proponents")}:
          {val.project_proponents}
        </div>
      {/if}

      <div class="mr-2 italic">
        {$_("Certification standard")}:
        {#if val.certification_standard}
          {$_("Yes")}
        {:else if val.certification_standard === false}
          {$_("No")}
        {:else}
          "--"
        {/if}
      </div>
      {#if val.certification_standard}
        {#if val.certification_standard_name}
          <div class="mr-2">
            {$_("Name of certification standard/mechanism")}:
            {#each val.certification_standard_name as cert_name}
              {$fieldChoices.deal.carbon_sequestration_certs.find(
                i => i.value === cert_name,
              )?.label ?? "--"}
            {/each}
          </div>
        {/if}
        {#if val.certification_standard_id}
          <div class="mr-2">
            {$_("ID of certification standard/mechanism")}:
            {val.certification_standard_id}
          </div>
        {/if}
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
