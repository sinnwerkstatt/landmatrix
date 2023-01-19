<script lang="ts">
  import { isEmpty } from "$lib/helpers"
  import type { Section } from "$lib/sections"
  import type { Deal } from "$lib/types/deal"

  import ExpandableDisplayField from "$components/Fields/ExpandableDisplayField.svelte"

  export let deal: Deal
  export let sections: Section[] = []

  function sectionFieldsWithValues(subsection: Section) {
    return subsection.fields.filter(field =>
      typeof field === "object" ? !isEmpty(deal[field.name]) : !isEmpty(deal[field]),
    )
  }

  $: subsectionsWithAtLeastOneField = sections.filter(
    section => sectionFieldsWithValues(section).length > 0,
  )
</script>

<section>
  {#each subsectionsWithAtLeastOneField as subsection}
    <div class="mt-2 space-y-4">
      <h3 class="my-0">{subsection.name}</h3>
      {#each sectionFieldsWithValues(subsection) as field}
        <ExpandableDisplayField {field} {deal} />
      {/each}
    </div>
  {/each}
  <slot />
</section>
