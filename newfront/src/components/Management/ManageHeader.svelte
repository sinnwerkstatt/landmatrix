<script lang="ts">
  import dayjs from "dayjs";
  import { createEventDispatcher } from "svelte";
  import { _ } from "svelte-i18n";
  import { page } from "$app/stores";
  import type { Obj, ObjVersion } from "$lib/types/generics";
  import ManageOverlay from "$components/Management/ManageOverlay.svelte";
  import DateTimeField from "../Fields/Display/DateTimeField.svelte";
  import ManageHeaderLogbook from "./ManageHeaderLogbook.svelte";

  const dispatch = createEventDispatcher();

  export let object: Obj;
  export let objectVersion: number;
  export let otype = "deal";

  function is_authorized(obj: Obj): boolean {
    const { id, role } = $page.stuff.user;
    switch (obj.draft_status) {
      case null: // anybody who has a ROLE
        return ["ADMINISTRATOR", "EDITOR", "REPORTER"].includes(role);
      case 1: // the Reporter of the Object or Editor,Administrator
        return (
          ["ADMINISTRATOR", "EDITOR"].includes(role) ||
          obj.versions[0]?.created_by?.id === id
        );
      case 2: // at least Editor
        return ["ADMINISTRATOR", "EDITOR"].includes(role);
      case 3: // only Admins
        return role === "ADMINISTRATOR";
      default:
        return false;
    }
  }

  let showToDraftOverlay = false;
  let showDeleteOverlay = false;
  let showSendToActivationOverlay = false;
  let showActivateOverlay = false;
  let show_new_draft_overlay = false;

  let last_version: ObjVersion;
  $: last_version = object?.versions[0] ?? undefined;
  let has_active: boolean;
  $: has_active = !!object?.status;

  $: is_active_with_draft = !objectVersion && !!object.draft_status;
  $: is_editable = true;
  //   is_editable(): boolean {
  //     // object ist deleted
  //     if (!this.objectVersion && this.object.status === 4) return false;
  //     if (this.is_active_with_draft) return false;
  //     if (this.object.draft_status === 4)
  //       return this.$store.state.user.role === "ADMINISTRATOR";
  //     return is_authorized(this.object);
  //   },

  $: is_deletable =
    is_active_with_draft || is_old_draft
      ? false
      : object.draft_status === null || object.draft_status === 4
      ? $page.stuff.user.role === "ADMINISTRATOR"
      : is_authorized(object);
  $: is_deleted = !objectVersion && object?.status === 4;

  $: latest_object_version = object?.versions.find(
    (v: ObjVersion) => v.id === last_version.id
  )[otype];

  $: is_draft_with_active =
    objectVersion && [2, 3].includes(object.status)
      ? true
      : is_old_draft && [2, 3].includes(latest_object_version?.status);
  $: is_old_draft = !!objectVersion && last_version.id !== +objectVersion;

  $: has_newer_draft = is_active_with_draft
    ? true
    : is_old_draft && !!latest_object_version?.draft_status;

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

  let transitionToUser;
  //   transition_to_user(): User {
  //     let latest_draft_creation = this.object.workflowinfos.find((v) => {
  //       return !v.draft_status_before && v.draft_status_after === 1;
  //     });
  //     if (!latest_draft_creation)
  //       latest_draft_creation = this.object.workflowinfos.find((v) => {
  //         return !v.draft_status_before && v.draft_status_after === 2;
  //       });
  //     return latest_draft_creation.from_user;
  //   },
  // },

  function object_detail_path(obID: number, obV?: number) {
    if (otype === "deal") return obV ? `/deal/${obID}/${obV}` : `/deal/${obID}`;
    return obV ? `/investor/${obID}/${obV}` : `/investor/${obID}`;
  }

  function object_edit_path(obID: number, obV?: number) {
    if (otype === "deal")
      return obV ? `/deal/edit/${obID}/${obV}` : `/deal/edit/${obID}`;
    return obV ? `/investor/edit/${obID}/${obV}` : `/investor/edit/${obID}`;
  }

  //   object_edit_path(obID: number, obV: number | string): Location {
  //     return this.otype === "deal"
  //       ? {
  //           name: "deal_edit",
  //           params: { dealId: obID.toString(), dealVersion: obV?.toString() },
  //         }
  //       : {
  //           name: "investor_edit",
  //           params: { investorId: obID.toString(), investorVersion: obV?.toString() },
  //         };
  //   },
  //   object_compare_path(
  //     oID: number,
  //     fromVersion: number,
  //     toVersion: number
  //   ): Location {
  //     return this.otype === "deal"
  //       ? {
  //           name: "deal_compare",
  //           params: {
  //             dealId: oID.toString(),
  //             fromVersion: fromVersion.toString(),
  //             toVersion: toVersion.toString(),
  //           },
  //         }
  //       : {
  //           name: "investor_compare",
  //           params: {
  //             investorId: oID.toString(),
  //             fromVersion: fromVersion.toString(),
  //             toVersion: toVersion.toString(),
  //           },
  //         };
  //   },
  function doDelete({ comment }): void {
    dispatch("delete", comment);
    showDeleteOverlay = false;
  }
  function sendToDraft({ comment, to_user }): void {
    console.log("to_draft", { comment, to_user });
    dispatch("change_status", { transition: "TO_DRAFT", comment, to_user });
    showToDraftOverlay = false;
  }
  function sendToActivation({ comment }) {
    dispatch("change_status", { comment, transition: "TO_ACTIVATION" });
    showSendToActivationOverlay = false;
  }
  function activate({ comment }) {
    dispatch("change_status", { comment, transition: "ACTIVATE" });
    showActivateOverlay = false;
  }
  // },
</script>

<div class="my-6">
  <div class="p-0 flex flex-col lg:flex-row">
    <div class="grow-[2] bg-neutral-200">
      <div class="flex justify-center gap-4 z-[1] -mt-5">
        {#if is_draft_with_active}
          <a href={object_detail_path(object.id)} class="btn btn-gray">
            {$_("Go to active version")}
          </a>
        {/if}
        {#if has_newer_draft}
          <a href={object_detail_path(object.id, last_version.id)} class="btn btn-gray">
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
        <div class="status-and-progress-buttons">
          <div class="fat-stati">
            <div class="text-white bg-[hsl(0,33%,68%)]">
              {$_("Deleted")}
            </div>
          </div>
        </div>
      {:else if object.status !== 1 && !objectVersion}
        <div class="status-and-progress-buttons">
          <div class="fat-stati">
            <div class="active">{$_("Activated")}</div>
          </div>
        </div>
      {:else}
        <div class="">
          <div class="status-and-progress">
            <div
              class:active={[1, 4].includes(object.draft_status)}
              class="status-field"
            >
              <span>{$_("Draft")}</span>
              {#if object.draft_status === 4}
                <span class="font-bold text-red-600 pl-2">
                  ({$_("Rejected")})
                </span>
              {/if}
            </div>
            <div class:active={object.draft_status === 2} class="status-field">
              <span>{$_("Submitted for review")}</span>
            </div>
            <div class:active={object.draft_status === 3} class="status-field">
              <span>{$_("Submitted for activation")}</span>
            </div>
            <div class:active={object.draft_status === null} class="status-field">
              <span>{$_("Activated")}</span>
            </div>
          </div>
          <div class="row workflow-buttons">
            <div class="col text-right">
              {#if object.draft_status === 1 && is_authorized(object)}
                <a
                  class:disabled={last_version.id !== +objectVersion}
                  title={otype === "deal"
                    ? $_("Submits the deal for review")
                    : $_("Submits the investor for review")}
                  class="btn btn-pelorous"
                  on:click={() => dispatch("send_to_review")}
                >
                  {$_("Submit for review")}
                </a>
              {/if}
              {#if (object.draft_status === 2 || object.draft_status === 3) && is_authorized(object)}
                <button
                  type="button"
                  class:disabled={last_version.id !== +objectVersion}
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
            <div class="col text-center">
              {#if object.draft_status === 2 && is_authorized(object)}
                <button
                  type="button"
                  class:disabled={last_version.id !== +objectVersion}
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
            <div class="col text-left">
              {#if object.draft_status === 3 && is_authorized(object)}
                <button
                  type="button"
                  class:disabled={last_version.id !== +objectVersion}
                  title={has_active
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
        <div class="grow-[2] basis-0">
          {#if last_version}
            <div class="text-sm mb-4">
              {$_("Last changes")}
              {#if last_version.created_by}
                <span>
                  {$_("by")}
                  {last_version.created_by.full_name}
                </span>
              {/if}
              on
              {dayjs(last_version.created_at).format("YYYY-MM-DD HH:mm")}
              <br />
              {#if object.versions.length > 1}
                <a
                  href="
                        object_compare_path(
                          object.id,
                          object.versions[1].id,
                          object.versions[0].id
                        )
                      "
                >
                  {$_("Show latest changes")}
                </a>
              {/if}
            </div>
          {/if}
          <div class="action-buttons">
            {#if is_editable}
              <div class="action-button">
                <div class="inline-block">
                  {#if !objectVersion || $page.stuff.user.id === object.modified_by?.id}
                    <a
                      class:disabled={is_old_draft}
                      href={object_edit_path(object.id, last_version.id)}
                      class="btn btn-primary"
                    >
                      {$_("Edit")}
                    </a>
                  {:else}
                    <button
                      class="btn btn-primary"
                      on:click|preventDefault={() => (show_new_draft_overlay = true)}
                    >
                      {$_("Edit")}
                    </button>
                  {/if}
                </div>
                <div class="inline-block ml-4 italic text-black/50">
                  {#if object.draft_status === 1}
                    {#if !has_active}
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
            {#if is_deletable}
              <div class="action-button">
                <div class="inline-block">
                  <button
                    class="btn btn-danger"
                    on:click|preventDefault={() => (showDeleteOverlay = true)}
                  >
                    {#if is_deleted}
                      {$_("Undelete")}
                    {:else if objectVersion && !object.draft_status}
                      {otype === "deal" ? $_("Delete deal") : $_("Delete investor")}
                    {:else}
                      {$_("Delete")}
                    {/if}
                  </button>
                </div>
                <div class="inline-block ml-4 italic text-black/50">
                  {#if is_deleted}
                    {otype === "deal"
                      ? $_("Reactivate this deal")
                      : $_("Reactivate this investor")}
                  {:else if objectVersion && has_active}
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
            {#if $page.stuff.user.role === "ADMINISTRATOR" && otype === "deal"}
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
    <ManageHeaderLogbook
      {object}
      {objectVersion}
      on:add_comment={(e) => dispatch("add_comment", e)}
    />
  </div>

  <!--    <Overlay-->
  <!--      v-if="show_new_draft_overlay"-->
  <!--      :comment-input="false"-->
  <!--      :title="$_('Create a new draft').toString()"-->
  <!--      @cancel="show_new_draft_overlay = false"-->
  <!--      @submit="() => $router.push(object_edit_path(object.id, objectVersion))"-->
  <!--    >-->
  <!--      {-->
  <!--        $_(-->
  <!--          "You are not the author of this version. Therefore, a new version will be created if you proceed."-->
  <!--        )-->
  <!--      }-->
  <!--    </Overlay>-->

  <ManageOverlay
    bind:visible={showToDraftOverlay}
    title={$_("Request improvement")}
    assignToUserInput
    commentRequired
    toUser={transitionToUser}
    on:submit={sendToDraft}
  />

  <ManageOverlay
    bind:visible={showDeleteOverlay}
    commentRequired
    on:submit={doDelete}
    title={deleteTitle}
  />

  <ManageOverlay
    bind:visible={showSendToActivationOverlay}
    commentInput
    on:submit={sendToActivation}
  />

  <ManageOverlay bind:visible={showActivateOverlay} commentInput on:submit={activate} />
</div>

<!--<style lang="scss" scoped>-->
<!--  $arrow-height: 34px;-->
<!--  $max-z-index: 10;-->

<!--  .status-and-progress-buttons {-->
<!--    display: flex;-->
<!--    flex-flow: column;-->
<!--    margin-bottom: 2rem;-->

<!--    > div {-->
<!--      width: 100%;-->
<!--    }-->

<!--    .fat-stati {-->
<!--      display: flex;-->
<!--      flex-flow: row wrap;-->
<!--      margin-top: 1rem;-->

<!--      @media (max-width: 400px) {-->
<!--        font-size: 0.9rem;-->
<!--        line-height: 1.1;-->
<!--      }-->

<!--      > div {-->
<!--        position: relative;-->
<!--        margin: 0.5rem 0.3rem;-->
<!--        padding: 0.5rem 0 0.5rem 1.3rem;-->
<!--        background: #dbdbdb;-->
<!--        flex-grow: 1;-->
<!--        text-align: center;-->
<!--        height: $arrow-height * 2;-->
<!--        display: flex;-->
<!--        align-items: center;-->
<!--        justify-content: center;-->
<!--        opacity: 0.7;-->

<!--        &.active {-->
<!--          background: #93c7c8;-->
<!--          color: white;-->

<!--          &:after {-->
<!--            border-left-color: #93c7c8;-->
<!--          }-->
<!--        }-->

<!--        @for $i from 0 to $max-z-index {-->
<!--          &:nth-child(#{$i + 1}) {-->
<!--            z-index: ($max-z-index - $i);-->
<!--          }-->
<!--        }-->

<!--        &:before {-->
<!--          // arrow from the left-->
<!--          content: "";-->
<!--          border-left: $arrow-height/2 solid #e5e5e5;-->
<!--          border-top: $arrow-height solid transparent;-->
<!--          border-bottom: $arrow-height solid transparent;-->
<!--          height: 0;-->
<!--          width: 0;-->
<!--          position: absolute;-->
<!--          left: 0;-->
<!--          top: 0;-->
<!--          bottom: 0;-->
<!--        }-->

<!--        &:after {-->
<!--          // arrow to the right-->
<!--          content: "";-->
<!--          border-left: $arrow-height/2 solid #dbdbdb;-->
<!--          border-top: $arrow-height solid transparent;-->
<!--          border-bottom: $arrow-height solid transparent;-->
<!--          height: 0;-->
<!--          width: 0;-->
<!--          position: absolute;-->
<!--          right: -($arrow-height - 1)/2;-->
<!--          top: 0;-->
<!--          bottom: 0;-->
<!--        }-->

<!--        &:first-child {-->
<!--          margin-left: 0;-->
<!--          padding-left: 0.2rem;-->

<!--          &:before {-->
<!--            display: none;-->
<!--          }-->
<!--        }-->

<!--        &:last-child {-->
<!--          margin-right: 0;-->

<!--          &:after {-->
<!--            display: none;-->
<!--          }-->
<!--        }-->
<!--      }-->
<!--    }-->
<!--  }-->

<!--    .action-button {-->
<!--      margin-bottom: 0.5em;-->

<!--      &:not(:last-child) {-->
<!--        margin-bottom: 7px;-->
<!--      }-->

<!--      align-items: center;-->

<!--    }-->
<!--  }-->
<!--</style>-->
