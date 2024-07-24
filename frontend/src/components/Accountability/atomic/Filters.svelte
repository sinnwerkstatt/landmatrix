<script lang="ts">
    import { page } from "$app/stores"

    import SideBarFilterTabItem from "./SideBarFilterTabItem.svelte"
    import Checkbox from "./Checkbox.svelte"
    import InputCheckboxGroup from "./InputCheckboxGroup.svelte"
    import InputRadioGroup from "./InputRadioGroup.svelte"
    import Input from "./Input.svelte"

    console.log($page.data)

    const regionChoices = [
        { label: "First region", value: "1" },
        { label: "Second region", value: "2" },
        { label: "Third region", value: "3" }
    ]

    const countryChoices = [
        { label: "One", value: "1" },
        { label: "Two", value: "2" },
        { label: "Three", value: "3" },
        { label: "Four", value: "4" },
        { label: "Five", value: "5" },
        { label: "Six", value: "6" },
        { label: "Seven", value: "7" },
        { label: "Eight", value: "8" },
        { label: "Nine", value: "9" },
        { label: "Ten", value: "10" }
    ]

    const negotiationStatusChoices = [
        { value: "EXPRESSION_OF_INTEREST", label: "Expression of interest" },
        { value: "UNDER_NEGOTIATION", label: "Under negotiation"},
        { value: "MEMORANDUM_OF_UNDERSTANDING", label: "Memorandum of understanding" },
        { value: "ORAL_AGREEMENT", label: "Oral Agreement" },
        { value: "CONTRACT_SIGNED", label: "Contract signed" },
        { value: "CHANGE_OF_OWNERSHIP", label: "Change of ownership" },
        { value: "NEGOTIATIONS_FAILED", label: "Negotiations failed" },
        { value: "CONTRACT_CANCELED", label: "Contract cancelled" },
        { value: "CONTRACT_EXPIRED", label: "Contract expired" }
    ]

    const negotiationStatusGroups = [
        { label: "Intended", values: ["EXPRESSION_OF_INTEREST", "UNDER_NEGOTIATION", "MEMORANDUM_OF_UNDERSTANDING"] },
        { label: "Concluded", values: ["ORAL_AGREEMENT", "CONTRACT_SIGNED", "CHANGE_OF_OWNERSHIP"] },
        { label: "Failed", values: ["NEGOTIATIONS_FAILED", "CONTRACT_CANCELED"] }
    ]

    const natureOfDealChoices = [
        { value: "OUTRIGHT_PURCHASE", label: "Outright purchase" },
        { value: "LEASE", label: "Lease" },
        { value: "CONCESSION", label: "Concession" },
        { value: "EXPLOITATION_PERMIT", label: "Exploitation permit / license / concession (for mineral resources)" },
        { value: "PURE_CONTRACT_FARMING", label: "Pure contract farming" },
        { value: "OTHER", label: "Other" }
    ]

    const investorNamesChoices = [
        { value: "1", label: "A" },
        { value: "2", label: "B" },
        { value: "3", label: "C" }
    ]

    const implementationStatusChoices = [
        { value: "PROJECT_NOT_STARTED", label: "Project not started" },
        { value: "STARTUP_PHASE", label: "Startup phase (no production)" },
        { value: "IN_OPERATION", label: "In operation (production)" },
        { value: "PROJECT_ABANDONED", label: "Project abandoned" }
    ]

    const intentionOfInvestmentChoices = [
        { value: "BIOFUELS", label: "Biomass for biofuels" },
        { value: "BIOMASS_ENERGY_GENERATION", label: "Biomass for energy generation (agriculture)" },
        { value: "FODDER", label: "Fodder" },
        { value: "FOOD_CROPS", label: "Food crops" },
        { value: "LIVESTOCK", label: "Livestock" },
        { value: "NON_FOOD_AGRICULTURE", label: "Non-food agricultural commodities" },
        { value: "AGRICULTURE_UNSPECIFIED", label: "Agriculture unspecified" },
        { value: "BIOMASS_ENERGY_PRODUCTION", label: "Biomass for energy generation (forestry)" },
        { value: "CARBON", label: "For carbon sequestration/REDD" },
        { value: "FOREST_LOGGING", label: "Forest logging / management for wood and fiber" },
        { value: "TIMBER_PLANTATION", label: "Timber plantation for wood and fiber" },
        { value: "FORESTRY_UNSPECIFIED", label: "Forestry unspecified" },
        { value: "SOLAR_PARK", label: "Solar park" },
        { value: "WIND_FARM", label: "Wind farm" },
        { value: "RENEWABLE_ENERGY", label: "Renewable energy unspecified" },
        { value: "CONVERSATION", label: "Conservation" },
        { value: "INDUSTRY", label: "Industry" },
        { value: "LAND_SPECULATION", label: "Land speculation" },
        { value: "MINING", label: "Mining" },
        { value: "OIL_GAS_EXTRACTION", label: "Oil / Gas extraction" },
        { value: "TOURISM", label: "Tourism" },
        { value: "OTHER", label: "Other" }
    ]

    const intentionOfInvestmentGroups = [
        { label: "Agriculture", values: ["BIOFUELS", "BIOMASS_ENERGY_GENERATION", "FODDER", "FOOD_CROPS", "LIVESTOCK", "NON_FOOD_AGRICULTURE", "AGRICULTURE_UNSPECIFIED"] },
        { label: "Forestry", values: ["BIOMASS_ENERGY_PRODUCTION", "CARBON", "FOREST_LOGGING", "TIMBER_PLANTATION", "FORESTRY_UNSPECIFIED"] },
        { label: "Renewable energy power plants", values: ["SOLAR_PARK", "WIND_FARM", "RENEWABLE_ENERGY"] },
    ]

    const produceChoices = [
        { value: "ACC", label: "Accacia" },
        { value: "ALF", label: "Alfalfa" },
        { value: "ALG", label: "Seaweed / Macroalgae(unspecified)" },
        { value: "ALM", label: "Almond" },
        { value: "ALV", label: "Aloe Vera" },
        { value: "APL", label: "Apple" },
        { value: "BEE", label: "Beef Cattle" },
        { value: "FSH", label: "Fish" },
        { value: "GOT", label: "Goats" },
        { value: "PIG", label: "Pork" },
        { value: "POU", label: "Poultry" },
        { value: "SHP", label: "Sheep" }
    ]

    const produceCategories = [
        { label: "Crops", values: ["ACC", "ALF", "ALG", "ALM", "ALV", "APL"] },
        { label: "Animals", values: ["BEE", "FSH", "GOT", "PIG", "POU", "SHP"] }
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