<script lang="ts">
  import { _ } from "svelte-i18n"

  import { isEmpty } from "$lib/helpers"
  import type { Section } from "$lib/sections"
  import type { Deal } from "$lib/types/deal"

  import DisplayField from "$components/Fields/DisplayField.svelte"

  export let deal: Deal
  export let sections: Section[] = []

  function sectionFieldsWithValues(subsection: Section) {
    return subsection.fields.filter(field => !isEmpty(deal[field]))
  }
  $: subsectionsWithAtLeastOneField = sections.filter(
    section => sectionFieldsWithValues(section).length > 0,
  )
</script>

<section>
  {#each subsectionsWithAtLeastOneField as subsection}
    <div class="mt-2 space-y-4">
      <h3 class="my-0">{subsection.name}</h3>
      {#each sectionFieldsWithValues(subsection) as fieldname}
        <DisplayField {fieldname} value={deal[fieldname]} showLabel />
      {/each}
    </div>
  {/each}
  <slot />
</section>
