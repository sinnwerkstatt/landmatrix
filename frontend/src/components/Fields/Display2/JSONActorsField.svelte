<script lang="ts">
  import { fieldChoices } from "$lib/stores"
  import type { InvolvedActor } from "$lib/types/data"

  export let value: InvolvedActor[]
</script>

<ul class="my-3">
  {#each value as actor}
    <li class="my-2">
      <span>{actor.name}</span>
      {#if actor.role}
        <span class="text-sm font-light">
          {$fieldChoices.deal.actors.find(a => a.value === actor.role)?.label ?? "-"}
        </span>
      {/if}
    </li>
  {/each}
</ul>
