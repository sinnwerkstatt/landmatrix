<script lang="ts">
  import { createEventDispatcher } from "svelte"
  import { _ } from "svelte-i18n"

  import { navigating, page } from "$app/stores"

  import { newIsAuthorized } from "$lib/helpers"
  import { loading } from "$lib/stores"
  import type { DealHull, InvestorHull } from "$lib/types/newtypes.js"
  import { Version2Status } from "$lib/types/newtypes.js"

  import ManageHeaderDeleteModal from "$components/New/ManageHeaderDeleteModal.svelte"

  const dispatch = createEventDispatcher()

  export let object: DealHull | InvestorHull

  let showToDraftOverlay = false
  let showSendToActivationOverlay = false
  let showActivateOverlay = false
  let showNewDraftOverlay = false
  let showDeleteOverlay = false

  let hasActiveVersion = false // TODO
  const isDeal = (obj: DealHull | InvestorHull): obj is DealHull =>
    "fully_updated_at" in obj

  $: isCurrentDraft = object.selected_version.id === object.draft_version
  $: i18nValues = { values: { object: isDeal(object) ? "deal" : "investor" } }
</script>

{JSON.stringify(object.selected_version.status)}

<div class="flex w-full flex-wrap justify-between text-center">
  <div
    class="status-field z-[3] bg-green-200 after:border-l-green-200"
    class:active={object.selected_version.status === Version2Status.DRAFT}
  >
    <span class="font-bold">{$_("Draft")}</span>
  </div>
  <div
    class="status-field z-[2] bg-green-300 after:border-l-green-300"
    class:inactive={object.selected_version.status !== Version2Status.REVIEW}
  >
    <span class="font-bold">{$_("Submitted for review")}</span>
  </div>
  <div
    class="status-field z-[1] bg-green-400 after:border-l-green-400"
    class:inactive={object.selected_version.status !== Version2Status.ACTIVATION}
  >
    <span class="font-bold">{$_("Submitted for activation")}</span>
  </div>
  <div class="status-field inactive">
    <span class="font-bold">{$_("Activated")}</span>
  </div>
</div>
<div class="workflow-buttons my-2 flex">
  <div class="flex-1 text-right">
    {#if object.selected_version.status === Version2Status.DRAFT && newIsAuthorized($page.data.user, object)}
      <button
        type="button"
        class:disabled={!isCurrentDraft || $loading || $navigating}
        title={$_("Submit the {object} for review", i18nValues)}
        class="butn butn-primary"
        on:click={() => dispatch("sendToReview")}
      >
        {$_("Submit for review")}
      </button>
    {/if}
    {#if [Version2Status.REVIEW, Version2Status.ACTIVATION].includes(object.selected_version.status) && newIsAuthorized($page.data.user, object)}
      <button
        type="button"
        class:disabled={!isCurrentDraft || $loading || $navigating}
        title={$_(
          "Send a request of improvement and create a new draft version of the {object}.",
          i18nValues,
        )}
        class="btn btn-primary"
        on:click={() => (showToDraftOverlay = true)}
      >
        {$_("Request improvement")}
      </button>
    {/if}
  </div>
  <div class="flex-1 text-center">
    {#if object.selected_version.status === Version2Status.REVIEW && newIsAuthorized($page.data.user, object)}
      <button
        type="button"
        class:disabled={!isCurrentDraft || $loading || $navigating}
        title={$_("Submit the {object} for activation", i18nValues)}
        class="btn btn-pelorous"
        on:click={() => (showSendToActivationOverlay = true)}
      >
        {$_("Submit for activation")}
      </button>
    {/if}
  </div>
  <div class="flex-1 text-left">
    {#if object.selected_version.status === Version2Status.ACTIVATION && newIsAuthorized($page.data.user, object)}
      <button
        type="button"
        class:disabled={!isCurrentDraft || $loading || $navigating}
        title={hasActiveVersion
          ? $_("Activate submitted version replacing currently active version")
          : $_("Set the {object} active", i18nValues)}
        class="btn btn-pelorous"
        on:click={() => (showActivateOverlay = true)}
      >
        {$_("Activate")}
      </button>
    {/if}
  </div>
</div>
<div class="mt-10 flex items-center gap-4">
  <div>
    <button
      class="butn-outline butn-flat butn-red min-w-[8rem]"
      class:disabled={$loading || $navigating}
      on:click|preventDefault={() => (showDeleteOverlay = true)}
    >
      {$_("Remove")}
    </button>
  </div>
  <div class="italic text-lm-dark dark:text-white">
    {$_(
      "Completely removes this version of the {object}. This action cannot be undone.",
      i18nValues,
    )}
  </div>
</div>

<ManageHeaderDeleteModal bind:object bind:showDeleteOverlay />

<style lang="postcss">
  .status-field {
    @apply relative flex h-16 w-1/4 items-center justify-center border-2 pl-5 text-lm-dark;
  }

  .status-field:before {
    @apply content-[""];
    @apply border-y-[31px] border-y-transparent;
    @apply border-l-[18px] border-l-neutral-200;
    @apply absolute inset-y-0 left-0;
  }

  .status-field:after {
    @apply content-[""];
    @apply border-y-[31px] border-y-transparent;
    @apply border-l-[18px];
    @apply absolute inset-y-0 right-[-17px];
  }

  .status-field:first-child:before {
    @apply hidden;
  }

  .status-field:last-child:after {
    @apply hidden;
  }

  .status-field.inactive {
    @apply bg-lm-darkgray after:border-l-lm-darkgray;
  }
</style>
