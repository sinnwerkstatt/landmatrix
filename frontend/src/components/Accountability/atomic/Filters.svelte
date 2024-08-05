<script lang="ts">
    import { page } from "$app/stores"
    import { filters } from "$lib/accountability/filters"
    import { groupBy, capitalizeFirst } from "$lib/accountability/helpers"

    import SideBarFilterTabItem from "./SideBarFilterTabItem.svelte"
    import Checkbox from "./Checkbox.svelte"
    import InputCheckboxGroup from "./InputCheckboxGroup.svelte"
    import InputRadioGroup from "./InputRadioGroup.svelte"
    import Input from "./Input.svelte"

    const regionChoices = $page.data.regions.map(({ name:label, id:value }) => ({ label, value }))
    const countryChoices = $page.data.countries.map(({ name:label, id:value }) => ({ label, value }))

    const negotiationStatusChoices = $page.data.fieldChoices.deal.negotiation_status
    const negotiationStatusGroups = groupBy(negotiationStatusChoices, 'group', 'value')
                                    .map(({ label, values }) => 
                                        ({ label: capitalizeFirst(label.replace("_", " ").toLowerCase()), values }))
                                        
    const natureOfDealChoices = $page.data.fieldChoices.deal.nature_of_deal
    const investorNamesChoices = $page.data.investors.map(({ name:label, id:value }) => ({ label, value }))
    const implementationStatusChoices = [{ label: "No information", value: "UNKNOWN" }].concat($page.data.fieldChoices.deal.implementation_status)

    const intentionOfInvestmentChoices = $page.data.fieldChoices.deal.intention_of_investment
    const intentionOfInvestmentGroups = groupBy(intentionOfInvestmentChoices, 'group', 'value')
                                        .map(({ label, values }) => 
                                            ({ label: capitalizeFirst(label.replace("_", " ").toLowerCase()), values }))

    const produceCrops = $page.data.fieldChoices.deal.crops
    const produceAnimals = $page.data.fieldChoices.deal.animals
    const produceMinerals = $page.data.fieldChoices.deal.minerals

    const scopeChoices = [
        { label: "All", value: null },
        { label: "Transnational", value: true },
        { label: "Domestic", value: false }
    ]

    const forestConcessionChoices = [
        { label: "Included", value: null },
        { label: "Excluded", value: false },
        { label: "Only", value: true }
    ]

    $: invalidMaxSize = $filters.area_min && $filters.area_min > $filters.area_max ? true : false;
    $: sizeNotification = $filters.area_min || $filters.area_max ? true : false;

    $: invalidMaxYear = $filters.initiation_year_max && $filters.initiation_year_min > $filters.initiation_year_max ? true : false;
    $: yearNotification = $filters.initiation_year_min || $filters.initiation_year_max ? true : false;

</script>

<div class="overflow-y-auto h-fit mb-6">
    <SideBarFilterTabItem label="Land Matrix region" count={$filters.region_id?.length} >
        <Input type="multiselect" placeholder="Choose a region" choices={regionChoices} bind:value={$filters.region_id} />
    </SideBarFilterTabItem>

    <SideBarFilterTabItem label="Countries" count={$filters.country_id?.length} >
        <Input type="multiselect" placeholder="Choose a country" choices={countryChoices} bind:value={$filters.country_id} />
    </SideBarFilterTabItem>

    <SideBarFilterTabItem label="Deal Size" notification={sizeNotification} >
        <div class="flex flex-col gap-1.5">
            <Input type="number" placeholder="from" min=0 bind:value={$filters.area_min} />
            <Input type="number" placeholder="to" min=0 bind:value={$filters.area_max}
                    status={invalidMaxSize ? "invalid" : "neutral"} />
        </div>
    </SideBarFilterTabItem>

    <SideBarFilterTabItem label="Negotiation status" count={$filters.negotiation_status.length} >
        <InputCheckboxGroup choices={negotiationStatusChoices} categories={negotiationStatusGroups}
                            orphansLabel="Other" bind:group={$filters.negotiation_status} />
    </SideBarFilterTabItem>

    <SideBarFilterTabItem label="Nature of the deal" count={$filters.nature_of_deal.length} >
        <InputCheckboxGroup choices={natureOfDealChoices} bind:group={$filters.nature_of_deal} />
    </SideBarFilterTabItem>

    <SideBarFilterTabItem label="Investors" count={$filters.investor_id?.length + $filters.investor_country_id?.length} >
        <div class="flex flex-col gap-1.5" class:gap-4={$filters.investor_id?.length > 0}>
            <Input type="multiselect" placeholder="Investor name" choices={investorNamesChoices} bind:value={$filters.investor_id} />
            <Input type="multiselect" placeholder="Country of registration" choices={countryChoices} bind:value={$filters.investor_country_id} />
        </div>
    </SideBarFilterTabItem>

    <SideBarFilterTabItem label="Year of initiation" notification={yearNotification} >
        <div class="flex flex-col gap-1.5">
            <Input type="number" placeholder="from" min=0 bind:value={$filters.initiation_year_min} />
            <Input type="number" placeholder="to" min=0 bind:value={$filters.initiation_year_max}
                    status={invalidMaxYear ? "invalid" : "neutral"} />
            <Checkbox label="Include unknown years" paddingX=2 bind:checked={$filters.initiation_year_unknown} />
        </div>
    </SideBarFilterTabItem>

    <SideBarFilterTabItem label="Implementation status" count={$filters.implementation_status.length} >
        <InputCheckboxGroup choices={implementationStatusChoices} bind:group={$filters.implementation_status} />
    </SideBarFilterTabItem>

    <SideBarFilterTabItem label="Intention of investment" count={$filters.intention_of_investment.length + $filters.intention_of_investment_unknown} >
        <Checkbox label="No information" bind:checked={$filters.intention_of_investment_unknown} />
        <InputCheckboxGroup choices={intentionOfInvestmentChoices} bind:group={$filters.intention_of_investment}
                            categories={intentionOfInvestmentGroups} orphansLabel="Other" />
    </SideBarFilterTabItem>

    <SideBarFilterTabItem label="Produce" count={$filters.crops?.length + $filters.animals?.length + $filters.minerals?.length}>
        <div class="pb-1.5" class:pb-4={$filters.crops?.length > 0}>
            <Input type="multiselect" placeholder="Crops" choices={produceCrops} bind:value={$filters.crops} />
        </div>
        <div class="pb-1.5" class:pb-4={$filters.animals?.length > 0}>
            <Input type="multiselect" placeholder="Animals" choices={produceAnimals} bind:value={$filters.animals} />
        </div>
        <Input type="multiselect" placeholder="Minerals" choices={produceMinerals} bind:value={$filters.minerals} />
    </SideBarFilterTabItem>

    <SideBarFilterTabItem label="Scope" >
        <InputRadioGroup choices={scopeChoices} bind:value={$filters.transnational} />
    </SideBarFilterTabItem>

    <SideBarFilterTabItem label="Forest concession" >
        <InputRadioGroup choices={forestConcessionChoices} bind:value={$filters.forest_concession} />
    </SideBarFilterTabItem>
</div>