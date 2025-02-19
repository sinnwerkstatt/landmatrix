<script lang="ts">
  import { _ } from "svelte-i18n"

  import type { DataSource, DataSourceType } from "$lib/types/data"

  import LowLevelNullBooleanField from "$components/Fields/Edit2/LowLevelNullBooleanField.svelte"
  import EditField from "$components/Fields/EditField.svelte"

  interface Props {
    entry: DataSource
    onchange?: () => void
  }

  let { entry = $bindable(), onchange }: Props = $props()

  const TYPES_REQUIRING_FILE_UPLOAD: DataSourceType[] = [
    "COMPANY_SOURCES",
    "CONTRACT",
    "CONTRACT_FARMING_AGREEMENT",
    "GOVERNMENT_SOURCES",
    "MEDIA_REPORT",
    "RESEARCH_PAPER_OR_POLICY_REPORT",
  ]

  let fileUploadRequired = $derived(
    entry.type && TYPES_REQUIRING_FILE_UPLOAD.includes(entry.type),
  )
</script>

<EditField fieldname="datasource.type" bind:value={entry.type} showLabel {onchange} />

<EditField fieldname="datasource.url" bind:value={entry.url} showLabel {onchange} />

<EditField
  fieldname="datasource.file"
  showLabel
  {onchange}
  bind:value={entry.file}
  extras={{ required: fileUploadRequired }}
>
  <label for={undefined} class="my-2 flex items-center gap-2">
    <LowLevelNullBooleanField
      bind:value={entry.file_not_public}
      name="datasource.file_not_public"
      {onchange}
    />
    {$_("Keep PDF not public")}
  </label>
</EditField>

<EditField
  fieldname="datasource.publication_title"
  bind:value={entry.publication_title}
  showLabel
  {onchange}
/>

<EditField fieldname="datasource.date" bind:value={entry.date} showLabel {onchange} />

<EditField fieldname="datasource.name" bind:value={entry.name} showLabel {onchange} />

<EditField
  fieldname="datasource.company"
  bind:value={entry.company}
  showLabel
  {onchange}
/>

<EditField fieldname="datasource.email" bind:value={entry.email} showLabel {onchange} />

<EditField fieldname="datasource.phone" bind:value={entry.phone} showLabel {onchange} />

<EditField
  fieldname="datasource.includes_in_country_verified_information"
  bind:value={entry.includes_in_country_verified_information}
  showLabel
  {onchange}
/>

<EditField
  fieldname="datasource.open_land_contracts_id"
  bind:value={entry.open_land_contracts_id}
  showLabel
  {onchange}
/>

<EditField
  fieldname="datasource.comment"
  bind:value={entry.comment}
  showLabel
  {onchange}
/>
