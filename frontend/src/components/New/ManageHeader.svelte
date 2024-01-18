<script lang="ts">
  import dayjs from "dayjs"
  import { _ } from "svelte-i18n"

  import { page } from "$app/stores"

  import type { DealHull, InvestorHull } from "$lib/types/newtypes.js"
  import { Version2Status } from "$lib/types/newtypes.js"
  import { UserRole } from "$lib/types/user"

  import DetailsSummary from "$components/DetailsSummary.svelte"
  import HeaderDates from "$components/HeaderDates.svelte"
  import Cog6ToothIcon from "$components/icons/Cog6ToothIcon.svelte"
  import ManageHeaderConfidentialModal from "$components/New/ManageHeaderConfidentialModal.svelte"
  import ManageHeaderCopyModal from "$components/New/ManageHeaderCopyModal.svelte"
  import ManageHeaderDeletionModal from "$components/New/ManageHeaderDeletionModal.svelte"
  import ManageHeaderLogbook from "$components/New/ManageHeaderLogbook.svelte"
  import ManageHeaderVersionComponent from "$components/New/ManageHeaderVersionComponent.svelte"

  export let object: DealHull | InvestorHull

  const isDeal = (obj: DealHull | InvestorHull): obj is DealHull =>
    "fully_updated_at" in obj

  $: objType = isDeal(object) ? "deal" : "investor"

  let showCopyOverlay = false
  let showDeletionOverlay = false
  let showConfidentialOverlay = false
</script>

<div class="my-4 grid grid-cols-2 lg:grid-cols-3">
  <div class="col-span-2 rounded-tl bg-gray-100 dark:bg-gray-600">
    <div class="flex items-center justify-between gap-4 p-2">
      <div>
        <h1 class="heading4 my-0 text-[1.875rem]">
          <slot name="heading" />
        </h1>
      </div>

      <DetailsSummary>
        <div class="butn flex items-center gap-1" slot="summary">
          <Cog6ToothIcon />
          actions
        </div>
        <ul
          class="absolute z-50 border border-black bg-white p-2 shadow-2xl dark:bg-gray-700"
          slot="details"
        >
          <li class="my-2">
            <div class="flex items-center gap-2">
              <a class="butn" href="/{objType}/edit/{object.id}/">edit {objType}</a>
              this will edit the current deal and create blablabla...
            </div>
          </li>
          {#if isDeal(object) && $page.data.user?.role === UserRole.ADMINISTRATOR}
            <li class="my-2">
              <div class="flex items-center gap-2">
                <button
                  type="button"
                  class="butn"
                  on:click={() => (showCopyOverlay = true)}
                >
                  {$_("Copy deal")}
                </button>
                {$_("Copy this deal")}
              </div>
            </li>
          {/if}
          <li class="my-2">
            <div class="flex items-center gap-2">
              <button
                type="button"
                class="butn butn-red"
                on:click={() => (showDeletionOverlay = true)}
              >
                {#if object.deleted}
                  undelete
                {:else}
                  delete
                {/if}
              </button>
              {#if object.deleted}
                {isDeal(object)
                  ? $_("Reactivate this deal")
                  : $_("Reactivate this investor")}
              {:else}
                {isDeal(object) ? $_("Delete this deal") : $_("Delete this investor")}
              {/if}
            </div>
          </li>
          {#if isDeal(object) && $page.data.user?.role === UserRole.ADMINISTRATOR}
            <li class="my-2">
              <div class="flex items-center gap-2">
                <button
                  type="button"
                  class="butn butn-red"
                  on:click={() => (showConfidentialOverlay = true)}
                >
                  {#if object.confidential}
                    unset confidential
                  {:else}
                    set confidential
                  {/if}
                </button>
                {#if object.confidential}
                  this will unsset confidential
                {:else}
                  this will set confidential
                {/if}
              </div>
            </li>
          {/if}
        </ul>
      </DetailsSummary>
      <DetailsSummary>
        <div class="butn butn-primary flex items-center gap-1" slot="summary">
          <Cog6ToothIcon />
          versions
        </div>
        <ul
          class="absolute z-50 border border-black bg-white p-2 shadow-2xl dark:bg-gray-700"
          slot="details"
        >
          {#if object.active_version_id}
            <li class="my-2">
              <div class="flex items-center gap-2">
                <a
                  class="butn"
                  href="/{objType}/{object.id}/{object.active_version_id}/"
                >
                  active version
                </a>
                go to current active version
              </div>
            </li>
          {/if}
          {#if object.draft_version_id}
            <li class="my-2">
              <div class="flex items-center gap-2">
                <a
                  class="butn"
                  href="/{objType}/{object.id}/{object.draft_version_id}/"
                >
                  draft version
                </a>
                go to current draft version
              </div>
            </li>
          {/if}
        </ul>
      </DetailsSummary>
      <HeaderDates obj={object} />
      <!--      <div class="bg-white px-4 py-2">Draft version</div>-->
    </div>
    <hr class="h-0.5 bg-black" />
    <div class="p-2 py-4">
      {#if object.deleted}
        <div
          class="my-6 flex flex-col items-center justify-center gap-1 bg-red-500 py-2 text-white"
        >
          <div class="heading4 mb-0">{$_("Deleted")}</div>
          <span>{object.deleted_comment}</span>
        </div>
      {:else if isDeal(object) && object.confidential}
        <div
          class="my-6 flex flex-col items-center justify-center gap-1 bg-red-700 py-2 text-white"
        >
          <div class="heading4 mb-0">{$_("Confidential")}</div>
          <span>{object.confidential_comment}</span>
        </div>
      {:else}
        <div class="mb-4 flex items-center justify-between gap-4">
          <h2 class="heading4 mb-0">Version #{object.selected_version.id}</h2>
          <slot name="visibility" />
        </div>
        {#if object.selected_version.status === Version2Status.ACTIVATED}
          <div
            class="my-6 flex flex-col items-center justify-center gap-1 bg-green-700 py-2 text-white"
          >
            <div class="heading4 mb-0">{$_("Activated")}</div>
            <div class="">
              {#if object.selected_version.activated_at}
                {dayjs(object.selected_version.activated_at).format("YYYY-MM-DD")}
              {/if}
            </div>
          </div>
        {:else}
          <ManageHeaderVersionComponent {object} />
        {/if}
      {/if}
    </div>
  </div>
  <ManageHeaderLogbook {object} extraUserIDs={[]} />
</div>

<ManageHeaderDeletionModal bind:object bind:open={showDeletionOverlay} />

{#if isDeal(object)}
  <ManageHeaderCopyModal bind:object bind:open={showCopyOverlay} />
  <ManageHeaderConfidentialModal bind:object bind:open={showConfidentialOverlay} />
{/if}
