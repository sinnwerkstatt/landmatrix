<script lang="ts">
  import { _ } from "svelte-i18n";
  import type { DealSection } from "$lib/deal_sections";
  import { isEmpty } from "$lib/helpers";
  import type { Deal } from "$lib/types/deal";
  import DisplayField from "$components/Fields/DisplayField.svelte";

  export let deal: Deal;
  export let sections: DealSection[] = [];

  function sectionFieldsWithValues(subsection: DealSection) {
    return subsection.fields.filter((field) => !isEmpty(deal[field]));
  }
  $: subsectionsWithAtLeastOneField = sections.filter(
    (section) => sectionFieldsWithValues(section).length > 0
  );
</script>

<section>
  {#each subsectionsWithAtLeastOneField as subsection}
    <div class="space-y-4 mt-2">
      <h3 class="my-0">{$_(subsection.name)}</h3>
      {#each sectionFieldsWithValues(subsection) as fieldname}
        <DisplayField {fieldname} value={deal[fieldname]} />
      {/each}
    </div>
  {/each}
  <slot />
</section>
