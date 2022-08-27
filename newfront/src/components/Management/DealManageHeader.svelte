<script lang="ts">
  import { gql } from "@urql/svelte";
  import { createEventDispatcher } from "svelte";
  import { _ } from "svelte-i18n";
  import { goto } from "$app/navigation";
  import { page } from "$app/stores";
  import { isAuthorized } from "$lib/helpers";
  import type { Deal } from "$lib/types/deal";
  import type { User } from "$lib/types/user";
  import CheckCircleIcon from "$components/icons/CheckCircleIcon.svelte";
  import CheckIcon from "$components/icons/CheckIcon.svelte";
  import EyeIcon from "$components/icons/EyeIcon.svelte";
  import EyeSlashIcon from "$components/icons/EyeSlashIcon.svelte";
  import MinusIcon from "$components/icons/MinusIcon.svelte";
  import XIcon from "$components/icons/XIcon.svelte";
  import CheckboxSwitch from "$components/LowLevel/CheckboxSwitch.svelte";
  import ManageOverlay from "$components/Management/ManageOverlay.svelte";
  import ManageHeader from "./ManageHeader.svelte";

  const dispatch = createEventDispatcher();

  export let deal: Deal;
  export let dealVersion: number;

  let fully_updated = false;

  $: isEditable =
    !dealVersion && deal.status === 4
      ? false
      : !dealVersion && !!deal.draft_status
      ? false
      : isAuthorized($page.data.user, deal);

  let showSendToReviewOverlay = false;
  async function sendToReview({ detail: { comment } }) {
    await changeStatus({ detail: { transition: "TO_REVIEW", comment } });
    showSendToReviewOverlay = false;
  }

  function changeStatus({ detail: { transition, comment = "", toUser = null } }) {
    $page.data.urqlClient
      .mutation(
        gql`
          mutation (
            $id: Int!
            $version: Int!
            $transition: WorkflowTransition!
            $comment: String
            $to_user_id: Int
            $fully_updated: Boolean
          ) {
            change_deal_status(
              id: $id
              version: $version
              transition: $transition
              comment: $comment
              to_user_id: $to_user_id
              fully_updated: $fully_updated
            ) {
              dealId
              dealVersion
            }
          }
        `,
        {
          id: deal.id,
          version: dealVersion,
          transition,
          comment,
          to_user_id: toUser?.id,
          fully_updated,
        }
      )
      .toPromise()
      .then(async ({ data: { change_deal_status } }) => {
        if (transition === "ACTIVATE") {
          await goto(`/deal/${change_deal_status.dealId}/`);
        } else if (dealVersion !== change_deal_status?.dealVersion)
          await goto(
            `/deal/${change_deal_status.dealId}/${change_deal_status.dealVersion}/`
          );
        else dispatch("reload");
      })
      .catch((error) => console.error(error));
  }

  function addComment({ detail: { comment, sendToUser } }) {
    $page.data.urqlClient
      .mutation(
        gql`
          mutation ($id: Int!, $version: Int, $comment: String!, $to_user_id: Int) {
            add_deal_comment(
              id: $id
              version: $version
              comment: $comment
              to_user_id: $to_user_id
            ) {
              dealId
              dealVersion
            }
          }
        `,
        {
          id: deal.id,
          version: dealVersion ?? null,
          comment: comment,
          to_user_id: sendToUser?.id,
        }
      )
      .toPromise()
      .then(() => dispatch("reload"))
      .catch((error) => console.error(error));
  }

  async function deleteDeal({ detail: { comment } }) {
    $page.data.urqlClient
      .mutation(
        gql`
          mutation ($id: Int!, $version: Int, $comment: String) {
            deal_delete(id: $id, version: $version, comment: $comment)
          }
        `,
        { id: deal.id, version: dealVersion, comment }
      )
      .toPromise()
      .then(async (dat) => {
        //todo: if it was just a draft, and we deleted the whole thing, jump to deal list
        console.log(dat);
        if (dealVersion) await goto(`/deal/${deal.id}`);
        dispatch("reload");
      });
  }

  let showCopyOverlay = false;
  async function copyDeal() {
    $page.data.urqlClient
      .mutation(
        gql`
          mutation ($id: Int!) {
            object_copy(otype: "deal", obj_id: $id) {
              objId
              objVersion
            }
          }
        `,
        { id: deal.id }
      )
      .toPromise()
      .then(({ data: { object_copy } }) => {
        window.open(`/deal/${object_copy.objId}/${object_copy.objVersion}`, "_blank");
      });
    showCopyOverlay = false;
  }

  let showConfidentialOverlay = false;
  async function toggleConfidential(data: {
    force: boolean;
    comment;
    string;
    to_user: User;
  }) {
    if (!isEditable) return;

    if (data.force) {
      if (deal.confidential) {
        setConfidential(false);
        showConfidentialOverlay = false;
      } else {
        setConfidential(true, data.comment);
        showConfidentialOverlay = false;
      }
    } else {
      showConfidentialOverlay = true;
    }
  }

  function setConfidential(confidential, comment = ""): void {
    $page.data.urqlClient
      .mutation(
        gql`
          mutation (
            $id: Int!
            $confidential: Boolean!
            $version: Int
            $comment: String
          ) {
            deal_set_confidential(
              id: $id
              confidential: $confidential
              version: $version
              comment: $comment
            )
          }
        `,
        { id: deal.id, version: dealVersion, confidential, comment }
      )
      .toPromise()
      .then(() => dispatch("reload"));
  }
</script>

<ManageHeader
  object={deal}
  objectVersion={dealVersion}
  on:addComment={addComment}
  on:changeStatus={changeStatus}
  on:copy={() => (showCopyOverlay = true)}
  on:delete={deleteDeal}
  on:sendToReview={() => (showSendToReviewOverlay = true)}
>
  <div slot="heading">
    {$_("Deal")} #{deal.id}
    {#if deal.country}
      <span class="block whitespace-nowrap text-base font-normal">
        {deal.country.name}
      </span>
    {/if}
  </div>
  <div slot="visibility" class="flex-auto">
    <div class="mb-2 flex items-center gap-1 text-lg">
      {#if deal.is_public}
        <EyeIcon class="h-6 w-6 text-orange" /> {$_("Publicly visible")}
      {:else}
        <EyeSlashIcon class="h-6 w-6 text-gray-500" />
        <span class="text-gray-500">{$_("Not publicly visible")}</span>
      {/if}
    </div>

    {#if isEditable}
      <CheckboxSwitch
        checked={deal.confidential}
        title={deal.confidential_comment}
        on:change={toggleConfidential}
      >
        {deal.confidential ? $_("Confidential") : $_("Not confidential")}
      </CheckboxSwitch>
    {/if}
    <ul>
      {#if !isEditable}
        <li class="flex items-center gap-1">
          {#if !deal.confidential}
            <CheckIcon class="mx-1 h-4 w-4" /> {$_("Not confidential")}
          {:else}
            <XIcon class="mx-1 h-4 w-4" /> {$_("Confidential")}
          {/if}
        </li>
      {/if}

      <li class="flex items-center gap-1">
        {#if deal.country}
          <CheckIcon class="mx-1 h-4 w-4" /> {$_("Target country is set")}
        {:else}
          <XIcon class="mx-1 h-4 w-4" /> {$_("Target country is NOT set")}
        {/if}
      </li>

      <li class="flex items-center gap-1 whitespace-nowrap">
        {#if deal.datasources?.length > 0}
          <CheckIcon class="mx-1 h-4 w-4" />
          {$_("At least one data source")} ({deal.datasources.length})
        {:else}
          <XIcon class="mx-1 h-4 w-4" /> {$_("No data source")}
        {/if}
      </li>

      <li class="flex items-center gap-1">
        {#if deal.has_known_investor}
          <CheckIcon class="mx-1 h-4 w-4" /> {$_("At least one investor")}
        {:else}
          <XIcon class="mx-1 h-4 w-4" /> {$_("No known investor")}
        {/if}
      </li>
    </ul>

    <div class="mt-2 flex items-center gap-1 font-bold">
      {#if deal.fully_updated}
        <CheckCircleIcon class="h-6 w-6 text-orange" />
        <span>{$_("Fully updated")}</span>
      {:else}
        <MinusIcon class="h-6 w-6 text-gray-500" />
        <span class="text-gray-500">{$_("Not fully updated")}</span>
      {/if}
    </div>
  </div>
</ManageHeader>

<ManageOverlay
  bind:visible={showSendToReviewOverlay}
  title={$_("Submit for review")}
  commentInput
  on:submit={sendToReview}
>
  <div class="mb-6">
    <div class="underline">{$_("Full update")}</div>
    <p class="mb-1">
      {$_(
        'If you have checked the information entered for every single variable, please tick the box beside "I fully updated this deal" - even if no additional information was found, but a complete search through the deal was conducted.'
      )}
    </p>
    <label class="my-1">
      <input bind:checked={fully_updated} type="checkbox" />
      {$_("I fully updated this deal.")}
    </label>
  </div>
  <div class="mb-6">
    <label for="data-policy-checkbox" class="underline">{$_("Data policy")}</label>
    <label class="mt-1 block font-bold">
      <input required type="checkbox" id="data-policy-checkbox" />
      {$_("I've read and agree to the")}
      <a href="/about/data-policy/" target="_blank">{$_("Data policy")} </a>.
    </label>
  </div>
</ManageOverlay>

<ManageOverlay
  bind:visible={showCopyOverlay}
  title={$_("Copy deal")}
  on:submit={copyDeal}
>
  <p>
    {$_(
      "This creates a completely identical copy of the deal. The copy must then be edited and adjusted to prevent identical duplicates."
    )}
  </p>
  <div class="font-medium">{$_("Do you really want to copy this deal?")}</div>
</ManageOverlay>

<ManageOverlay
  bind:visible={showConfidentialOverlay}
  on:submit={({ detail }) => toggleConfidential({ ...detail, force: true })}
  on:close={() => (deal.confidential = deal.confidential)}
  title={deal.confidential ? $_("Unset confidential") : $_("Set confidential")}
  commentRequired={!deal.confidential}
>
  <p>
    {#if deal.confidential}
      {$_(
        "If you unset the confidential flag, this deal will be publicly visible once it is set active. If you want to keep it confidential, click on 'Cancel'."
      )}
    {:else}
      {$_(
        "If you set the confidential flag, this deal will not be publicly visible anymore. If you want to keep it public, click on 'Cancel'."
      )}
    {/if}
  </p>
</ManageOverlay>
