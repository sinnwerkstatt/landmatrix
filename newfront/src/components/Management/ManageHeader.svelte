<script lang="ts">
  import dayjs from "dayjs";
  import { createEventDispatcher } from "svelte";
  import { _ } from "svelte-i18n";
  import { goto } from "$app/navigation";
  import { page } from "$app/stores";
  import { isAuthorized } from "$lib/helpers";
  import type { Obj, ObjVersion } from "$lib/types/generics";
  import { UserLevel } from "$lib/types/user";
  import DateTimeField from "$components/Fields/Display/DateTimeField.svelte";
  import ManageOverlay from "$components/Management/ManageOverlay.svelte";
  import ManageHeaderLogbook from "./ManageHeaderLogbook.svelte";

  const dispatch = createEventDispatcher();

  export let object: Obj;
  export let objectVersion: number;
  export let otype: "deal" | "investor" = "deal";

  let showToDraftOverlay = false;
  let showDeleteOverlay = false;
  let showSendToActivationOverlay = false;
  let showActivateOverlay = false;
  let showNewDraftOverlay = false;

  let lastVersion: ObjVersion;
  $: lastVersion = object.versions[0];

  let hasActive: boolean;
  $: hasActive = !!object.status;

  let isActiveWithDraft: boolean;
  $: isActiveWithDraft = !objectVersion && !!object.draft_status;

  let isEditable: boolean;
  $: isEditable =
    (!objectVersion && object.status === 4) || isActiveWithDraft
      ? false
      : object.draft_status === 4
      ? $page.stuff.user.level === UserLevel.ADMINISTRATOR
      : isAuthorized($page.stuff.user, object);

  let isOldDraft: boolean;
  $: isOldDraft = !!objectVersion && lastVersion.id !== objectVersion;

  let isDraftWithActive: boolean;
  $: isDraftWithActive =
    objectVersion && [2, 3].includes(object.status)
      ? true
      : isOldDraft && [2, 3].includes(lastVersion?.[otype]?.status);

  let hasNewerDraft: boolean;
  $: hasNewerDraft = isActiveWithDraft
    ? true
    : isOldDraft && !!lastVersion?.[otype]?.draft_status;

  $: isDeletable =
    isActiveWithDraft || isOldDraft
      ? false
      : object.draft_status === null || object.draft_status === 4
      ? $page.stuff.user.level === UserLevel.ADMINISTRATOR
      : isAuthorized($page.stuff.user, object);
  $: isDeleted = !objectVersion && object?.status === 4;

  $: deleteTitle = $_(
    objectVersion
      ? otype === "deal"
        ? "Delete deal version"
        : "Delete investor version"
      : object.status === 4
      ? otype === "deal"
        ? "Reactivate deal"
        : "Reactivate investor"
      : otype === "deal"
      ? "Delete deal"
      : "Delete investor"
  );

  function doDelete({ detail: { comment } }): void {
    dispatch("delete", { comment });
    showDeleteOverlay = false;
  }
  function sendToDraft({ detail: { comment, to_user } }): void {
    dispatch("changeStatus", { transition: "TO_DRAFT", comment, to_user });
    showToDraftOverlay = false;
  }
  function sendToActivation({ detail: { comment } }) {
    dispatch("changeStatus", { transition: "TO_ACTIVATION", comment });
    showSendToActivationOverlay = false;
  }
  function activate({ detail: { comment } }) {
    dispatch("changeStatus", { transition: "ACTIVATE", comment });
    showActivateOverlay = false;
  }
</script>

<div class="my-6">
  <div class="p-0 flex flex-col lg:flex-row">
    <div class="grow-[2] bg-neutral-200">
      <div class="flex justify-center gap-4 -mt-5">
        {#if isDraftWithActive}
          <a href="/{otype}/{object.id}" class="btn btn-gray">
            {$_("Go to active version")}
          </a>
        {/if}
        {#if hasNewerDraft}
          <a href="/{otype}/{object.id}/{lastVersion.id}/" class="btn btn-gray">
            {$_("Go to current draft")}
          </a>
        {/if}
      </div>

      <div
        class="title-and-date-bar mt-4 p-4 flex flex-row justify-between w-full gap-4"
      >
        <div>
          <h1 class="text-black text-3xl mb-0">
            <slot name="heading" />
          </h1>
        </div>
        <div class="flex items-center bg-gray-50 rounded p-3 my-2 w-auto">
          <div class="mr-10 md:mx-5 text-xs md:text-sm text-lm-dark">
            {$_("Created")}<br />
            <DateTimeField value={object.created_at} />
          </div>
          <div class="mr-10 md:mx-5 text-xs md:text-sm text-lm-dark">
            {$_("Last update")}<br />
            <DateTimeField value={object.modified_at} />
          </div>
          {#if object.fully_updated_at}
            <div class="mr-10 md:mx-5 text-xs md:text-sm text-lm-dark">
              {$_("Last full update")}<br />
              <DateTimeField value={object.fully_updated_at} />
            </div>
          {/if}
        </div>
      </div>

      {#if object.status === 4}
        <div
          class="flex items-center justify-center h-16 w-full text-white bg-[hsl(0,33%,68%)] text-lg border-2"
        >
          {$_("Deleted")}
        </div>
      {:else if object.status !== 1 && !objectVersion}
        <div
          class="flex items-center justify-center h-16 w-full text-white bg-pelorous-300 font-medium text-lg border-2"
        >
          {$_("Activated")}
        </div>
      {:else}
        <div>
          <div class="flex flex-wrap w-full justify-between text-center">
            <div
              class:active={[1, 4].includes(object.draft_status)}
              class="status-field z-[3]"
            >
              <span>{$_("Draft")}</span>
              {#if object.draft_status === 4}
                <span class="font-bold text-red-600 pl-2">
                  ({$_("Rejected")})
                </span>
              {/if}
            </div>
            <div class:active={object.draft_status === 2} class="status-field z-[2]">
              <span>{$_("Submitted for review")}</span>
            </div>
            <div class:active={object.draft_status === 3} class="status-field z-[1]">
              <span>{$_("Submitted for activation")}</span>
            </div>
            <div class:active={object.draft_status === null} class="status-field">
              <span>{$_("Activated")}</span>
            </div>
          </div>
          <div class="flex workflow-buttons">
            <div class="flex-1 text-right">
              {#if object.draft_status === 1 && isAuthorized($page.stuff.user, object)}
                <button
                  type="button"
                  class:disabled={lastVersion.id !== +objectVersion}
                  title={otype === "deal"
                    ? $_("Submits the deal for review")
                    : $_("Submits the investor for review")}
                  class="btn btn-pelorous"
                  on:click={() => dispatch("sendToReview")}
                >
                  {$_("Submit for review")}
                </button>
              {/if}
              {#if (object.draft_status === 2 || object.draft_status === 3) && isAuthorized($page.stuff.user, object)}
                <button
                  type="button"
                  class:disabled={lastVersion.id !== +objectVersion}
                  title={otype === "deal"
                    ? $_(
                        "Send a request of improvent and create a new draft version of the deal"
                      )
                    : $_(
                        "Send a request of improvent and create a new draft version of the investor"
                      )}
                  class="btn btn-primary"
                  on:click={() => (showToDraftOverlay = true)}
                >
                  {$_("Request improvement")}
                </button>
              {/if}
            </div>
            <div class="flex-1 text-center">
              {#if object.draft_status === 2 && isAuthorized($page.stuff.user, object)}
                <button
                  type="button"
                  class:disabled={lastVersion.id !== +objectVersion}
                  title={otype === "deal"
                    ? $_("Submits the deal for activation")
                    : $_("Submits the investor for activation")}
                  class="btn btn-pelorous"
                  on:click={() => (showSendToActivationOverlay = true)}
                >
                  {$_("Submit for activation")}
                </button>
              {/if}
            </div>
            <div class="flex-1 text-left">
              {#if object.draft_status === 3 && isAuthorized($page.stuff.user, object)}
                <button
                  type="button"
                  class:disabled={lastVersion.id !== +objectVersion}
                  title={hasActive
                    ? $_(
                        "Activates submitted version replacing currently active version"
                      )
                    : otype === "deal"
                    ? $_("Sets the deal active")
                    : $_("Sets the investor active")}
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
      <div class="p-4 flex w-full flew-row gap-4">
        <div class="flex-auto">
          {#if lastVersion}
            <div class="text-sm mb-4">
              {$_("Last changes")}
              {#if lastVersion.created_by}
                <span>
                  {$_("by")}
                  {lastVersion.created_by.full_name}
                </span>
              {/if}
              on
              {dayjs(lastVersion.created_at).format("YYYY-MM-DD HH:mm")}
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
          <div class="action-buttons">
            {#if isEditable}
              <div class="action-button">
                <div class="inline-block">
                  {#if !objectVersion || $page.stuff.user.id === object.created_by?.id}
                    <a
                      class:disabled={isOldDraft}
                      href="/{otype}/edit/{object.id}/{objectVersion ?? ''}"
                      class="btn btn-primary"
                    >
                      {$_("Edit")}
                    </a>
                  {:else}
                    <button
                      class="btn btn-primary"
                      on:click|preventDefault={() => (showNewDraftOverlay = true)}
                    >
                      {$_("Edit")}
                    </button>
                  {/if}
                </div>
                <div class="inline-block ml-4 italic text-black/50">
                  {#if object.draft_status === 1}
                    {#if !hasActive}
                      {otype === "deal"
                        ? $_("Starts editing this deal")
                        : $_("Starts editing this investor")}
                    {:else}
                      {otype === "deal"
                        ? $_("Edits this draft version")
                        : $_("Edits this investor version")}
                    {/if}
                  {:else}
                    {otype === "deal"
                      ? $_("Creates a new draft version of this deal")
                      : $_("Creates a new draft version of this investor")}
                  {/if}
                </div>
              </div>
            {/if}
            {#if isDeletable}
              <div class="action-button">
                <div class="inline-block">
                  <button
                    class="btn btn-danger"
                    on:click|preventDefault={() => (showDeleteOverlay = true)}
                  >
                    {#if isDeleted}
                      {$_("Undelete")}
                    {:else if objectVersion && !object.draft_status}
                      {otype === "deal" ? $_("Delete deal") : $_("Delete investor")}
                    {:else}
                      {$_("Delete")}
                    {/if}
                  </button>
                </div>
                <div class="inline-block ml-4 italic text-black/50">
                  {#if isDeleted}
                    {otype === "deal"
                      ? $_("Reactivate this deal")
                      : $_("Reactivate this investor")}
                  {:else if objectVersion && hasActive}
                    {otype === "deal"
                      ? $_("Deletes this draft version of the deal")
                      : $_("Deletes this draft version of the investor")}
                  {:else}
                    {otype === "deal"
                      ? $_("Deletes this deal")
                      : $_("Deletes this investor")}
                  {/if}
                </div>
              </div>
            {/if}
            {#if $page.stuff.user.level === UserLevel.ADMINISTRATOR && otype === "deal" && object.status !== 1}
              <div class="action-button">
                <div class="inline-block">
                  <button
                    class="btn btn-gray btn-sm"
                    on:click|preventDefault={() => dispatch("copy")}
                  >
                    {$_("Copy deal")}
                  </button>
                </div>
                <div class="inline-block ml-4 italic text-black/50">
                  {otype === "deal" ? $_("Copy this deal") : $_("Copy this investor")}
                </div>
              </div>
            {/if}
          </div>
        </div>
        <slot name="visibility" />
      </div>
    </div>
    <ManageHeaderLogbook {object} on:addComment />
  </div>
</div>

<ManageOverlay
  bind:visible={showNewDraftOverlay}
  title={$_("Create a new draft")}
  commentInput={false}
  on:submit={() => goto(`/${otype}/edit/${object.id}/${objectVersion ?? ""}`)}
>
  {$_(
    "You are not the author of this version. Therefore, a new version will be created if you proceed."
  )}
</ManageOverlay>

<ManageOverlay
  bind:visible={showToDraftOverlay}
  title={$_("Request improvement")}
  assignToUserInput
  commentRequired
  toUser={lastVersion?.created_by?.id}
  on:submit={sendToDraft}
/>

<ManageOverlay
  bind:visible={showDeleteOverlay}
  commentRequired
  on:submit={doDelete}
  title={deleteTitle}
  xtitle={objectVersion
    ? `${$_("Delete")} ${$_(otype)} ${$_("version")}`
    : `${object.status === 4 ? $_("Reactivate") : $_("Delete")} ${$_(otype)}`}
/>

<ManageOverlay
  bind:visible={showSendToActivationOverlay}
  commentInput
  on:submit={sendToActivation}
  title={$_("Submit for activation")}
/>

<ManageOverlay
  bind:visible={showActivateOverlay}
  commentInput
  on:submit={activate}
  title={$_("Activate")}
/>

<style>
  .status-field {
    @apply w-1/4 border-2 h-16 bg-zinc-300 flex items-center justify-center relative pl-5;
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
    @apply text-white bg-pelorous-300;
  }
  .status-field.active:after {
    @apply border-l-pelorous-300;
  }
</style>
