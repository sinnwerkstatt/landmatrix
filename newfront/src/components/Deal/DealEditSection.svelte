<script lang="ts">
  import { slide } from "svelte/transition"

  import type { Section } from "$lib/sections"
  import type { Deal } from "$lib/types/deal"

  import EditField from "$components/Fields/EditField.svelte"

  export let deal: Deal
  export let sections: Section[] = []
  export let id: string
</script>

<section>
  <form {id}>
    {#each sections as subsection}
      <div class="mt-2 space-y-4">
        <h3 class="my-0">{subsection.name}</h3>
        {#each subsection.fields as fieldname}
          {#if typeof fieldname === "object"}
            <EditField fieldname={fieldname.name} bind:value={deal[fieldname.name]} />
            {#if deal[fieldname.name] === true}
              <div transition:slide class="pl-4">
                {#each fieldname.fields as connectedField}
                  <EditField
                    fieldname={connectedField}
                    bind:value={deal[connectedField]}
                  />
                {/each}
              </div>
            {/if}
          {:else}
            <EditField {fieldname} bind:value={deal[fieldname]} />
          {/if}
        {/each}
      </div>
    {/each}
    <slot />
  </form>
</section>
