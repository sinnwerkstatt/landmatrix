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
  import SolarPanelIcon from "$components/icons/SolarPanelIcon.svelte"

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
    SOLAR_PARK: SolarPanelIcon,
    WIND_FARM: RenewableEnergyIcon,
    RENEWABLE_ENERGY: RenewableEnergyIcon,
    OTHER: null,
  }

  const parseValues = (value: string[], choices?: Record<string, string>) => {
    if (!value) return "—"
    // The literal translation strings are defined in apps/landmatrix/models/choices.py
    if (choices) return value.map(v => $_(choices[v])).join(", ")
    return value.join(", ")
  }
</script>

{#if formfield?.name === "current_intention_of_investment"}
  {#each value ?? [] as ioi}
    <span
      class="mx-1 my-0.5 inline-flex items-center gap-1 whitespace-nowrap border border-lm-darkgray bg-lm-lightgray px-1 py-0.5 text-gray-800 dark:border-transparent dark:bg-gray-800 dark:text-white"
    >
      {#if intention_of_investment_map[ioi] != null}
        <svelte:component this={intention_of_investment_map[ioi]} />
      {/if}
      <!-- This is a special case where the string to be translated is NOT defined
        in the backend and needs to be defined in the frontend -->
      {$_(flat_intention_of_investment_map[ioi])}
    </span>
  {/each}
{:else}
  {parseValues(value, formfield.choices)}
{/if}
