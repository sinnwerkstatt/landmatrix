<script lang="ts">
  import { dealChoices } from "$lib/fieldChoices"
  import type { InvolvedActor } from "$lib/types/data"

  import SourcesDisplayButton from "$components/Quotations/SourcesDisplayButton.svelte"

  interface Props {
    value: InvolvedActor[]
    fieldname?: string
  }

  let { value, fieldname = "" }: Props = $props()
</script>

<ul class="my-3">
  {#each value ?? [] as actor, i}
    <li class="my-2">
      <span>{actor.name}</span>
      {#if actor.role}
        <span class="text-sm font-light">
          {$dealChoices.actors.find(a => a.value === actor.role)?.label ?? "-"}
        </span>
      {/if}

      <SourcesDisplayButton path={[fieldname, i]} />
    </li>
  {/each}
</ul>
