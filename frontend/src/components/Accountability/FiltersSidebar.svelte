<script lang="ts">
    import { openedFilterBar } from "$lib/accountability/stores"

    import Sidebar from "./atomic/Sidebar.svelte"
    import IconCollapse from "$components/Accountability/icons/IconCollapse.svelte"
    import SideBarFilterTabItem from "./atomic/SideBarFilterTabItem.svelte"
    import Input from "./atomic/Input.svelte"
    import InputCheckboxGroup from "./atomic/InputCheckboxGroup.svelte"

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

    let filters = {
        regions: [],
        countries: [],
        size: { min: null, max: null },
        negotiationStatus: ["EXPRESSION_OF_INTEREST", "UNDER_NEGOTIATION"],
        natureOfDeal: ["OUTRIGHT_PURCHASE"]
    }

    $: invalidMaxSize = filters.size.max && filters.size.min > filters.size.max ? true : false;
    $: sizeNotification = filters.size.min || filters.size.max ? true : false;

    // $: console.log(filters)
</script>

{#if $openedFilterBar}
    <Sidebar>
        <div class="flex items-center flex-nowrap justify-between">
            <span class="text-a-sm font-semibold text-a-gray-500">Filters</span>
            <button on:click={() => { $openedFilterBar = false }}>
                <IconCollapse />
            </button>
        </div>

        <div class="overflow-y-auto">
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
                                    orphansLabel="Others" bind:group={filters.negotiationStatus} />
            </SideBarFilterTabItem>

            <SideBarFilterTabItem label="Nature of the deal" count={filters.natureOfDeal.length} >
                <InputCheckboxGroup choices={natureOfDealChoices} bind:group={filters.natureOfDeal} />
            </SideBarFilterTabItem>

        </div>
    </Sidebar>
{/if}