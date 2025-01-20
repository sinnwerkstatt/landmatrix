<script lang="ts">
  import { getStatusColor } from "$lib/accountability/helpers"

  import Badge from "./Badge.svelte"

  interface Props {
    value?: "to_score" | "pending" | "validated"
    type?: "badge" | "dot"
  }

  let { value = "to_score", type = "badge" }: Props = $props()

  const statuses = [
    { value: "TO_SCORE", label: "To score", color: "neutral", variant: "light" },
    {
      value: "WAITING",
      label: "Waiting for review",
      color: "primary",
      variant: "light",
    },
    { value: "VALIDATED", label: "Validated", color: "success", variant: "light" },
    { value: "NO_DATA", label: "No data", color: "neutral", variant: "filled" },
  ]

  let status = $derived(statuses.find(e => e.value == value))
  let bg = $derived(getStatusColor(value))
</script>

{#if type == "dot"}
  <div class="flex items-center gap-1.5">
    <div class="h-3 w-3 rounded-full {bg}"></div>
    <span>{status?.label}</span>
  </div>
{:else}
  <Badge label={status?.label} color={status?.color} variant={status?.variant} />
{/if}
