<script lang="ts">
  import { getStatusColor } from "$lib/accountability/helpers"

  interface Props {
    variables?: {
      vggt_variable: number
      status: "no_score" | "pending" | "validated" | "no_data"
      score: number | null
      assignee: { id: number; name: string; initials: string } | null
    }
  }

  let { variables = [] }: Props = $props()
</script>

<div class="flex max-w-48 justify-between">
  {#each variables as variable}
    {@const color = getStatusColor(variable.status)}
    <div class="h-2.5 w-2.5 rounded-full {color}"></div>
  {/each}
</div>
