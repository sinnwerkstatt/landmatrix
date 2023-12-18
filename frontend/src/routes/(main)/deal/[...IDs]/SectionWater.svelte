<script lang="ts">
  import { _ } from "svelte-i18n"

  import { fieldChoices } from "$lib/stores"
  import type { DealVersion2 } from "$lib/types/newtypes"

  import BooleanField from "$components/Fields/Display2/BooleanField.svelte"
  import TextField from "$components/Fields/Display2/TextField.svelte"

  import Subsection from "./Subsection.svelte"

  export let version: DealVersion2
</script>

<section>
  <Subsection
    title={$_("Water extraction envisaged")}
    fields={[
      version.water_extraction_envisaged,
      version.water_extraction_envisaged_comment,
    ]}
  >
    <BooleanField
      fieldname="water_extraction_envisaged"
      label={$_("Water extraction envisaged")}
      value={version.water_extraction_envisaged}
    />
    <TextField
      fieldname="water_extraction_envisaged_comment"
      label={$_("Comment on water extraction envisaged")}
      value={version.water_extraction_envisaged_comment}
    />
  </Subsection>
  <Subsection
    title={$_("Source of water extraction")}
    fields={[
      version.source_of_water_extraction,
      version.source_of_water_extraction_comment,
    ]}
  >
    <TextField
      fieldname="source_of_water_extraction"
      label={$_("Source of water extraction")}
      value={version.source_of_water_extraction}
      choices={$fieldChoices.deal.water_source}
      multipleChoices
    />
    <TextField
      fieldname="source_of_water_extraction_comment"
      label={$_("Comment on source of water extraction")}
      value={version.source_of_water_extraction_comment}
    />
  </Subsection>
  <Subsection
    title={$_(
      "How much do investors pay for water and the use of water infrastructure?",
    )}
    fields={[version.how_much_do_investors_pay_comment]}
  >
    <TextField
      fieldname="how_much_do_investors_pay_comment"
      label={$_("Comment on how much do investors pay")}
      value={version.how_much_do_investors_pay_comment}
    />
  </Subsection>
  <Subsection
    title={$_("How much water is extracted?")}
    fields={[
      version.water_extraction_amount,
      version.water_extraction_amount_comment,
      version.use_of_irrigation_infrastructure,
      version.use_of_irrigation_infrastructure_comment,
      version.water_footprint,
    ]}
  >
    <TextField
      fieldname="water_extraction_amount"
      label={$_("Water extraction amount")}
      value={version.water_extraction_amount}
    />
    <TextField
      fieldname="water_extraction_amount_comment"
      label={$_("Comment on water extraction amount")}
      value={version.water_extraction_amount_comment}
    />
    <BooleanField
      fieldname="use_of_irrigation_infrastructure"
      label={$_("Use of irrigation infrastructure")}
      value={version.use_of_irrigation_infrastructure}
    />
    <TextField
      fieldname="use_of_irrigation_infrastructure_comment"
      label={$_("Comment on use of irrigation infrastructure")}
      value={version.use_of_irrigation_infrastructure_comment}
    />
    <TextField
      fieldname="water_footprint"
      label={$_("Water footprint")}
      value={version.water_footprint}
    />
  </Subsection>
</section>
