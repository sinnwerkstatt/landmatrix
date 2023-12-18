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
    title={$_("Names of communities / indigenous peoples affected")}
    fields={[
      version.name_of_community,
      version.name_of_indigenous_people,
      version.people_affected_comment,
    ]}
  >
    <TextField
      fieldname="name_of_community"
      label={$_("Name of community")}
      value={version.name_of_community}
    />
    <TextField
      fieldname="name_of_indigenous_people"
      label={$_("Name of indigenous people")}
      value={version.name_of_indigenous_people}
    />
    <TextField
      fieldname="people_affected_comment"
      label={$_("Comment on people affected")}
      value={version.people_affected_comment}
    />
  </Subsection>
  <Subsection
    title={$_("Recognition status of community land tenure")}
    fields={[version.recognition_status, version.recognition_status_comment]}
  >
    <TextField
      fieldname="recognition_status"
      label={$_("Recognition status")}
      value={version.recognition_status}
      choices={$fieldChoices.deal.recognition_status}
      multipleChoices
    />
    <TextField
      fieldname="recognition_status_comment"
      label={$_("Comment on recognition status")}
      value={version.recognition_status_comment}
    />
  </Subsection>
  <Subsection
    title={$_("Consultation of local community")}
    fields={[version.community_consultation, version.community_consultation_comment]}
  >
    <TextField
      fieldname="community_consultation"
      label={$_("Community consultation")}
      value={version.community_consultation}
      choices={$fieldChoices.deal.community_consultation}
      multipleChoices
    />
    <TextField
      fieldname="community_consultation_comment"
      label={$_("Comment on community consultation")}
      value={version.community_consultation_comment}
    />
  </Subsection>
  <Subsection
    title={$_("How did the community react?")}
    fields={[version.community_reaction, version.community_reaction_comment]}
  >
    <TextField
      fieldname="community_reaction"
      label={$_("Community reaction")}
      value={version.community_reaction}
      choices={$fieldChoices.deal.community_reaction}
      multipleChoices
    />
    <TextField
      fieldname="community_reaction_comment"
      label={$_("Comment on community reaction")}
      value={version.community_reaction_comment}
    />
  </Subsection>
  <Subsection
    title={$_("Presence of land conflicts")}
    fields={[version.land_conflicts, version.land_conflicts_comment]}
  >
    <TextField
      fieldname="land_conflicts"
      label={$_("Land conflicts")}
      value={version.land_conflicts}
    />
    <TextField
      fieldname="land_conflicts_comment"
      label={$_("Comment on land conflicts")}
      value={version.land_conflicts_comment}
    />
  </Subsection>

  <Subsection
    title={$_("Displacement of people")}
    fields={[
      version.displaced_people,
      version.displaced_households,
      version.displaced_people_from_community_land,
      version.displaced_people_within_community_land,
      version.displaced_households_from_fields,
      version.displaced_people_on_completion,
      version.displacement_of_people_comment,
    ]}
  >
    <TextField
      fieldname="displaced_people"
      label={$_("Displaced people")}
      value={version.displaced_people}
    />
    <TextField
      fieldname="displaced_households"
      label={$_("Displaced households")}
      value={version.displaced_households}
    />
    <TextField
      fieldname="displaced_people_from_community_land"
      label={$_("Displaced people from community land")}
      value={version.displaced_people_from_community_land}
    />
    <TextField
      fieldname="displaced_people_within_community_land"
      label={$_("Displaced people within community land")}
      value={version.displaced_people_within_community_land}
    />
    <TextField
      fieldname="displaced_households_from_fields"
      label={$_("Displaced households from fields")}
      value={version.displaced_households_from_fields}
    />
    <TextField
      fieldname="displaced_people_on_completion"
      label={$_("Displaced people on completion")}
      value={version.displaced_people_on_completion}
    />
    <TextField
      fieldname="displacement_of_people_comment"
      label={$_("Comment on displacement of people")}
      value={version.displacement_of_people_comment}
    />
  </Subsection>
  <Subsection
    title={$_("Negative impacts for local communities")}
    fields={[version.negative_impacts, version.negative_impacts_comment]}
  >
    <TextField
      fieldname="negative_impacts"
      label={$_("Negative impacts")}
      value={version.negative_impacts}
      choices={$fieldChoices.deal.negative_impacts}
      multipleChoices
    />
    <TextField
      fieldname="negative_impacts_comment"
      label={$_("Comment on negative impacts")}
      value={version.negative_impacts_comment}
    />
  </Subsection>
  <Subsection
    title={$_("Promised or received compensation")}
    fields={[version.promised_compensation, version.received_compensation]}
  >
    <TextField
      fieldname="promised_compensation"
      label={$_("Promised compensation")}
      value={version.promised_compensation}
    />
    <TextField
      fieldname="received_compensation"
      label={$_("Received compensation")}
      value={version.received_compensation}
    />
  </Subsection>
  <Subsection
    title={$_("Promised benefits for local communities")}
    fields={[version.promised_benefits, version.promised_benefits_comment]}
  >
    <TextField
      fieldname="promised_benefits"
      label={$_("Promised benefits")}
      value={version.promised_benefits}
      choices={$fieldChoices.deal.benefits}
      multipleChoices
    />
    <TextField
      fieldname="promised_benefits_comment"
      label={$_("Comment on promised benefits")}
      value={version.promised_benefits_comment}
    />
  </Subsection>
  <Subsection
    title={$_("Materialized benefits for local communities")}
    fields={[version.materialized_benefits, version.materialized_benefits_comment]}
  >
    <TextField
      fieldname="materialized_benefits"
      label={$_("Materialized benefits")}
      value={version.materialized_benefits}
      choices={$fieldChoices.deal.benefits}
      multipleChoices
    />
    <TextField
      fieldname="materialized_benefits_comment"
      label={$_("Comment on materialized benefits")}
      value={version.materialized_benefits_comment}
    />
  </Subsection>
  <Subsection
    title={$_(
      "Presence of organizations and actions taken (e.g. farmer organizations, NGOs, etc.)",
    )}
    fields={[version.presence_of_organizations]}
  >
    <TextField
      fieldname="presence_of_organizations"
      label={$_("Presence of organizations")}
      value={version.presence_of_organizations}
    />
  </Subsection>
</section>
