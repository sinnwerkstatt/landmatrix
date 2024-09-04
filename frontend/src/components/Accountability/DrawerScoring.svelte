<script lang="ts">
    import { page } from "$app/stores"
    import { scoreLabels, vggtInfo } from "$lib/accountability/vggtInfo"
    import { currentDeal, currentVariable, openDrawer, deals } from "$lib/accountability/stores"

    import Drawer from "./atomic/Drawer.svelte"
    import DrawerScoringItem from "./atomic/DrawerScoringItem.svelte"
    import Badge from "./atomic/Badge.svelte"
    import Input from "./atomic/Input.svelte"
    import Avatar from "./atomic/Avatar.svelte"
    import IconXMark from "./icons/IconXMark.svelte"
    import Section from "./atomic/Section.svelte"
    import DrawerScoringInfo from "./atomic/DrawerScoringInfo.svelte"
    import Button from "./Button.svelte"

    let vggtArticles = $page.data.vggtArticles
    let vggtVariables = $page.data.vggtVariables

    $: variableInfo = vggtVariables.filter(v => v.number == $currentVariable)[0]
    $: deal = $deals.find(deal => deal.id == $currentDeal) ?? undefined

    let score = null
    let status = "no_score"

    $: console.log(vggtArticles)

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
                    <h1 class="text-a-xl font-semibold">Variable {$currentVariable} - {variableInfo.name}</h1>
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
                {#each variableInfo.score_options as value}
                    {@const label = scoreLabels[value] ?? ""}
                    {@const description = vggtInfo[$currentVariable].score_meaning[value] ?? ""}
                    <DrawerScoringItem {label} {description} {value} {score} on:onClick={selectScore} />
                {/each}
            </div>

            <Section title="Show more details" extraClass="pl-0 underline underline-offset-4" open={false}>
                <!-- Help -->
                 {#if vggtInfo[$currentVariable].score_help.length > 0}
                    <h3>Help</h3>
                    <ul>
                        {#each vggtInfo[$currentVariable].score_help as help}
                            <li>{help}</li>
                        {/each}
                    </ul>
                 {/if}

                <!-- Resources -->
                <h3>Resources (VGGTs articles linked to this variable)</h3>
                {#each variableInfo.articles as id}
                    {@const item = vggtArticles.find(i => i.id == id)}
                    <ul>
                        <li class="font-semibold">Article {item.chapter}.{item.article} (Chapter {item.chapter}: {item.title})</li>
                        <ul>
                            <li>{item.description}</li>
                        </ul>
                    </ul>
                {/each}
            </Section>

            <!-- LM Info -->
            <h2 class="mt-4">Land Matrix information</h2>
            <DrawerScoringInfo {deal} fields={variableInfo.landmatrix_fields} />
            {#if variableInfo?.landmatrix_additional_fields.length > 0}
                <h4 class="my-4 text-sm font-medium text-a-gray-500">Additional fields</h4>
                <DrawerScoringInfo {deal} fields={variableInfo.landmatrix_additional_fields} />
            {/if}
            <h2 class="mt-10">Deal main information</h2>
            <DrawerScoringInfo {deal} main_info={true} />
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