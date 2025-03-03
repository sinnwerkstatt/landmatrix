<script lang="ts">
  import { _ } from "svelte-i18n"

  import type { components } from "$lib/openAPI"
  import type { DealVersion, InvestorVersion, Model } from "$lib/types/data"

  import DisplayField from "$components/Fields/DisplayField.svelte"
  import SubmodelDisplayField from "$components/Fields/SubmodelDisplayField.svelte"

  interface Props {
    version: DealVersion | InvestorVersion
    model: Model
  }

  let { version, model }: Props = $props()

  type DataSource =
    | components["schemas"]["InvestorDataSource"]
    | components["schemas"]["DealDataSource"]
</script>

<SubmodelDisplayField
  {model}
  fieldname="datasources"
  label={$_("Data source")}
  entries={version.datasources}
>
  {#snippet children(datasource: DataSource)}
    <DisplayField fieldname="datasource.type" showLabel value={datasource.type} />
    <DisplayField fieldname="datasource.url" showLabel value={datasource.url} />
    <DisplayField
      fieldname="datasource.file"
      showLabel
      value={datasource.file}
      extras={{ notPublic: datasource.file_not_public }}
    />
    <DisplayField
      fieldname="datasource.publication_title"
      showLabel
      value={datasource.publication_title}
    />
    <DisplayField fieldname="datasource.date" showLabel value={datasource.date} />
    <DisplayField fieldname="datasource.name" showLabel value={datasource.name} />
    <DisplayField fieldname="datasource.company" showLabel value={datasource.company} />
    <DisplayField fieldname="datasource.email" showLabel value={datasource.email} />
    <DisplayField fieldname="datasource.phone" showLabel value={datasource.phone} />
    <DisplayField
      fieldname="datasource.includes_in_country_verified_information"
      showLabel
      value={datasource.includes_in_country_verified_information}
    />
    <DisplayField
      fieldname="datasource.open_land_contracts_id"
      showLabel
      value={datasource.open_land_contracts_id}
    />
    <DisplayField fieldname="datasource.comment" showLabel value={datasource.comment} />
  {/snippet}
</SubmodelDisplayField>
