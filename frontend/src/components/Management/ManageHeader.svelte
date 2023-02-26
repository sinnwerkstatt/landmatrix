<script lang="ts">
  import cn from "classnames"
  import dayjs from "dayjs"
  import { createEventDispatcher } from "svelte"
  import { _ } from "svelte-i18n"

  import { goto } from "$app/navigation"
  import { page } from "$app/stores"

  import {
    isAuthorized,
    findActiveVersion,
    isAdmin,
    isCreator,
    isEditorPlus,
  } from "$lib/helpers"
  import type { Obj, ObjVersion } from "$lib/types/generics"
  import { DraftStatus, Status } from "$lib/types/generics"

  import DateTimeField from "$components/Fields/Display/DateTimeField.svelte"
  import ManageOverlay from "$components/Management/ManageOverlay.svelte"

  import ManageHeaderLogbook from "./ManageHeaderLogbook.svelte"

  const dispatch = createEventDispatcher()

  export let object: Obj
  export let objectVersion: number | undefined
  export let otype: "deal" | "investor" = "deal"

  let showToDraftOverlay = false
  let showDeleteOverlay = false
  let showSendToActivationOverlay = false
  let showActivateOverlay = false
  let showNewDraftOverlay = false

  let lastVersion: ObjVersion
  $: lastVersion = object.versions[0]

  let extraUserIDs: number[]
  $: extraUserIDs = [
    ...new Set(object.versions.filter(v => v.created_by).map(v => v.created_by.id)),
  ]

  let activeVersion: ObjVersion | undefined
  $: activeVersion = findActiveVersion(object, otype)

  // object status
  let isActive: boolean
  $: isActive = object.status === Status.LIVE || object.status === Status.UPDATED

  let isDeleted: boolean
  $: isDeleted = object.status === Status.DELETED

  // object draft status
  let isCurrentDraft: boolean
  $: isCurrentDraft = objectVersion ? lastVersion.id === objectVersion : false

  let hasCurrentDraft: boolean
  $: hasCurrentDraft = (lastVersion[otype] as Obj).draft_status !== null

  let isActiveVersion: boolean
  $: isActiveVersion = !objectVersion

  let hasActiveVersion: boolean
  $: hasActiveVersion = !!activeVersion

  let canGoToDraftVersion: boolean
  $: canGoToDraftVersion =
    isCreator($page.data.user, lastVersion) || isEditorPlus($page.data.user)

  let isEditable: boolean
  $: isEditable = hasCurrentDraft ? isCurrentDraft : isActiveVersion && !isDeleted

  function doDelete({ detail: { comment } }): void {
    dispatch("delete", { comment })
    showDeleteOverlay = false
  }
  function sendToDraft({ detail: { comment, toUser } }): void {
    dispatch("changeStatus", { transition: "TO_DRAFT", comment, toUser })
    showToDraftOverlay = false
  }
  function sendToActivation({ detail: { comment } }) {
    dispatch("changeStatus", { transition: "TO_ACTIVATION", comment })
    showSendToActivationOverlay = false
  }
  function activate({ detail: { comment } }) {
    dispatch("changeStatus", { transition: "ACTIVATE", comment })
    showActivateOverlay = false
  }
</script>

<div class="my-6">
  <div class="flex flex-col p-0 lg:flex-row">
    <div class="grow-[2] bg-neutral-200">
      <div class="-mt-5 flex justify-center gap-4">
        {#if hasActiveVersion && !isActiveVersion}
          <a href="/{otype}/{object.id}" class="btn btn-gray">
            {$_("Go to active version")}
          </a>
        {/if}
        {#if hasCurrentDraft && !isCurrentDraft && canGoToDraftVersion}
          <a href="/{otype}/{object.id}/{lastVersion.id}/" class="btn btn-gray">
            {$_("Go to current draft")}
          </a>
        {/if}
      </div>

      <div
        class="title-and-date-bar mt-4 flex w-full flex-row justify-between gap-4 p-4"
      >
        <div>
          <h1 class="mb-0 text-3xl text-black">
            <slot name="heading" />
          </h1>
        </div>
        <div class="my-2 flex w-auto items-center rounded bg-gray-50 p-3">
          <div class="mr-10 text-xs text-lm-dark md:mx-5 md:text-sm">
            {$_("Created")}
            <br />
            <DateTimeField value={object.created_at} />
          </div>
          <div class="mr-10 text-xs text-lm-dark md:mx-5 md:text-sm">
            {$_("Last update")}
            <br />
            <DateTimeField value={object.modified_at} />
          </div>
          {#if object.fully_updated_at}
            <div class="mr-10 text-xs text-lm-dark md:mx-5 md:text-sm">
              {$_("Last full update")}
              <br />
              <DateTimeField value={object.fully_updated_at} />
            </div>
          {/if}
        </div>
      </div>

      {#if isActiveVersion}
        <div
          class={cn(
            "flex h-16 w-full items-center justify-center border-2",
            "text-lg font-medium text-white",
            isActive ? "bg-pelorous-300" : "bg-[hsl(0,33%,68%)]",
          )}
        >
          {isActive ? $_("Activated") : $_("Deleted")}
        </div>
      {:else}
        <div>
          <div class="flex w-full flex-wrap justify-between text-center">
            <div
              class:active={object.draft_status === DraftStatus.DRAFT ||
                object.draft_status === DraftStatus.REJECTED}
              class="status-field z-[3]"
            >
              <span>{$_("Draft")}</span>
              {#if object.draft_status === DraftStatus.REJECTED}
                <span class="pl-2 font-bold text-red-600">
                  ({$_("Rejected")})
                </span>
              {/if}
            </div>
            <div
              class:active={object.draft_status === DraftStatus.REVIEW}
              class="status-field z-[2]"
            >
              <span>{$_("Submitted for review")}</span>
            </div>
            <div
              class:active={object.draft_status === DraftStatus.ACTIVATION}
              class="status-field z-[1]"
            >
              <span>{$_("Submitted for activation")}</span>
            </div>
            <div class:active={object.draft_status === null} class="status-field">
              <span>{$_("Activated")}</span>
            </div>
          </div>
          <div class="workflow-buttons flex">
            <div class="flex-1 text-right">
              {#if object.draft_status === DraftStatus.DRAFT && isAuthorized($page.data.user, object)}
                <button
                  type="button"
                  class:disabled={!isCurrentDraft}
                  title={otype === "deal"
                    ? $_("Submit the deal for review")
                    : $_("Submit the investor for review")}
                  class="btn btn-pelorous"
                  on:click={() => dispatch("sendToReview")}
                >
                  {$_("Submit for review")}
                </button>
              {/if}
              {#if (object.draft_status === DraftStatus.REVIEW || object.draft_status === DraftStatus.ACTIVATION) && isAuthorized($page.data.user, object)}
                <button
                  type="button"
                  class:disabled={!isCurrentDraft}
                  title={otype === "deal"
                    ? $_(
                        "Send a request of improvement and create a new draft version of the deal",
                      )
                    : $_(
                        "Send a request of improvement and create a new draft version of the investor",
                      )}
                  class="btn btn-primary"
                  on:click={() => (showToDraftOverlay = true)}
                >
                  {$_("Request improvement")}
                </button>
              {/if}
            </div>
            <div class="flex-1 text-center">
              {#if object.draft_status === DraftStatus.REVIEW && isAuthorized($page.data.user, object)}
                <button
                  type="button"
                  class:disabled={!isCurrentDraft}
                  title={otype === "deal"
                    ? $_("Submit the deal for activation")
                    : $_("Submit the investor for activation")}
                  class="btn btn-pelorous"
                  on:click={() => (showSendToActivationOverlay = true)}
                >
                  {$_("Submit for activation")}
                </button>
              {/if}
            </div>
            <div class="flex-1 text-left">
              {#if object.draft_status === DraftStatus.ACTIVATION && isAuthorized($page.data.user, object)}
                <button
                  type="button"
                  class:disabled={!isCurrentDraft}
                  title={hasActiveVersion
                    ? $_(
                        "Activate submitted version replacing currently active version",
                      )
                    : otype === "deal"
                    ? $_("Set the deal active")
                    : $_("Set the investor active")}
                  class="btn btn-pelorous"
                  on:click={() => (showActivateOverlay = true)}
                >
                  {$_("Activate")}
                </button>
              {/if}
            </div>
          </div>
        </div>
      {/if}
      <div class="flew-row flex w-full gap-4 p-4">
        <div class="flex-auto">
          {#if lastVersion}
            <div class="mb-4 text-sm">
              {$_("Last changes")}
              {#if lastVersion.created_by}
                <span>
                  {$_("by")}
                  {lastVersion.created_by.full_name}
                </span>
              {/if}
              on
              {dayjs(lastVersion.modified_at ?? lastVersion.created_at).format(
                "YYYY-MM-DD HH:mm",
              )}
              <br />
              {#if object.versions.length > 1}
                <a
                  href="/{otype}/{object.id}/compare/{object.versions[1].id}/{object
                    .versions[0].id}/"
                >
                  {$_("Show latest changes")}
                </a>
              {/if}
            </div>
          {/if}
          <div class="space-y-0.5">
            {#if isEditable}
              <div class="flex items-center gap-4">
                {#if isCreator($page.data.user, object)}
                  <div>
                    <a
                      href="/{otype}/edit/{object.id}/{objectVersion ?? ''}"
                      class="btn btn-primary min-w-[8rem]"
                    >
                      {$_("Edit")}
                    </a>
                  </div>
                  <div class="italic text-black/50">
                    {$_("Edit this version")}
                  </div>
                {:else}
                  <button
                    class="btn btn-primary min-w-[8rem]"
                    on:click|preventDefault={() => (showNewDraftOverlay = true)}
                  >
                    {$_("Edit")}
                  </button>
                  <div class="italic text-black/50">
                    {otype === "deal"
                      ? $_("Create a new draft version of this deal")
                      : $_("Create a new draft version of this investor")}
                  </div>
                {/if}
              </div>
            {/if}
            {#if isActiveVersion && isAdmin($page.data.user)}
              <div class="flex items-center gap-4">
                <div>
                  <button
                    class="btn btn-danger min-w-[8rem]"
                    on:click|preventDefault={() => (showDeleteOverlay = true)}
                  >
                    {isDeleted ? $_("Undelete") : $_("Delete")}
                  </button>
                </div>
                <div class="italic text-black/50">
                  {#if isDeleted}
                    {otype === "deal"
                      ? $_("Reactivate this deal")
                      : $_("Reactivate this investor")}
                  {:else}
                    {otype === "deal"
                      ? $_("Delete this deal")
                      : $_("Delete this investor")}
                  {/if}
                </div>
              </div>
            {:else if isCurrentDraft && isAuthorized($page.data.user, object)}
              <div class="flex items-center gap-4">
                <div>
                  <button
                    class="btn btn-danger min-w-[8rem]"
                    on:click|preventDefault={() => (showDeleteOverlay = true)}
                  >
                    {$_("Remove")}
                  </button>
                </div>
                <div class="italic text-black/50">
                  {otype === "deal"
                    ? $_("Completely removes this version of the deal")
                    : $_("Completely removes this version of the investor")}
                </div>
              </div>
            {/if}
            {#if otype === "deal" && isAdmin($page.data.user)}
              <div class="flex items-center gap-4">
                <div>
                  <button
                    class="btn btn-gray btn-sm min-w-[8rem]"
                    on:click|preventDefault={() => dispatch("copy")}
                  >
                    {$_("Copy deal")}
                  </button>
                </div>
                <div class="italic text-black/50">
                  {$_("Copy this deal")}
                </div>
              </div>
            {/if}
          </div>
        </div>
        <slot name="visibility" />
      </div>
    </div>
    <ManageHeaderLogbook
      workflowInfos={object.workflowinfos}
      {extraUserIDs}
      on:addComment
    />
  </div>
</div>

{#if showNewDraftOverlay}
  <ManageOverlay
    bind:visible={showNewDraftOverlay}
    title={$_("Create a new draft")}
    commentInput={false}
    on:submit={() => goto(`/${otype}/edit/${object.id}/${objectVersion ?? ""}`)}
  >
    {$_(
      "You are not the author of this version. Therefore, a new version will be created if you proceed.",
    )}
  </ManageOverlay>
{/if}

{#if showToDraftOverlay}
  <ManageOverlay
    bind:visible={showToDraftOverlay}
    title={$_("Request improvement")}
    assignToUserInput
    commentRequired
    toUser={lastVersion?.created_by?.id}
    toUserRequired
    {extraUserIDs}
    on:submit={sendToDraft}
  />
{/if}

{#if showDeleteOverlay}
  <ManageOverlay
    bind:visible={showDeleteOverlay}
    commentRequired
    on:submit={doDelete}
    title={objectVersion
      ? otype === "deal"
        ? $_("Remove deal version")
        : $_("Remove investor version")
      : isDeleted
      ? otype === "deal"
        ? $_("Reactivate deal")
        : $_("Reactivate investor")
      : otype === "deal"
      ? $_("Delete deal")
      : $_("Delete investor")}
  />
{/if}

{#if showSendToActivationOverlay}
  <ManageOverlay
    bind:visible={showSendToActivationOverlay}
    commentInput
    on:submit={sendToActivation}
    title={$_("Submit for activation")}
  />
{/if}

{#if showActivateOverlay}
  <ManageOverlay
    bind:visible={showActivateOverlay}
    commentInput
    on:submit={activate}
    title={$_("Activate")}
  />
{/if}

<style>
  .status-field {
    @apply relative flex h-16 w-1/4 items-center justify-center border-2 bg-zinc-300 pl-5;
  }
  .status-field:before {
    @apply content-[""];
    @apply border-y border-y-[31px] border-y-transparent;
    @apply border-l border-l-[18px] border-l-neutral-200;
    @apply absolute inset-y-0 left-0;
  }
  .status-field:after {
    @apply content-[""];
    @apply border-y border-y-[31px] border-y-transparent;
    @apply border-l border-l-[18px] border-l-zinc-300;
    @apply absolute inset-y-0 right-[-17px];
  }
  .status-field:first-child:before {
    @apply hidden;
  }
  .status-field:last-child:after {
    @apply hidden;
  }

  .status-field.active {
    @apply bg-pelorous-300 text-white;
  }
  .status-field.active:after {
    @apply border-l-pelorous-300;
  }
</style>
