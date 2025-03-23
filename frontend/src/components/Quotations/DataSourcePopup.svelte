<script lang="ts">
  import type { DataSource } from "$lib/types/data"
  import type { SubmodelEntry } from "$lib/utils/dataProcessing"

  import DisplayField from "$components/Fields/DisplayField.svelte"

  interface Props {
    entry: SubmodelEntry
  }

  let { entry }: Props = $props()

  const dataSource = $derived(entry as DataSource)
</script>

<DisplayField fieldname="datasource.type" showLabel value={dataSource.type} />
<DisplayField fieldname="datasource.url" showLabel value={dataSource.url} />
<DisplayField
  fieldname="datasource.file"
  showLabel
  value={dataSource.file}
  extras={{ notPublic: dataSource.file_not_public }}
/>
<DisplayField
  fieldname="datasource.publication_title"
  showLabel
  value={dataSource.publication_title}
/>
<DisplayField fieldname="datasource.date" showLabel value={dataSource.date} />
<DisplayField fieldname="datasource.name" showLabel value={dataSource.name} />
<DisplayField fieldname="datasource.company" showLabel value={dataSource.company} />
<DisplayField fieldname="datasource.email" showLabel value={dataSource.email} />
<DisplayField fieldname="datasource.phone" showLabel value={dataSource.phone} />
<DisplayField
  fieldname="datasource.includes_in_country_verified_information"
  showLabel
  value={dataSource.includes_in_country_verified_information}
/>
<DisplayField
  fieldname="datasource.open_land_contracts_id"
  showLabel
  value={dataSource.open_land_contracts_id}
/>
<DisplayField fieldname="datasource.comment" showLabel value={dataSource.comment} />
