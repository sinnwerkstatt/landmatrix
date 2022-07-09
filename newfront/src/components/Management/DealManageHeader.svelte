<script lang="ts">
  import { gql } from "graphql-tag";
  import { createEventDispatcher } from "svelte";
  import { _ } from "svelte-i18n";
  import { goto } from "$app/navigation";
  import { page } from "$app/stores";
  import type { Deal } from "$lib/types/deal";
  import ManageOverlay from "$components/Management/ManageOverlay.svelte";
  import ManageHeader from "./ManageHeader.svelte";

  const dispatch = createEventDispatcher();

  export let deal: Deal;
  export let dealVersion: number;

  let fully_updated = false;

  let showSendToReviewOverlay = false;
  async function sendToReview({ detail: { comment } }) {
    await changeStatus({ detail: { transition: "TO_REVIEW", comment } });
    showSendToReviewOverlay = false;
  }

  let showCopyOverlay = false;
  async function copyDeal() {
    $page.stuff.secureApolloClient
      .mutate({
        mutation: gql`
          mutation ($id: Int!) {
            object_copy(otype: "deal", obj_id: $id) {
              objId
              objVersion
            }
          }
        `,
        variables: { id: deal.id },
      })
      .then(({ data: { object_copy } }) => {
        window.open(`/deal/${object_copy.objId}/${object_copy.objVersion}`, "_blank");
      });
    showCopyOverlay = false;
  }

  function changeStatus({ detail: { transition, comment = "", to_user = null } }) {
    $page.stuff.secureApolloClient
      .mutate({
        mutation: gql`
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
        variables: {
          id: deal.id,
          version: dealVersion,
          transition,
          comment,
          to_user_id: to_user?.id,
          fully_updated,
        },
      })
      .then(async ({ data: { change_deal_status } }) => {
        console.log(change_deal_status);
        if (transition === "ACTIVATE") {
          await goto(`/deal/${change_deal_status.dealId}/`);
        } else {
          if (dealVersion !== change_deal_status.dealVersion)
            await goto(
              `/deal/${change_deal_status.dealId}/${change_deal_status.dealVersion}/`
            );
          else dispatch("reload");
        }
      })
      .catch((error) => console.error(error));
  }
  async function deleteDeal({ detail: { comment } }) {
    $page.stuff.secureApolloClient
      .mutate({
        mutation: gql`
          mutation ($id: Int!, $version: Int, $comment: String) {
            deal_delete(id: $id, version: $version, comment: $comment)
          }
        `,
        variables: { id: deal.id, version: dealVersion, comment },
      })
      .then(async () => {
        if (dealVersion) await goto(`/deal/${deal.id}`);
        dispatch("reload");
      });
  }
</script>

<ManageHeader
  object={deal}
  objectVersion={dealVersion}
  on:send_to_review={() => (showSendToReviewOverlay = true)}
  on:change_status={changeStatus}
  on:delete={deleteDeal}
  on:copy={() => (showCopyOverlay = true)}
>
  <div slot="heading">
    {$_("Deal")} #{deal.id}
    {#if deal.country}
      <span class="whitespace-nowrap block text-base font-normal">
        {deal.country.name}
      </span>
    {/if}
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
    <label class="font-bold block mt-1">
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
