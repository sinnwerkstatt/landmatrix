<script lang="ts">
  import { dealChoices } from "$lib/fieldChoices"
  import type { InvolvedActor } from "$lib/types/data"

  interface Props {
    value: InvolvedActor[]
  }

  let { value }: Props = $props()
</script>

<ul class="my-3">
  {#each value as actor}
    <li class="my-2">
      <span>{actor.name}</span>
      {#if actor.role}
        <span class="text-sm font-light">
          {$dealChoices.actors.find(a => a.value === actor.role)?.label ?? "-"}
        </span>
      {/if}
    </li>
  {/each}
</ul>
