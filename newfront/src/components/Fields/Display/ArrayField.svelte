<script lang="ts">
  import { _ } from "svelte-i18n"

  import { flat_intention_of_investment_map } from "$lib/choices"

  import type { FormField } from "$components/Fields/fields"
  import AgricultureIcon from "$components/icons/AgricultureIcon.svelte"
  import FoodCropsIcon from "$components/icons/FoodCropsIcon.svelte"
  import ForestIcon from "$components/icons/ForestIcon.svelte"
  import IndustryIcon from "$components/icons/IndustryIcon.svelte"
  import LandSpeculationIcon from "$components/icons/LandSpeculationIcon.svelte"
  import LifestockIcon from "$components/icons/LifestockIcon.svelte"
  import MiningIcon from "$components/icons/MiningIcon.svelte"
  import OilIcon from "$components/icons/OilIcon.svelte"
  import PlaneIcon from "$components/icons/PlaneIcon.svelte"
  import RenewableEnergyIcon from "$components/icons/RenewableEnergyIcon.svelte"

  export let value: string[]
  export let formfield: FormField

  const intention_of_investment_map = {
    BIOFUELS: AgricultureIcon,
    FOOD_CROPS: FoodCropsIcon,
    FODDER: FoodCropsIcon,
    LIVESTOCK: LifestockIcon,
    NON_FOOD_AGRICULTURE: AgricultureIcon,
    AGRICULTURE_UNSPECIFIED: AgricultureIcon,
    TIMBER_PLANTATION: ForestIcon,
    FOREST_LOGGING: ForestIcon,
    CARBON: ForestIcon,
    FORESTRY_UNSPECIFIED: ForestIcon,
    MINING: MiningIcon,
    OIL_GAS_EXTRACTION: OilIcon,
    TOURISM: PlaneIcon,
    INDUSTRY: IndustryIcon,
    CONVERSATION: null,
    LAND_SPECULATION: LandSpeculationIcon,
    RENEWABLE_ENERGY: RenewableEnergyIcon,
    OTHER: null,
  }

  export function parseValues(value) {
    if (!value) return "—"
    if (Object.keys(formfield.choices).length > 0)
      return value.map(v => formfield.choices?.[v]).join(", ")
    return value.join(", ")
  }
</script>

<div class="array_field" data-name={formfield?.name ?? ""}>
  {#if formfield?.name === "current_intention_of_investment"}
    {#each value ?? [] as ioi}
      <span
        class="mx-1 my-0.5 inline-flex items-center gap-1 whitespace-nowrap border border-black/10 bg-black/5 px-1 py-0.5 text-gray-900"
      >
        {#if intention_of_investment_map[ioi] != null}
          <svelte:component this={intention_of_investment_map[ioi]} />
        {/if}
        {$_(flat_intention_of_investment_map[ioi])}
      </span>
    {/each}
  {:else}
    {parseValues(value)}
  {/if}
</div>
