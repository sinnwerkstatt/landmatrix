<script lang="ts">
  import { slide } from "svelte/transition"

  import type { DealHull } from "$lib/types/data"

  import EditSubsection from "$components/Data/EditSubsection.svelte"
  import EditField from "$components/Fields/EditField.svelte"

  interface Props {
    deal: DealHull
  }

  let { deal = $bindable() }: Props = $props()
</script>

<form id="local_communities" class="pb-52">
  <EditSubsection id="name_of_community">
    <EditField
      fieldname="name_of_community"
      showLabel
      bind:value={deal.selected_version.name_of_community}
    />
    <EditField
      fieldname="name_of_indigenous_people"
      showLabel
      bind:value={deal.selected_version.name_of_indigenous_people}
    />
    <EditField
      fieldname="people_affected_comment"
      showLabel
      bind:value={deal.selected_version.people_affected_comment}
    />
  </EditSubsection>

  <EditSubsection id="recognition_status">
    <EditField
      fieldname="recognition_status"
      showLabel
      bind:value={deal.selected_version.recognition_status}
    />
    <EditField
      fieldname="recognition_status_comment"
      showLabel
      bind:value={deal.selected_version.recognition_status_comment}
    />
  </EditSubsection>

  <EditSubsection id="community_consultation">
    <EditField
      fieldname="community_consultation"
      showLabel
      bind:value={deal.selected_version.community_consultation}
    />
    <EditField
      fieldname="community_consultation_comment"
      showLabel
      bind:value={deal.selected_version.community_consultation_comment}
    />
  </EditSubsection>

  <EditSubsection id="community_reaction">
    <EditField
      fieldname="community_reaction"
      showLabel
      bind:value={deal.selected_version.community_reaction}
    />
    <EditField
      fieldname="community_reaction_comment"
      showLabel
      bind:value={deal.selected_version.community_reaction_comment}
    />
  </EditSubsection>

  <EditSubsection id="land_conflicts">
    <EditField
      fieldname="land_conflicts"
      showLabel
      bind:value={deal.selected_version.land_conflicts}
    />
    <EditField
      fieldname="land_conflicts_comment"
      showLabel
      bind:value={deal.selected_version.land_conflicts_comment}
    />
  </EditSubsection>

  <EditSubsection id="displacement_of_people">
    <EditField
      fieldname="displacement_of_people"
      showLabel
      bind:value={deal.selected_version.displacement_of_people}
    />
    {#if deal.selected_version.displacement_of_people === true}
      <div class="pl-4" transition:slide={{ duration: 300 }}>
        <EditField
          fieldname="displaced_people"
          showLabel
          bind:value={deal.selected_version.displaced_people}
        />
        <EditField
          fieldname="displaced_households"
          showLabel
          bind:value={deal.selected_version.displaced_households}
        />
        <EditField
          fieldname="displaced_people_from_community_land"
          showLabel
          bind:value={deal.selected_version.displaced_people_from_community_land}
        />
        <EditField
          fieldname="displaced_people_within_community_land"
          showLabel
          bind:value={deal.selected_version.displaced_people_within_community_land}
        />
        <EditField
          fieldname="displaced_households_from_fields"
          showLabel
          bind:value={deal.selected_version.displaced_households_from_fields}
        />
        <EditField
          fieldname="displaced_people_on_completion"
          showLabel
          bind:value={deal.selected_version.displaced_people_on_completion}
        />
      </div>
    {/if}
    <EditField
      fieldname="displacement_of_people_comment"
      showLabel
      bind:value={deal.selected_version.displacement_of_people_comment}
    />
  </EditSubsection>

  <EditSubsection id="negative_impacts">
    <EditField
      fieldname="negative_impacts"
      showLabel
      bind:value={deal.selected_version.negative_impacts}
    />
    <EditField
      fieldname="negative_impacts_comment"
      showLabel
      bind:value={deal.selected_version.negative_impacts_comment}
    />
  </EditSubsection>

  <EditSubsection id="promised_compensation">
    <EditField
      fieldname="promised_compensation"
      showLabel
      bind:value={deal.selected_version.promised_compensation}
    />
    <EditField
      fieldname="received_compensation"
      showLabel
      bind:value={deal.selected_version.received_compensation}
    />
  </EditSubsection>

  <EditSubsection id="promised_benefits">
    <EditField
      fieldname="promised_benefits"
      showLabel
      bind:value={deal.selected_version.promised_benefits}
    />
    <EditField
      fieldname="promised_benefits_comment"
      showLabel
      bind:value={deal.selected_version.promised_benefits_comment}
    />
  </EditSubsection>

  <EditSubsection id="materialized_benefits">
    <EditField
      fieldname="materialized_benefits"
      showLabel
      bind:value={deal.selected_version.materialized_benefits}
    />
    <EditField
      fieldname="materialized_benefits_comment"
      showLabel
      bind:value={deal.selected_version.materialized_benefits_comment}
    />
  </EditSubsection>

  <EditSubsection id="presence_of_organizations">
    <EditField
      fieldname="presence_of_organizations"
      showLabel
      bind:value={deal.selected_version.presence_of_organizations}
    />
  </EditSubsection>
</form>
