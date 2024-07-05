<script lang="ts">
    import { currentDeal, currentVariable, openDrawer } from "$lib/accountability/stores"

    import Drawer from "./atomic/Drawer.svelte"
    import DrawerScoringItem from "./atomic/DrawerScoringItem.svelte"
    import Badge from "./atomic/Badge.svelte"
    import Input from "./atomic/Input.svelte"
    import Avatar from "./atomic/Avatar.svelte"
    import IconXMark from "./icons/IconXMark.svelte"
    import Section from "./atomic/Section.svelte"
    import DrawerScoringInfo from "./atomic/DrawerScoringInfo.svelte"
    import Button from "./Button.svelte"

    let score = null
    let status = "no_score"

    const scores = [
        { value: 0, label: "No data", description: "Insufficient data available to score this variable" },
        { value: 1, label: "Severe violations", description: "Severe violations description" },
        { value: 2, label: "Partial violations", description: "Partial violations description" },
        { value: 3, label: "No violations", description: "No violations description (congrats!)" }
    ]

    const statuses = [
        { value: "no_score", label: "To score" },
        { value: "pending", label: "Waiting for review" },
        { value: "validated", label: "Validated" },
        { value: "no_data", label: "No data" }
    ]

    const selectableStatuses = [
        { value: "validated", label: "Validated" },
        { value: "waiting for review", label: "Waiting for review" }
    ]

    const relatedArticles = [
        {
            chapter: 4,
            article: 4.5,
            title: "Rights and responsibilities related to tenure",
            description: "States should protect legitimate tenure rights, and ensure that people are not arbitrarily evicted and that their legitimate tenure rights are not otherwise extinguished or infringed."
        },
        {
            chapter: 7,
            article: 7.6,
            title: "Safeguards",
            description: "Where it is not possible to provide legal recognition of tenure rights, States should prevent forced evictions that are inconsistent with their existing obligations under national and international law, and in accordance with the principles of these Guidelines."
        },
        {
            chapter: 10,
            article: 10.6,
            title: "Informal tenure",
            description: "Where it is not possible to provide legal recognition to informal tenure, States should prevent forced evictions that violate existing obligations under national and international law, and consistent with relevant provisions under Section 16."
        }
    ]

    const dealInfo = [
        {
            label: "Recognition of status of community land tenure",
            value: "Indigenous rights recognized"
        },
        {
            label: "Comment on recognition of community land tenure",
            value: "Rights officially recognised, but not applied."
        },
        {
            label: "Number of people displaced out of their community land",
            value: "104"
        },
        {
            label: "Number of people displaced staying on their community land",
            value: undefined
        },
        {
            label: "Number of households displaced “only” from their agricultural fields",
            value: undefined
        },
        {
            label: "Number of people facing displacement once project is fully implemented",
            value: undefined
        },
        {
            label: "Comments on displacement of people",
            value: "244 farmers complained in Sept. 2016 against the planting of oil palm [company] for violation of property rights."
        }
    ]

    const dealAdditionalInfo = [
        {
            label: "Received compensation",
            value: "The group is accused of never having respected its commitments."
        },
        {
            label: "Community consultation",
            value: "Limited consultation"
        },
        {
            label: "Comment on consultation of local community",
            value: "No consultation with the forest-dwelling people during the privatisation of the current Company plantation after 2000. The government committed to returning thousands of hectares to local communities but so far just over 100 hectares have been returned. People are not aware of what land has been returned to them and their customary lands and farms are inside concession boundaries."
        }
    ]

    const dealMainInfo = [
        { label: "Country", value: "Senegal" },
        { label: "Size", value: 1000 },
        { label: "Investor", id: 44470, name: "Swami Agri" }
    ]

    function selectScore(event) {
        const value = event.detail.value
        score = value
        if (value == 0) {
            status = "no_data"
        } else {
            if (!["pending", "validated"].includes(status)) status = "validated"
        }
    }

</script>

<Drawer bind:open={$openDrawer}>
    <div class="h-screen flex flex-col divide-y divide-a-gray-200">
        <!-- Heading -->
        <div class="p-6">
            <div class="flex justify-between">
                <div class="flex items-center gap-2">
                    <span class="block w-3 h-3 rounded-full indicator"></span>
                    <h1 class="text-a-xl font-semibold">Variable {$currentVariable} - Description</h1>
                    <Badge variant="filled" label={$currentDeal} href="https://landmatrix.org/deal/{$currentDeal}/" />
                </div>
                <button class="text-a-gray-400" on:click={() => openDrawer.set(false)}><IconXMark size=24 /></button>
            </div>
            <div class="mt-2 flex gap-4">
                <Input type="select" choices={selectableStatuses} style="white" extraClass="!w-60"
                       search={false}  />
                <Avatar />
            </div>
        </div>

        <!-- Body -->
        <div class="p-6 h-full w-full overflow-auto">
            <h2>VGGT compliance</h2>
            <div class="flex gap-2">
                {#each scores as scoreBox}
                    <DrawerScoringItem {...scoreBox} {score} on:onClick={selectScore} />
                {/each}
            </div>

            <Section title="Show more details" extraClass="pl-0 underline underline-offset-4" open={false}>
                <!-- Help -->
                <h3>Help</h3>
                <ul>
                    <li>Please make sure that compensation refer to displacement</li>
                    <li>Dealt with means that the company addressed the issues created by the displacement. Compensation and Resettlement that do not address the issue  created by displacement such as not providing any new livelihood opportunities or creating even more conflict should be rated as not adequately dealt with.</li>
                    <li>If displacement and no information provided on “is dealt with”, then assume it is not dealt with</li>
                </ul>

                <!-- Resources -->
                <h3>Resources (VGGTs articles linked to this variable)</h3>
                {#each relatedArticles as { chapter, article, title, description }}
                    <ul>
                        <li class="font-semibold">Article {article} - Chapter {chapter} - {title}</li>
                        <ul>
                            <li>{description}</li>
                        </ul>
                    </ul>
                {/each}
            </Section>

            <!-- LM Info -->
            <h2 class="mt-4">Land Matrix information</h2>
            <DrawerScoringInfo {dealInfo} />
            <h4 class="my-4 text-sm font-medium text-a-gray-500">Additional fields</h4>
            <DrawerScoringInfo dealInfo={dealAdditionalInfo} />
            <h2 class="mt-10">Deal main information</h2>
            <DrawerScoringInfo dealInfo={dealMainInfo} />
        </div>

        <!-- Footer -->
        <div class="p-6 grow-0 flex justify-between">
            <Button label="Previous" type="outline" style="neutral" />
            <div class="flex gap-4">
                <Button label="Next" type="outline" style="neutral" />
                <Button label="Save" style="neutral" disabled />
            </div>
        </div>
    </div>
</Drawer>

<style>
    h2 {
        @apply text-a-2xl font-semibold mb-4;
    }

    h3 {
        @apply py-2;
        @apply text-a-base;
    }

    ul {
        @apply list-disc pl-4;
        @apply text-a-sm font-normal text-a-gray-500;
    }

    .indicator {
        @apply bg-a-gray-200;
    }
</style>