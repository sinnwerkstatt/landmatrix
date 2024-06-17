<script lang="ts">
  import type { DealHull, DealVersion2 } from "$lib/types/data"

  import Subsection from "$components/Data/Subsection.svelte"
  import DisplayField from "$components/Fields/DisplayField.svelte"

  export let deal: DealHull

  let version: DealVersion2 = deal.selected_version
  $: version = deal.selected_version
</script>

<section>
  <Subsection id="name_of_community" obj={version}>
    <DisplayField
      fieldname="name_of_community"
      showLabel
      value={version.name_of_community}
    />
    <DisplayField
      fieldname="name_of_indigenous_people"
      showLabel
      value={version.name_of_indigenous_people}
    />
    <DisplayField
      fieldname="people_affected_comment"
      showLabel
      value={version.people_affected_comment}
    />
  </Subsection>

  <Subsection id="recognition_status" obj={version}>
    <DisplayField
      fieldname="recognition_status"
      showLabel
      value={version.recognition_status}
    />
    <DisplayField
      fieldname="recognition_status_comment"
      showLabel
      value={version.recognition_status_comment}
    />
  </Subsection>

  <Subsection id="community_consultation" obj={version}>
    <DisplayField
      fieldname="community_consultation"
      showLabel
      value={version.community_consultation}
    />
    <DisplayField
      fieldname="community_consultation_comment"
      showLabel
      value={version.community_consultation_comment}
    />
  </Subsection>

  <Subsection id="community_reaction" obj={version}>
    <DisplayField
      fieldname="community_reaction"
      showLabel
      value={version.community_reaction}
    />
    <DisplayField
      fieldname="community_reaction_comment"
      showLabel
      value={version.community_reaction_comment}
    />
  </Subsection>

  <Subsection id="land_conflicts" obj={version}>
    <DisplayField fieldname="land_conflicts" showLabel value={version.land_conflicts} />
    <DisplayField
      fieldname="land_conflicts_comment"
      showLabel
      value={version.land_conflicts_comment}
    />
  </Subsection>

  <Subsection id="displacement_of_people" obj={version}>
    <DisplayField
      fieldname="displacement_of_people"
      showLabel
      value={version.displacement_of_people}
    />
    <DisplayField
      fieldname="displaced_people"
      showLabel
      value={version.displaced_people}
    />
    <DisplayField
      fieldname="displaced_households"
      showLabel
      value={version.displaced_households}
    />
    <DisplayField
      fieldname="displaced_people_from_community_land"
      showLabel
      value={version.displaced_people_from_community_land}
    />
    <DisplayField
      fieldname="displaced_people_within_community_land"
      showLabel
      value={version.displaced_people_within_community_land}
    />
    <DisplayField
      fieldname="displaced_households_from_fields"
      showLabel
      value={version.displaced_households_from_fields}
    />
    <DisplayField
      fieldname="displaced_people_on_completion"
      showLabel
      value={version.displaced_people_on_completion}
    />
    <DisplayField
      fieldname="displacement_of_people_comment"
      showLabel
      value={version.displacement_of_people_comment}
    />
  </Subsection>

  <Subsection id="negative_impacts" obj={version}>
    <DisplayField
      fieldname="negative_impacts"
      showLabel
      value={version.negative_impacts}
    />
    <DisplayField
      fieldname="negative_impacts_comment"
      showLabel
      value={version.negative_impacts_comment}
    />
  </Subsection>

  <Subsection id="promised_compensation" obj={version}>
    <DisplayField
      fieldname="promised_compensation"
      showLabel
      value={version.promised_compensation}
    />
    <DisplayField
      fieldname="received_compensation"
      showLabel
      value={version.received_compensation}
    />
  </Subsection>

  <Subsection id="promised_benefits" obj={version}>
    <DisplayField
      fieldname="promised_benefits"
      showLabel
      value={version.promised_benefits}
    />
    <DisplayField
      fieldname="promised_benefits_comment"
      showLabel
      value={version.promised_benefits_comment}
    />
  </Subsection>

  <Subsection id="materialized_benefits" obj={version}>
    <DisplayField
      fieldname="materialized_benefits"
      showLabel
      value={version.materialized_benefits}
    />
    <DisplayField
      fieldname="materialized_benefits_comment"
      showLabel
      value={version.materialized_benefits_comment}
    />
  </Subsection>

  <Subsection id="presence_of_organizations" obj={version}>
    <DisplayField
      fieldname="presence_of_organizations"
      showLabel
      value={version.presence_of_organizations}
    />
  </Subsection>
</section>
