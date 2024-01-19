<script lang="ts">
  import type { ComponentType } from "svelte"
  import { _ } from "svelte-i18n"

  import { flat_intention_of_investment_map } from "$lib/choices"
  import type { IntentionOfInvestment } from "$lib/types/deal"

  import AgricultureIcon from "$components/icons/AgricultureIcon.svelte"
  import FoodCropsIcon from "$components/icons/FoodCropsIcon.svelte"
  import ForestIcon from "$components/icons/ForestIcon.svelte"
  import HandsHoldingCircleIcon from "$components/icons/HandsHoldingCircleIcon.svelte"
  import IndustryIcon from "$components/icons/IndustryIcon.svelte"
  import LandSpeculationIcon from "$components/icons/LandSpeculationIcon.svelte"
  import LifestockIcon from "$components/icons/LifestockIcon.svelte"
  import MiningIcon from "$components/icons/MiningIcon.svelte"
  import OilIcon from "$components/icons/OilIcon.svelte"
  import OtterIcon from "$components/icons/OtterIcon.svelte"
  import PlaneIcon from "$components/icons/PlaneIcon.svelte"
  import RenewableEnergyIcon from "$components/icons/RenewableEnergyIcon.svelte"
  import SolarPanelIcon from "$components/icons/SolarPanelIcon.svelte"

  export let value: IntentionOfInvestment[]

  const intention_of_investment_map: { [key in IntentionOfInvestment]: ComponentType } =
    {
      // agriculture
      BIOFUELS: AgricultureIcon,
      BIOMASS_ENERGY_GENERATION: AgricultureIcon,
      FODDER: FoodCropsIcon,
      FOOD_CROPS: FoodCropsIcon,
      LIVESTOCK: LifestockIcon,
      NON_FOOD_AGRICULTURE: AgricultureIcon,
      AGRICULTURE_UNSPECIFIED: AgricultureIcon,
      // forest
      BIOMASS_ENERGY_PRODUCTION: ForestIcon,
      CARBON: ForestIcon,
      FOREST_LOGGING: ForestIcon,
      TIMBER_PLANTATION: ForestIcon,
      FORESTRY_UNSPECIFIED: ForestIcon,
      // renewable
      SOLAR_PARK: SolarPanelIcon,
      WIND_FARM: RenewableEnergyIcon,
      RENEWABLE_ENERGY: RenewableEnergyIcon,
      // other
      CONVERSATION: HandsHoldingCircleIcon,
      INDUSTRY: IndustryIcon,
      LAND_SPECULATION: LandSpeculationIcon,
      MINING: MiningIcon,
      OIL_GAS_EXTRACTION: OilIcon,
      TOURISM: PlaneIcon,
      OTHER: OtterIcon,
    }
</script>

{#each value as ioi}
  <span
    class="mx-1 my-0.5 inline-flex items-center gap-1 whitespace-nowrap border border-gray-100 bg-gray-50 px-1 py-0.5 text-gray-800 dark:border-transparent dark:bg-gray-800 dark:text-white"
  >
    {#if intention_of_investment_map[ioi] != null}
      <svelte:component this={intention_of_investment_map[ioi]} />
    {/if}
    <!-- This is a special case where the string to be translated is NOT defined
        in the backend and needs to be defined in the frontend -->
    {$_(flat_intention_of_investment_map[ioi])}
  </span>
{/each}
