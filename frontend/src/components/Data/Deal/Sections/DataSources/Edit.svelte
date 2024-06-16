<script lang="ts">
  import { _ } from "svelte-i18n"

  import { type DataSource, type DealHull } from "$lib/types/data"

  import SubmodelEditField from "$components/Fields/SubmodelEditField.svelte"

  import Entry from "./Entry.svelte"

  export let deal: DealHull

  const createDataSource = (nid: string): DataSource => ({
    id: null!,
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
    dealversion: null!,
  })
</script>

<SubmodelEditField
  label={$_("Data Source")}
  bind:entries={deal.selected_version.datasources}
  createEntry={createDataSource}
  entryComponent={Entry}
/>
