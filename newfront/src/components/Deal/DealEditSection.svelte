<script lang="ts">
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
          <EditField {fieldname} bind:value={deal[fieldname]} />
        {/each}
      </div>
    {/each}
    <slot />
  </form>
</section>
