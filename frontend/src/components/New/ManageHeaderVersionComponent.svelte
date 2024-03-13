<script lang="ts">
  import { _ } from "svelte-i18n"

  import { navigating, page } from "$app/stores"

  import { loading } from "$lib/stores"
  import type { DealHull, InvestorHull } from "$lib/types/newtypes.js"
  import { Version2Status } from "$lib/types/newtypes.js"
  import { UserRole, type User } from "$lib/types/user"

  import Modal from "$components/Modal.svelte"
  import ManageHeaderActivateModal from "$components/New/ManageHeaderActivateModal.svelte"
  import ManageHeaderRequestImprovementModal from "$components/New/ManageHeaderRequestImprovementModal.svelte"
  import ManageHeaderSendToActivationModal from "$components/New/ManageHeaderSendToActivationModal.svelte"
  import ManageHeaderSendToReviewModal from "$components/New/ManageHeaderSendToReviewModal.svelte"
  import ManageHeaderVersionRemoveModal from "$components/New/ManageHeaderVersionRemoveModal.svelte"

  export let object: DealHull | InvestorHull

  let showRequestImprovementOverlay = false
  let showSendToReviewOverlay = false
  let showSendToActivationOverlay = false
  let showActivateOverlay = false

  let showDeleteOverlay = false

  const isDeal = (obj: DealHull | InvestorHull): obj is DealHull =>
    "fully_updated_at" in obj

  let showReallyEditModal = false
  $: editLink = `/${isDeal(object) ? "deal" : "investor"}/edit/${object.id}/${
    object.selected_version.id
  }/`

  $: isCurrentDraft = object.selected_version.id === object.draft_version_id
  $: i18nValues = { values: { object: isDeal(object) ? "deal" : "investor" } }

  function isAuthorized(user: User, obj: DealHull | InvestorHull): boolean {
    const { role } = user
    switch (obj.selected_version.status) {
      case null: // anybody who has a relevant role (Reporter, Editor, Admin)
        return role >= UserRole.REPORTER
      case Version2Status.DRAFT: // the Reporter of the Object or Editor,Administrator
        return role >= UserRole.EDITOR || user.id === obj.selected_version.created_by_id
      case Version2Status.REVIEW: // at least Editor
        return role >= UserRole.EDITOR
      case Version2Status.REJECTED: // only Admins
        return role === UserRole.ADMINISTRATOR
      case Version2Status.ACTIVATION: // only Admins
        return role === UserRole.ADMINISTRATOR
      default:
        return false
    }
  }
</script>

<div class="flex w-full flex-wrap justify-between text-center">
  <div class="status-field z-[3] bg-green-300 after:border-l-green-300">
    <span class="font-bold">{$_("Draft")}</span>
  </div>
  <div
    class="status-field z-[2] bg-green-400 after:border-l-green-400"
    class:inactive={object.selected_version.status === Version2Status.DRAFT}
  >
    <span class="font-bold">{$_("Submitted for review")}</span>
  </div>
  <div
    class="status-field z-[1] bg-green-500 after:border-l-green-500"
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
    {#if object.selected_version.status === Version2Status.DRAFT && isAuthorized($page.data.user, object)}
      <button
        type="button"
        class:disabled={!isCurrentDraft || $loading || $navigating}
        title={$_("Submit the {object} for review", i18nValues)}
        class="butn butn-primary"
        on:click={() => (showSendToReviewOverlay = true)}
      >
        {$_("Submit for review")}
      </button>
    {/if}
    {#if [Version2Status.REVIEW, Version2Status.ACTIVATION].includes(object.selected_version.status) && isAuthorized($page.data.user, object)}
      <button
        type="button"
        class:disabled={!isCurrentDraft || $loading || $navigating}
        title={$_(
          "Send a request of improvement and create a new draft version of the {object}.",
          i18nValues,
        )}
        class="btn btn-primary"
        on:click={() => (showRequestImprovementOverlay = true)}
      >
        {$_("Request improvement")}
      </button>
    {/if}
  </div>
  <div class="flex-1 text-center">
    {#if object.selected_version.status === Version2Status.REVIEW && isAuthorized($page.data.user, object)}
      <button
        type="button"
        class:disabled={!isCurrentDraft || $loading || $navigating}
        title={$_("Submit the {object} for activation", i18nValues)}
        class="butn butn-pelorous"
        on:click={() => (showSendToActivationOverlay = true)}
      >
        {$_("Submit for activation")}
      </button>
    {/if}
  </div>
  <div class="flex-1 text-left">
    {#if object.selected_version.status === Version2Status.ACTIVATION && isAuthorized($page.data.user, object)}
      <button
        type="button"
        class:disabled={!isCurrentDraft || $loading || $navigating}
        title={object.active_version_id
          ? $_("Activate submitted version replacing currently active version")
          : $_("Set the {object} active", i18nValues)}
        class="butn butn-pelorous"
        on:click={() => (showActivateOverlay = true)}
      >
        {$_("Activate")}
      </button>
    {/if}
  </div>
</div>
<div class="mt-10 flex flex-col gap-2">
  <div class=" flex items-center gap-4">
    {#if object.selected_version.created_by_id !== $page.data.user.id}
      <div>
        <button
          on:click={() => (showReallyEditModal = true)}
          class="butn-outline butn-flat butn-primary min-w-[8rem]"
          class:disabled={$loading || $navigating}
        >
          {$_("Edit")}
        </button>
      </div>
      <div class="italic text-gray-700 dark:text-white">
        {$_(
          "Edit this version. Since you are not the author of the current one, a new draft will be created.",
        )}
      </div>
    {:else}
      <div>
        <a
          href={editLink}
          class="butn-outline butn-flat butn-primary min-w-[8rem]"
          class:disabled={$loading || $navigating}
        >
          {$_("Edit")}
        </a>
      </div>
      <div class="italic text-gray-700 dark:text-white">
        {$_("Edit this version.")}
      </div>
    {/if}
  </div>

  {#if $page.data.user?.role >= UserRole.EDITOR}
    <div class="flex items-center gap-4">
      <div>
        <button
          class="butn-outline butn-flat butn-red min-w-[8rem]"
          class:disabled={$loading || $navigating}
          on:click|preventDefault={() => (showDeleteOverlay = true)}
        >
          {$_("Remove")}
        </button>
      </div>
      <div class="italic text-gray-700 dark:text-white">
        {$_(
          "Completely removes this version of the {object}. This action cannot be undone.",
          i18nValues,
        )}
      </div>
    </div>
  {/if}
</div>

<Modal bind:open={showReallyEditModal} dismissible>
  <h2 class="heading4">{$_("Create a new draft")}</h2>
  <hr />
  <form class="mt-6 text-lg">
    You are not the author of this version. Therefore, a new version will be created if
    you proceed.

    <div class="mt-14 flex justify-end gap-4">
      <button
        class="butn-outline"
        on:click={() => (showReallyEditModal = false)}
        type="button"
      >
        {$_("Cancel")}
      </button>
      <a class="butn butn-primary" href={editLink}>
        {$_("Create a new draft")}
      </a>
    </div>
  </form>
</Modal>

<ManageHeaderSendToReviewModal bind:object bind:open={showSendToReviewOverlay} />
<ManageHeaderSendToActivationModal
  bind:object
  bind:open={showSendToActivationOverlay}
/>
<ManageHeaderActivateModal bind:object bind:open={showActivateOverlay} />
<ManageHeaderRequestImprovementModal
  bind:object
  bind:open={showRequestImprovementOverlay}
/>
<ManageHeaderVersionRemoveModal bind:object bind:open={showDeleteOverlay} />

<style lang="postcss">
  .status-field {
    @apply relative flex h-16 w-1/4 items-center justify-center border-2 pl-5 text-gray-700;
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
    @apply bg-gray-100 after:border-l-gray-100;
  }
</style>
