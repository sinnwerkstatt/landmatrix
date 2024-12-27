<script lang="ts">
  import { _ } from "svelte-i18n"

  import { navigating, page } from "$app/state"

  import { loading } from "$lib/stores/basics"
  import {
    Version2Status,
    type DealHull,
    type InvestorHull,
    type LeanUser,
    type User,
  } from "$lib/types/data"
  import { isAdmin, isEditorOrAbove } from "$lib/utils/permissions"

  import Modal from "$components/Modal.svelte"
  import ManageHeaderActivateModal from "$components/New/ManageHeaderActivateModal.svelte"
  import ManageHeaderRequestImprovementModal from "$components/New/ManageHeaderRequestImprovementModal.svelte"
  import ManageHeaderSendToActivationModal from "$components/New/ManageHeaderSendToActivationModal.svelte"
  import ManageHeaderSendToReviewModal from "$components/New/ManageHeaderSendToReviewModal.svelte"
  import ManageHeaderVersionRemoveModal from "$components/New/ManageHeaderVersionRemoveModal.svelte"

  interface Props {
    object: DealHull | InvestorHull
  }

  let { object }: Props = $props()

  let showRequestImprovementOverlay = $state(false)
  let showSendToReviewOverlay = $state(false)
  let showSendToActivationOverlay = $state(false)
  let showActivateOverlay = $state(false)
  let showDeleteOverlay = $state(false)

  const isDeal = (obj: DealHull | InvestorHull): obj is DealHull =>
    "fully_updated_at" in obj

  let showReallyEditModal = $state(false)
  let editLink = $derived(
    `/${isDeal(object) ? "deal" : "investor"}/edit/${object.id}/${
      object.selected_version.id
    }/`,
  )

  let isCurrentDraft = $derived(object.selected_version.id === object.draft_version_id)
  let i18nValues = $derived({
    values: { object: isDeal(object) ? "deal" : "investor" },
  })

  // TODO: Refactor to object (deal/investor) utils!
  const isActiveVersionCreator = (
    user: User | LeanUser | null,
    obj: DealHull | InvestorHull,
  ) => !!user && user.id === obj.selected_version.created_by_id

  const isAuthorized = (user: User | null, obj: DealHull | InvestorHull): boolean => {
    switch (obj.selected_version.status) {
      case Version2Status.DRAFT:
        return isEditorOrAbove(user) || isActiveVersionCreator(user, obj)
      case Version2Status.REVIEW:
        return isEditorOrAbove(user)
      case Version2Status.ACTIVATION:
        return isAdmin(user)
      case Version2Status.ACTIVATED:
        return isAdmin(user)
      default:
        return false
    }
  }

  let userCanEditOrRemove = $derived(
    isAdmin(page.data.user)
      ? true
      : isEditorOrAbove(page.data.user)
        ? ["DRAFT", "REVIEW"].includes(object.selected_version.status)
        : isActiveVersionCreator(page.data.user, object) &&
          object.selected_version.status === "DRAFT",
  )
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
    {#if object.selected_version.status === Version2Status.DRAFT && isAuthorized(page.data.user, object)}
      <button
        type="button"
        class:disabled={!isCurrentDraft || $loading || navigating.to}
        title={$_("Submit the {object} for review", i18nValues)}
        class="btn btn-primary"
        onclick={() => (showSendToReviewOverlay = true)}
      >
        {$_("Submit for review")}
      </button>
    {/if}
    {#if ["REVIEW", "ACTIVATION"].includes(object.selected_version.status) && isAuthorized(page.data.user, object)}
      <button
        type="button"
        class:disabled={!isCurrentDraft || $loading || navigating.to}
        title={$_(
          "Send a request of improvement and create a new draft version of the {object}.",
          i18nValues,
        )}
        class="btn btn-primary"
        onclick={() => (showRequestImprovementOverlay = true)}
      >
        {$_("Request improvement")}
      </button>
    {/if}
  </div>
  <div class="flex-1 text-center">
    {#if object.selected_version.status === Version2Status.REVIEW && isAuthorized(page.data.user, object)}
      <button
        type="button"
        class:disabled={!isCurrentDraft || $loading || navigating.to}
        title={$_("Submit the {object} for activation", i18nValues)}
        class="btn btn-pelorous"
        onclick={() => (showSendToActivationOverlay = true)}
      >
        {$_("Submit for activation")}
      </button>
    {/if}
  </div>
  <div class="flex-1 text-left">
    {#if object.selected_version.status === Version2Status.ACTIVATION && isAuthorized(page.data.user, object)}
      <button
        type="button"
        class:disabled={!isCurrentDraft || $loading || navigating.to}
        title={object.active_version_id
          ? $_("Activate submitted version replacing currently active version")
          : $_("Set the {object} active", i18nValues)}
        class="btn btn-pelorous"
        onclick={() => (showActivateOverlay = true)}
      >
        {$_("Activate")}
      </button>
    {/if}
  </div>
</div>
<div class="mt-10 flex flex-col gap-2">
  {#if userCanEditOrRemove}
    <div class=" flex items-center gap-4">
      {#if isActiveVersionCreator(page.data.user, object) && object.selected_version.status === "DRAFT"}
        <div>
          <a
            href={editLink}
            class="btn-outline btn-flat btn-primary min-w-[8rem]"
            class:disabled={!isCurrentDraft || $loading || navigating.to}
          >
            {$_("Edit")}
          </a>
        </div>
        <div class="italic text-gray-700 dark:text-white">
          {$_("Edit this version.")}
        </div>
      {:else}
        <div>
          <button
            onclick={() => (showReallyEditModal = true)}
            class="btn-outline btn-flat btn-primary min-w-[8rem]"
            class:disabled={!isCurrentDraft || $loading || navigating.to}
          >
            {$_("Edit")}
          </button>
        </div>
        <div class="italic text-gray-700 dark:text-white">
          {#if object.selected_version.status === "DRAFT"}
            {$_(
              "Edit this version. Since you are not the author of the current one, a new draft will be created.",
            )}
          {:else}
            {$_(
              "Edit this version. Since this version is not in Draft status anymore, a new draft will be created.",
            )}
          {/if}
        </div>
      {/if}
    </div>
  {/if}

  {#if userCanEditOrRemove}
    <div class="flex items-center gap-4">
      <div>
        <button
          class="btn-outline btn-flat btn-red min-w-[8rem]"
          class:disabled={$loading || navigating.to}
          type="button"
          onclick={() => (showDeleteOverlay = true)}
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
    {#if object.selected_version.status === "DRAFT"}
      {$_(
        "You are not the author of this version. Therefore, a new version will be created if you proceed.",
      )}
    {:else}
      {$_(
        "This version is not in Draft status anymore. Therefore, a new version will be created if you proceed.",
      )}
    {/if}
    <div class="mt-14 flex justify-end gap-4">
      <button
        class="btn-outline"
        onclick={() => (showReallyEditModal = false)}
        type="button"
      >
        {$_("Cancel")}
      </button>
      <a class="btn btn-primary" href={editLink}>
        {$_("Create a new draft")}
      </a>
    </div>
  </form>
</Modal>

<ManageHeaderSendToReviewModal {object} bind:open={showSendToReviewOverlay} />
<ManageHeaderSendToActivationModal {object} bind:open={showSendToActivationOverlay} />
<ManageHeaderActivateModal {object} bind:open={showActivateOverlay} />
<ManageHeaderRequestImprovementModal
  {object}
  bind:open={showRequestImprovementOverlay}
/>
<ManageHeaderVersionRemoveModal {object} bind:open={showDeleteOverlay} />

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
    @apply bg-gray-100;
  }
  .status-field.inactive:after {
    @apply border-l-gray-100;
  }
</style>
