<script lang="ts">
  import { page } from "$app/state"

  import { filters } from "$lib/accountability/filters"
  import { capitalizeFirst, groupBy } from "$lib/accountability/helpers"
  import { dealChoices } from "$lib/fieldChoices"

  import Checkbox from "./Checkbox.svelte"
  import Input from "./Input.svelte"
  import InputCheckboxGroup from "./InputCheckboxGroup.svelte"
  import InputRadioGroup from "./InputRadioGroup.svelte"
  import SideBarFilterTabItem from "./SideBarFilterTabItem.svelte"

  interface Props {
    disabled?: boolean
  }

  let { disabled = false }: Props = $props()

  const regionChoices = page.data.regions.map(({ name: label, id: value }) => ({
    label,
    value,
  }))
  const countryChoices = page.data.countries.map(({ name: label, id: value }) => ({
    label,
    value,
  }))

  const negotiationStatusChoices = $dealChoices.negotiation_status
  const negotiationStatusGroups = groupBy(
    negotiationStatusChoices,
    "group",
    "value",
  ).map(({ label, values }) => ({
    label: capitalizeFirst(label.replace("_", " ").toLowerCase()),
    values,
  }))

  const natureOfDealChoices = $dealChoices.nature_of_deal
  const investorNamesChoices = page.data.investors.map(
    ({ name: label, id: value }) => ({ label, value }),
  )
  const implementationStatusChoices = [
    { label: "No information", value: "UNKNOWN" },
  ].concat($dealChoices.implementation_status)

  const intentionOfInvestmentChoices = $dealChoices.intention_of_investment
  const intentionOfInvestmentGroups = groupBy(
    intentionOfInvestmentChoices,
    "group",
    "value",
  ).map(({ label, values }) => ({
    label: capitalizeFirst(label.replace("_", " ").toLowerCase()),
    values,
  }))

  const produceCrops = $dealChoices.crops
  const produceAnimals = $dealChoices.animals
  const produceMinerals = $dealChoices.minerals

  const scopeChoices = [
    { label: "All", value: null },
    { label: "Transnational", value: true },
    { label: "Domestic", value: false },
  ]

  const forestConcessionChoices = [
    { label: "Included", value: null },
    { label: "Excluded", value: false },
    { label: "Only", value: true },
  ]

  let invalidMaxSize = $derived(
    $filters.area_min && $filters.area_min > $filters.area_max ? true : false,
  )
  let sizeNotification = $derived($filters.area_min || $filters.area_max ? true : false)

  let invalidMaxYear = $derived(
    $filters.initiation_year_max &&
      $filters.initiation_year_min &&
      $filters.initiation_year_min > $filters.initiation_year_max
      ? true
      : false,
  )
  let yearNotification = $derived(
    $filters.initiation_year_min || $filters.initiation_year_max ? true : false,
  )
</script>

<div class="mb-6 h-fit overflow-y-auto">
  <SideBarFilterTabItem label="Land Matrix region" count={$filters.region_id?.length}>
    <Input
      type="multiselect"
      placeholder="Choose a region"
      choices={regionChoices}
      bind:value={$filters.region_id}
      {disabled}
    />
  </SideBarFilterTabItem>

  <SideBarFilterTabItem label="Countries" count={$filters.country_id?.length}>
    <Input
      type="multiselect"
      placeholder="Choose a country"
      choices={countryChoices}
      bind:value={$filters.country_id}
      {disabled}
    />
  </SideBarFilterTabItem>

  <SideBarFilterTabItem label="Deal Size" notification={sizeNotification}>
    <div class="flex flex-col gap-1.5">
      <Input
        type="number"
        placeholder="from"
        min="0"
        bind:value={$filters.area_min}
        {disabled}
      />
      <Input
        type="number"
        placeholder="to"
        min="0"
        bind:value={$filters.area_max}
        {disabled}
        status={invalidMaxSize ? "invalid" : "neutral"}
      />
    </div>
  </SideBarFilterTabItem>

  <SideBarFilterTabItem
    label="Negotiation status"
    count={$filters.negotiation_status.length}
  >
    <InputCheckboxGroup
      choices={negotiationStatusChoices}
      categories={negotiationStatusGroups}
      orphansLabel="Other"
      bind:group={$filters.negotiation_status}
      {disabled}
    />
  </SideBarFilterTabItem>

  <SideBarFilterTabItem
    label="Nature of the deal"
    count={$filters.nature_of_deal.length}
  >
    <InputCheckboxGroup
      choices={natureOfDealChoices}
      bind:group={$filters.nature_of_deal}
      {disabled}
    />
  </SideBarFilterTabItem>

  <SideBarFilterTabItem
    label="Investors"
    count={$filters.investor_id?.length + $filters.investor_country_id?.length}
  >
    <div class="flex flex-col gap-1.5" class:gap-4={$filters.investor_id?.length > 0}>
      <Input
        type="multiselect"
        placeholder="Investor name"
        choices={investorNamesChoices}
        bind:value={$filters.investor_id}
        {disabled}
      />
      <Input
        type="multiselect"
        placeholder="Country of registration"
        choices={countryChoices}
        bind:value={$filters.investor_country_id}
        {disabled}
      />
    </div>
  </SideBarFilterTabItem>

  <SideBarFilterTabItem label="Year of initiation" notification={yearNotification}>
    <div class="flex flex-col gap-1.5">
      <Input
        type="number"
        placeholder="from"
        min="0"
        bind:value={$filters.initiation_year_min}
        {disabled}
      />
      <Input
        type="number"
        placeholder="to"
        min="0"
        bind:value={$filters.initiation_year_max}
        {disabled}
        status={invalidMaxYear ? "invalid" : "neutral"}
      />
      <Checkbox
        label="Include unknown years"
        paddingX="2"
        bind:checked={$filters.initiation_year_unknown}
        {disabled}
      />
    </div>
  </SideBarFilterTabItem>

  <SideBarFilterTabItem
    label="Implementation status"
    count={$filters.implementation_status.length}
  >
    <InputCheckboxGroup
      choices={implementationStatusChoices}
      bind:group={$filters.implementation_status}
      {disabled}
    />
  </SideBarFilterTabItem>

  <SideBarFilterTabItem
    label="Intention of investment"
    count={$filters.intention_of_investment.length +
      $filters.intention_of_investment_unknown}
  >
    <Checkbox
      label="No information"
      bind:checked={$filters.intention_of_investment_unknown}
      {disabled}
    />
    <InputCheckboxGroup
      choices={intentionOfInvestmentChoices}
      bind:group={$filters.intention_of_investment}
      {disabled}
      categories={intentionOfInvestmentGroups}
      orphansLabel="Other"
    />
  </SideBarFilterTabItem>

  <SideBarFilterTabItem
    label="Produce"
    count={$filters.crops?.length +
      $filters.animals?.length +
      $filters.minerals?.length}
  >
    <div class="pb-1.5" class:pb-4={$filters.crops?.length > 0}>
      <Input
        type="multiselect"
        placeholder="Crops"
        choices={produceCrops}
        bind:value={$filters.crops}
        {disabled}
      />
    </div>
    <div class="pb-1.5" class:pb-4={$filters.animals?.length > 0}>
      <Input
        type="multiselect"
        placeholder="Animals"
        choices={produceAnimals}
        bind:value={$filters.animals}
        {disabled}
      />
    </div>
    <Input
      type="multiselect"
      placeholder="Minerals"
      choices={produceMinerals}
      bind:value={$filters.minerals}
      {disabled}
    />
  </SideBarFilterTabItem>

  <SideBarFilterTabItem label="Scope">
    <InputRadioGroup
      choices={scopeChoices}
      bind:value={$filters.transnational}
      {disabled}
    />
  </SideBarFilterTabItem>

  <SideBarFilterTabItem label="Forest concession">
    <InputRadioGroup
      choices={forestConcessionChoices}
      bind:value={$filters.forest_concession}
      {disabled}
    />
  </SideBarFilterTabItem>
</div>
