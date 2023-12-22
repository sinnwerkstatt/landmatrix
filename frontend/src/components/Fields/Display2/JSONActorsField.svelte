<script lang="ts">
  import { fieldChoices } from "$lib/stores"
  import type { InvolvedActor } from "$lib/types/newtypes"

  import Label2 from "$components/Fields/Display2/Label2.svelte"

  export let value: InvolvedActor[]
  export let fieldname: string
  export let label = ""
  export let wrapperClass = "mb-3 flex flex-wrap leading-5"
  export let labelClass = "md:w-5/12 lg:w-4/12"
  export let valueClass = "text-gray-700 dark:text-white md:w-7/12 lg:w-8/12"
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
