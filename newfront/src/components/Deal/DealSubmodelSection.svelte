<script lang="ts">
  import { _ } from "svelte-i18n";
  import { isEmpty } from "$lib/helpers";
  import DisplayField from "../Fields/DisplayField.svelte";

  export let model;
  export let modelName;
  export let entries = [];
  export let fields;

  let wrapperClasses = "col-md-12 col-lg-7 col-xl-6"; // TODO different on locations! w-full
  wrapperClasses = "w-full";
</script>

{#if entries.length > 0}
  <section class="flex">
    <div class={wrapperClasses}>
      {#each entries as entry, index}
        <div class="panel-body">
          <h3>
            {$_(modelName)} <small class="text-sm text-gray-500">#{entry.id}</small>
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
      <slot />
    </div>
  </section>
{/if}
