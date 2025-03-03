<script lang="ts">
  import dayjs from "dayjs"
  import type { Snippet } from "svelte"
  import { _ } from "svelte-i18n"

  import { page } from "$app/state"

  import { Version2Status, type DealHull, type InvestorHull } from "$lib/types/data"
  import { isAdmin } from "$lib/utils/permissions"

  import DetailsSummary from "$components/DetailsSummary.svelte"
  import HeaderDatesWDownload from "$components/HeaderDatesWDownload.svelte"
  import Cog6ToothIcon from "$components/icons/Cog6ToothIcon.svelte"
  import ManageHeaderConfidentialModal from "$components/New/ManageHeaderConfidentialModal.svelte"
  import ManageHeaderCopyModal from "$components/New/ManageHeaderCopyModal.svelte"
  import ManageHeaderDeletionModal from "$components/New/ManageHeaderDeletionModal.svelte"
  import ManageHeaderLogbook from "$components/New/ManageHeaderLogbook.svelte"
  import ManageHeaderVersionComponent from "$components/New/ManageHeaderVersionComponent.svelte"

  interface Props {
    object: DealHull | InvestorHull
    heading?: Snippet
    visibility?: Snippet
  }

  let { object = $bindable(), heading, visibility }: Props = $props()

  const isDeal = (obj: DealHull | InvestorHull): obj is DealHull =>
    "fully_updated_at" in obj

  let objType = $derived(isDeal(object) ? "deal" : "investor")

  let showCopyOverlay = $state(false)
  let showDeletionOverlay = $state(false)
  let showConfidentialOverlay = $state(false)

  let oldVersion = $derived(
    ![object.active_version_id, object.draft_version_id].includes(
      object.selected_version.id,
    ),
  )
</script>

{#if object.selected_version.id === object.draft_version_id && object.active_version_id}
  <div
    class="rounded border border-purple-500 bg-purple-100 px-4 py-2 text-lg dark:text-gray-900"
  >
    {isDeal(object)
      ? $_("You're viewing the draft version of this deal.")
      : $_("You're viewing the draft version of this investor.")}
    <a class="btn btn-flat" href="/{objType}/{object.id}/">
      {$_("Go to active version")}
    </a>
  </div>
{/if}
{#if object.draft_version_id && object.selected_version.id !== object.draft_version_id}
  <div
    class="rounded border border-green-500 bg-green-100 px-4 py-2 text-lg dark:text-gray-900"
  >
    {isDeal(object)
      ? $_("There is a draft version of this deal")
      : $_("There is a draft version of this investor.")}
    <a class="btn btn-flat" href="/{objType}/{object.id}/{object.draft_version_id}/">
      {$_("Go to current draft")}
    </a>
  </div>
{/if}

<div class="my-4 grid grid-cols-2 lg:grid-cols-3">
  <div class="col-span-2 rounded-tl bg-gray-100 dark:bg-gray-600">
    <div class="flex flex-col items-center justify-between gap-4 p-2 md:flex-row">
      <div class="flex items-center gap-8">
        <h1 class="heading4 my-0 text-[1.875rem]">
          {#if object.selected_version.id !== object.active_version_id}
            <a href="/{objType}/{object.id}/" class:investor={!isDeal(object)}>
              {@render heading?.()}
            </a>
          {:else}
            {@render heading?.()}
          {/if}
        </h1>
        <div
          class={oldVersion
            ? "pointer-events-none cursor-not-allowed opacity-40"
            : undefined}
        >
          <DetailsSummary>
            {#snippet summary()}
              <div class="btn flex items-center gap-1">
                <Cog6ToothIcon />
                {$_("actions")}
              </div>
            {/snippet}

            {#snippet details()}
              <ul
                class="absolute z-50 mt-1 rounded border border-gray-400 bg-white px-4 py-2 shadow-2xl dark:bg-gray-700"
              >
                {#if object.selected_version.id === object.active_version_id && !object.draft_version_id}
                  <li class="my-3">
                    <div class="flex items-center gap-2">
                      <a
                        class="btn btn-primary min-w-[9rem]"
                        href="/{objType}/edit/{object.id}/"
                      >
                        {$_("Edit")}
                      </a>
                      {isDeal(object)
                        ? $_("Create a new draft version of this deal")
                        : $_("Create a new draft version of this investor")}
                    </div>
                  </li>
                {:else if object.selected_version.id !== object.draft_version_id}
                  <li class="my-3">
                    <div class="flex items-center gap-2">
                      <button
                        type="button"
                        class="btn btn-primary disabled min-w-[9rem]"
                      >
                        {$_("Edit")}
                      </button>
                      {$_("There is already a draft version, that you can find here:")}
                      <a href="/{objType}/{object.id}/{object.draft_version_id}/">
                        {$_("Version")} #{object.draft_version_id}
                      </a>
                    </div>
                  </li>
                {/if}

                {#if isDeal(object) && isAdmin(page.data.user)}
                  <li class="my-3">
                    <div class="flex items-center gap-2">
                      <button
                        type="button"
                        class="btn"
                        onclick={() => (showCopyOverlay = true)}
                      >
                        {$_("Copy deal")}
                      </button>
                      {$_("Copy this deal")}
                    </div>
                  </li>
                {/if}

                {#if isAdmin(page.data.user)}
                  <li class="my-3">
                    <div class="flex items-center gap-2">
                      <button
                        type="button"
                        class="btn btn-red min-w-[9rem]"
                        onclick={() => (showDeletionOverlay = true)}
                      >
                        {#if object.deleted}
                          {$_("Undelete")}
                        {:else}
                          {$_("Delete")}
                        {/if}
                      </button>
                      {#if object.deleted}
                        {isDeal(object)
                          ? $_("Reactivate this deal")
                          : $_("Reactivate this investor")}
                      {:else}
                        {isDeal(object)
                          ? $_("Delete this deal")
                          : $_("Delete this investor")}
                      {/if}
                    </div>
                  </li>
                {/if}

                {#if isDeal(object) && isAdmin(page.data.user)}
                  <li class="my-3">
                    <div class="flex items-center gap-2">
                      <button
                        type="button"
                        class="btn btn-red"
                        onclick={() => (showConfidentialOverlay = true)}
                      >
                        {object.confidential
                          ? $_("Unset confidential")
                          : $_("Set confidential")}
                      </button>
                    </div>
                  </li>
                {/if}
              </ul>
            {/snippet}
          </DetailsSummary>
        </div>
      </div>

      <HeaderDatesWDownload obj={object} />
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
          {@render visibility?.()}
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
  <ManageHeaderLogbook {object} />
</div>

<ManageHeaderDeletionModal {object} bind:open={showDeletionOverlay} />

{#if isDeal(object)}
  <ManageHeaderCopyModal {object} bind:open={showCopyOverlay} />
  <ManageHeaderConfidentialModal {object} bind:open={showConfidentialOverlay} />
{/if}
