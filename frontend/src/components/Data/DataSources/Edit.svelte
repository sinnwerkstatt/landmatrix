<script lang="ts">
  import { _ } from "svelte-i18n"

  import {
    type DataSource,
    type DealVersion2,
    type InvestorVersion2,
  } from "$lib/types/data"
  import { isEmptySubmodel } from "$lib/utils/dataProcessing"

  import SubmodelEditField from "$components/Fields/SubmodelEditField.svelte"

  import Entry from "./Entry.svelte"

  export let version: DealVersion2 | InvestorVersion2

  const createDataSource = (nid: string): DataSource =>
    ({
      // id: null!,
      nid,
      type: "" as never,
      url: "",
      file: null!,
      file_not_public: false,
      publication_title: "",
      date: null,
      name: "",
      company: "",
      email: "",
      phone: "",
      includes_in_country_verified_information: null,
      open_land_contracts_id: "",
      comment: "",
      // dealversion: null!,
      // investorversion: null!,
    }) as unknown as DataSource

  $: isEmpty = (dataSource: DataSource) =>
    isEmptySubmodel(dataSource, ["dealversion", "investorversion", "file_not_public"])
</script>

<SubmodelEditField
  label={$_("Data Source")}
  bind:entries={version.datasources}
  createEntry={createDataSource}
  {isEmpty}
  entryComponent={Entry}
/>
