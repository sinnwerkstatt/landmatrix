<script lang="ts">
  import { _ } from "svelte-i18n"

  import { fieldChoices } from "$lib/stores"
  import type { DealVersion2 } from "$lib/types/newtypes"

  import TextField from "$components/Fields/Display2/TextField.svelte"

  import Subsection from "./Subsection.svelte"

  export let version: DealVersion2
</script>

<section>
  <Subsection
    title={$_("Former land owner (not by constitution)")}
    fields={[version.former_land_owner, version.former_land_owner_comment]}
  >
    <TextField
      fieldname="former_land_owner"
      label={$_("Former land owner")}
      value={version.former_land_owner}
      choices={$fieldChoices.deal.former_land_owner}
      multipleChoices
    />
    <TextField
      fieldname="former_land_owner_comment"
      label={$_("Comment on former land owner")}
      value={version.former_land_owner_comment}
    />
  </Subsection>
  <Subsection
    title={$_("Former land use")}
    fields={[version.former_land_use, version.former_land_use_comment]}
  >
    <TextField
      fieldname="former_land_use"
      label={$_("Former land use")}
      value={version.former_land_use}
      choices={$fieldChoices.deal.former_land_use}
      multipleChoices
    />
    <TextField
      fieldname="former_land_use_comment"
      label={$_("Comment on former land use")}
      value={version.former_land_use_comment}
    />
  </Subsection>
  <Subsection
    title={$_("Former land cover")}
    fields={[version.former_land_cover, version.former_land_cover_comment]}
  >
    <TextField
      fieldname="former_land_cover"
      label={$_("Former land cover")}
      value={version.former_land_cover}
      choices={$fieldChoices.deal.former_land_cover}
      multipleChoices
    />
    <TextField
      fieldname="former_land_cover_comment"
      label={$_("Comment on former land cover")}
      value={version.former_land_cover_comment}
    />
  </Subsection>
</section>
