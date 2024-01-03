<script lang="ts">
  import { fieldChoices } from "$lib/stores"
  import type { InvolvedActor } from "$lib/types/newtypes"

  import { LABEL_CLASS, VALUE_CLASS, WRAPPER_CLASS } from "$components/Fields/consts"
  import Label2 from "$components/Fields/Display2/Label2.svelte"

  export let value: InvolvedActor[]
  export let fieldname: string
  export let label = ""
  export let wrapperClass = WRAPPER_CLASS
  export let labelClass = LABEL_CLASS
  export let valueClass = VALUE_CLASS
</script>

{#if value}
  <div class={wrapperClass} data-fieldname={fieldname}>
    {#if label}
      <Label2 value={label} class={labelClass} />
    {/if}
    <div class={valueClass}>
      <ul>
        {#each value as actor}
          <li>
            <span>{actor.name}</span>
            {#if actor.role}
              <span class="text-sm font-light">
                {$fieldChoices.deal.actors.find(a => a.value === actor.role)?.label ??
                  "-"}
              </span>
            {/if}
          </li>
        {/each}
      </ul>
    </div>
  </div>
{/if}
