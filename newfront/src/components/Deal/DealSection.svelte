<script lang="ts">
  import { _ } from "svelte-i18n";
  import DisplayField from "$components/Fields/DisplayField.svelte";
  import { isEmpty } from "$lib/helpers";

  export let deal;
  export let sections = [];

  function sectionFieldsWithValues(subsection) {
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
