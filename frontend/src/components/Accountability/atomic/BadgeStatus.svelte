<script lang="ts">
    import { getStatusColor } from "$lib/accountability/helpers"

    import Badge from "./Badge.svelte"

    export let value:"to_score"|"pending"|"validated" = "to_score"
    export let type:"badge"|"dot" = "badge"

    const statuses = [
        { value: "no_score", label: "To score", color: "neutral", variant: "light" },
        { value: "pending", label: "Waiting for review", color: "primary", variant: "light" },
        { value: "validated", label: "Validated", color: "success", variant: "light" },
        { value: "no_data", label: "No data", color: "neutral", variant: "filled" }
    ]

    $: status = statuses.find(e => e.value == value)
    $: bg = getStatusColor(value)

</script>

{#if type == "dot"}
    <div class="flex items-center gap-1.5">
        <div class="h-3 w-3 rounded-full {bg}"></div>
        <span>{status?.label}</span>
    </div>
{:else}
    <Badge label={status?.label} color={status?.color} variant={status?.variant} />
{/if}
