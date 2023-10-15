<script lang="ts">
  import type { Section } from "$lib/sections"
  import type { Deal } from "$lib/types/deal"

  import ExpandableEditField from "$components/Fields/ExpandableEditField.svelte"

  export let deal: Deal
  export let sections: Section[] = []
  export let id: string
</script>

<section>
  <form {id}>
    {#each sections as subsection}
      <div class="mt-10 space-y-4 border-t-2 first:border-t-0">
        <h3 class="my-0 pt-8 text-[26px]">{subsection.name}</h3>
        {#each subsection.fields as field}
          <ExpandableEditField {field} bind:deal />
        {/each}
      </div>
    {/each}
    <slot />
  </form>
</section>
