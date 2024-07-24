<script lang="ts">
    import { page } from "$app/stores"

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
    const implementationStatusChoices = $page.data.fieldChoices.deal.implementation_status
    const intentionOfInvestmentChoices = $page.data.fieldChoices.deal.intention_of_investment
    const intentionOfInvestmentGroups = groupBy(intentionOfInvestmentChoices, 'group', 'value')
                                        .map(({ label, values }) => 
                                            ({ label: capitalizeFirst(label.replace("_", " ").toLowerCase()), values }))
    const produceCrops = $page.data.fieldChoices.deal.crops
    const produceAnimals = $page.data.fieldChoices.deal.animals
    const produceMinerals = $page.data.fieldChoices.deal.minerals
    const produceChoices = produceCrops.concat(produceAnimals).concat(produceMinerals)
    const produceCategories = [
        { label: "Crops", values: produceCrops.map(e => e.value) },
        { label: "Animals", values: produceAnimals.map(e => e.value) },
        { label: "Mineral resources", values: produceMinerals.map(e => e.value) }
    ]
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

    let filters = {
        regions: [],
        countries: [],
        size: { min: null, max: null },
        negotiationStatus: ["EXPRESSION_OF_INTEREST", "UNDER_NEGOTIATION"],
        natureOfDeal: ["OUTRIGHT_PURCHASE"],
        investor: { names: [] , countries: [] },
        initiationYear: { min: null, max: null, includeUnknown: false },
        implementationStatus: [],
        intentionOfInvestment: { values: [], noInformation: false },
        produce: [],
        transnational: null,
        forestConcession: null
    }

    $: invalidMaxSize = filters.size.max && filters.size.min > filters.size.max ? true : false;
    $: sizeNotification = filters.size.min || filters.size.max ? true : false;

    $: invalidMaxYear = filters.initiationYear.max && filters.initiationYear.min > filters.initiationYear.max ? true : false;
    $: yearNotification = filters.initiationYear.min || filters.initiationYear.max ? true : false;

    // $: console.log(filters)

</script>

<div class="overflow-y-auto h-fit mb-6">
    <SideBarFilterTabItem label="Land Matrix region" count={filters.regions?.length} >
        <Input type="multiselect" placeholder="Choose a region" choices={regionChoices} bind:value={filters.regions} />
    </SideBarFilterTabItem>

    <SideBarFilterTabItem label="Countries" count={filters.countries?.length} >
        <Input type="multiselect" placeholder="Choose a country" choices={countryChoices} bind:value={filters.countries} />
    </SideBarFilterTabItem>

    <SideBarFilterTabItem label="Deal Size" notification={sizeNotification} >
        <div class="flex flex-col gap-1.5">
            <Input type="number" placeholder="from" min=0 bind:value={filters.size.min} />
            <Input type="number" placeholder="to" min=0 bind:value={filters.size.max}
                    status={invalidMaxSize ? "invalid" : "neutral"} />
        </div>
    </SideBarFilterTabItem>

    <SideBarFilterTabItem label="Negotiation status" count={filters.negotiationStatus.length} >
        <InputCheckboxGroup choices={negotiationStatusChoices} categories={negotiationStatusGroups}
                            orphansLabel="Other" bind:group={filters.negotiationStatus} />
    </SideBarFilterTabItem>

    <SideBarFilterTabItem label="Nature of the deal" count={filters.natureOfDeal.length} >
        <InputCheckboxGroup choices={natureOfDealChoices} bind:group={filters.natureOfDeal} />
    </SideBarFilterTabItem>

    <SideBarFilterTabItem label="Investors" count={filters.investor.names?.length + filters.investor.countries?.length} >
        <div class="flex flex-col gap-1.5" class:gap-4={filters.investor.names?.length > 0}>
            <Input type="multiselect" placeholder="Investor name" choices={investorNamesChoices} bind:value={filters.investor.names} />
            <Input type="multiselect" placeholder="Country of registration" choices={countryChoices} bind:value={filters.investor.countries} />
        </div>
    </SideBarFilterTabItem>

    <SideBarFilterTabItem label="Year of initiation" notification={yearNotification} >
        <div class="flex flex-col gap-1.5">
            <Input type="number" placeholder="from" min=0 bind:value={filters.initiationYear.min} />
            <Input type="number" placeholder="to" min=0 bind:value={filters.initiationYear.max}
                    status={invalidMaxYear ? "invalid" : "neutral"} />
            <Checkbox label="Include unknown years" paddingX=2 bind:checked={filters.initiationYear.includeUnknown} />
        </div>
    </SideBarFilterTabItem>

    <SideBarFilterTabItem label="Implementation status" count={filters.implementationStatus.length} >
        <InputCheckboxGroup choices={implementationStatusChoices} bind:group={filters.implementationStatus} />
    </SideBarFilterTabItem>

    <SideBarFilterTabItem label="Intention of investment" count={filters.intentionOfInvestment.values.length + filters.intentionOfInvestment.noInformation} >
        <Checkbox label="No information" bind:checked={filters.intentionOfInvestment.noInformation} />
        <InputCheckboxGroup choices={intentionOfInvestmentChoices} bind:group={filters.intentionOfInvestment.values}
                            categories={intentionOfInvestmentGroups} orphansLabel="Other" />
    </SideBarFilterTabItem>

    <SideBarFilterTabItem label="Produce" count={filters.produce.length} >
        <Input type="multiselect" placeholder="Select production" choices={produceChoices} 
                                    bind:value={filters.produce} categories={produceCategories}
                                    readonlyCategories={true} />
    </SideBarFilterTabItem>

    <SideBarFilterTabItem label="Scope" >
        <InputRadioGroup choices={scopeChoices} bind:value={filters.transnational} />
    </SideBarFilterTabItem>

    <SideBarFilterTabItem label="Forest concession" >
        <InputRadioGroup choices={forestConcessionChoices} bind:value={filters.forestConcession} />
    </SideBarFilterTabItem>
</div>