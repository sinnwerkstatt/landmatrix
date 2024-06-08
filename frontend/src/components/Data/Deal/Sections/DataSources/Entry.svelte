<script lang="ts">
  import { _ } from "svelte-i18n"

  import LowLevelNullBooleanField from "$components/Fields/Edit2/LowLevelNullBooleanField.svelte"
  import EditField from "$components/Fields/EditField.svelte"

  export let entry: Record<string, unknown>
</script>

<EditField fieldname="datasource.type" bind:value={entry.type} showLabel />

<EditField fieldname="datasource.url" bind:value={entry.url} showLabel />

<EditField fieldname="datasource.file" showLabel bind:value={entry.file}>
  <label for={undefined} class="my-2 flex items-center gap-2">
    <LowLevelNullBooleanField
      bind:value={entry.file_not_public}
      fieldname="datasource.file_not_public"
    />
    {$_("Keep PDF not public")}
  </label>
</EditField>

<EditField
  fieldname="datasource.publication_title"
  bind:value={entry.publication_title}
  showLabel
/>

<EditField fieldname="datasource.date" bind:value={entry.date} showLabel />

<EditField fieldname="datasource.name" bind:value={entry.name} showLabel />

<EditField fieldname="datasource.company" bind:value={entry.company} showLabel />

<EditField fieldname="datasource.email" bind:value={entry.email} showLabel />

<EditField fieldname="datasource.phone" bind:value={entry.phone} showLabel />

<EditField
  fieldname="datasource.includes_in_country_verified_information"
  bind:value={entry.includes_in_country_verified_information}
  showLabel
/>

<EditField
  fieldname="datasource.open_land_contracts_id"
  bind:value={entry.open_land_contracts_id}
  showLabel
/>

<EditField fieldname="datasource.comment" bind:value={entry.comment} showLabel />
