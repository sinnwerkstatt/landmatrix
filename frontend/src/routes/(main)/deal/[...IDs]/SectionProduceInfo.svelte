<script lang="ts">
  import { _ } from "svelte-i18n"

  import { fieldChoices } from "$lib/stores"
  import type { DealVersion2 } from "$lib/types/newtypes"

  import BooleanField from "$components/Fields/Display2/BooleanField.svelte"
  import JSONCurrentDateChoiceField from "$components/Fields/Display2/JSONCurrentDateChoiceField.svelte"
  import TextField from "$components/Fields/Display2/TextField.svelte"

  import Subsection from "./Subsection.svelte"

  export let version: DealVersion2
</script>

<section>
  <Subsection
    title={$_("Detailed crop, animal and mineral information")}
    fields={[
      version.crops,
      version.crops_comment,
      version.animals,
      version.animals_comment,
      version.mineral_resources,
      version.mineral_resources_comment,
    ]}
  >
    <JSONCurrentDateChoiceField
      fieldname="crops"
      label={$_("Crops area/yield/export")}
      value={version.crops}
      choices={$fieldChoices.deal.crops}
    />
    {JSON.stringify(version.crops)}

    <TextField
      fieldname="crops_comment"
      label={$_("Comment on crops")}
      value={version.crops_comment}
    />
    <TextField
      fieldname="animals"
      label={$_("Animals")}
      value={version.animals}
      choices={$fieldChoices.deal.animals}
      multipleChoices
    />
    <TextField
      fieldname="animals_comment"
      label={$_("Comment on animals")}
      value={version.animals_comment}
    />
    <TextField
      fieldname="mineral_resources"
      label={$_("Mineral resources")}
      value={version.mineral_resources}
      choices={$fieldChoices.deal.minerals}
      multipleChoices
    />
    <TextField
      fieldname="mineral_resources_comment"
      label={$_("Comment on mineral resources")}
      value={version.mineral_resources_comment}
    />
  </Subsection>
  <Subsection
    title={$_("Detailed contract farming crop and animal information")}
    fields={[
      version.contract_farming_crops,
      version.contract_farming_crops_comment,
      version.contract_farming_animals,
      version.contract_farming_animals_comment,
    ]}
  >
    <TextField
      fieldname="contract_farming_crops"
      label={$_("Contract farming crops")}
      value={version.contract_farming_crops}
    />
    <TextField
      fieldname="contract_farming_crops_comment"
      label={$_("Comment on contract farming crops")}
      value={version.contract_farming_crops_comment}
    />
    <TextField
      fieldname="contract_farming_animals"
      label={$_("Contract farming animals")}
      value={version.contract_farming_animals}
    />
    <TextField
      fieldname="contract_farming_animals_comment"
      label={$_("Comment on contract farming animals")}
      value={version.contract_farming_animals_comment}
    />
  </Subsection>
  <Subsection
    title={$_("Detailed electricity generation information")}
    fields={[version.electricity_generation, version.electricity_generation_comment]}
  >
    <TextField
      fieldname="electricity_generation"
      label={$_("Electricity generation")}
      value={version.electricity_generation}
      choices={$fieldChoices.deal.electricity_generation}
      multipleChoices
    />
    <TextField
      fieldname="electricity_generation_comment"
      label={$_("Comment on electricity generation")}
      value={version.electricity_generation_comment}
    />
  </Subsection>
  <Subsection
    title={$_("Detailed carbon sequestration information")}
    fields={[version.carbon_sequestration, version.carbon_sequestration_comment]}
  >
    <TextField
      fieldname="carbon_sequestration"
      label={$_("Carbon sequestration")}
      value={version.carbon_sequestration}
      choices={$fieldChoices.deal.carbon_sequestration}
      multipleChoices
    />
    <TextField
      fieldname="carbon_sequestration_comment"
      label={$_("Comment on carbon sequestration")}
      value={version.carbon_sequestration_comment}
    />
  </Subsection>
  <Subsection
    title={$_("Use of produce")}
    fields={[
      version.domestic_use,
      version.export,
      version.export_country1,
      version.export_country1_ratio,
      version.export_country2,
      version.export_country2_ratio,
      version.export_country3,
      version.export_country3_ratio,
    ]}
  >
    <TextField
      fieldname="domestic_use"
      label={$_("Domestic use")}
      value={version.domestic_use}
    />
    <TextField fieldname="export" label={$_("Export")} value={version.export} />
    <TextField
      fieldname="export_country1"
      label={$_("Counrtry 1")}
      value={version.export_country1}
    />
    <TextField
      fieldname="export_country1_ratio"
      label={$_("Counrtry 1 ratio")}
      value={version.export_country1_ratio}
    />
    <TextField
      fieldname="export_country2"
      label={$_("Counrtry 2")}
      value={version.export_country2}
    />
    <TextField
      fieldname="export_country2_ratio"
      label={$_("Counrtry 2 ratio")}
      value={version.export_country2_ratio}
    />
    <TextField
      fieldname="export_country3"
      label={$_("Counrtry 3")}
      value={version.export_country3}
    />
    <TextField
      fieldname="export_country3__ratio"
      label={$_("Counrtry 3 ratio")}
      value={version.export_country3_ratio}
    />
  </Subsection>
  <Subsection
    title={$_("In country processing of produce")}
    fields={[
      version.in_country_processing,
      version.in_country_processing_comment,
      version.in_country_processing_facilities,
      version.in_country_end_products,
    ]}
  >
    <BooleanField
      fieldname="in_country_processing"
      label={$_("In country processing of produce")}
      value={version.in_country_processing}
    />
    <TextField
      fieldname="in_country_processing_comment"
      label={$_("Comment on in country processing of produce")}
      value={version.in_country_processing_comment}
    />
    <TextField
      fieldname="in_country_processing_facilities"
      label={$_("In country processing facilities")}
      value={version.in_country_processing_facilities}
    />
    <TextField
      fieldname="in_country_end_products"
      label={$_("In country end products")}
      value={version.in_country_end_products}
    />
  </Subsection>
</section>
