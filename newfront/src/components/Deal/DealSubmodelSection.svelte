<script lang="ts">
  import { _ } from "svelte-i18n";
  import { isEmpty } from "$lib/helpers";
  import type { Contract, DataSource, Location } from "$lib/types/deal";
  import DisplayField from "$components/Fields/DisplayField.svelte";

  export let model: string;
  export let modelName: string;
  export let entries: Array<Contract | DataSource | Location> = [];

  $: fields = {
    location: [
      "level_of_accuracy",
      "name",
      "description",
      "point",
      "facility_name",
      "comment",
    ],
    contract: ["number", "date", "expiration_date", "agreement_duration", "comment"],
    datasource: [
      "type",
      "url",
      "file",
      "file_not_public",
      "publication_title",
      "date",
      "name",
      "company",
      "email",
      "phone",
      "includes_in_country_verified_information",
      "open_land_contracts_id",
      "comment",
    ],
  }[model];

  let wrapperClasses = $$slots.default ? "w-full lg:w-1/2" : "w-full";
</script>

{#if entries.length > 0}
  <section class="flex flex-wrap h-full">
    <div class={wrapperClasses}>
      {#each entries as entry, index}
        <div class="{model}-entry">
          <h3>
            {index + 1}. {$_(modelName)}
            <small class="text-sm text-gray-500">#{entry.id}</small>
          </h3>
          {#each fields as fieldname}
            {#if !isEmpty(entry[fieldname])}
              <DisplayField
                {fieldname}
                value={entry[fieldname]}
                {model}
                :file-not-public="entry.file_not_public"
              />
            {/if}
          {/each}
        </div>
      {/each}
    </div>
    <slot />
  </section>
{/if}
