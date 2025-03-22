<script lang="ts">
  import type { DataSource } from "$lib/types/data"

  import DisplayField from "$components/Fields/DisplayField.svelte"
  import SubmodelPopup from "$components/Quotations/SubmodelPopup.svelte"

  interface Props {
    dataSource: DataSource
    label: string
  }

  let { dataSource, label }: Props = $props()
</script>

<SubmodelPopup>
  <h5 class="heading5">
    {label}
    <small class="text-sm text-gray-500">
      #{dataSource.nid}
    </small>
  </h5>

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
</SubmodelPopup>
