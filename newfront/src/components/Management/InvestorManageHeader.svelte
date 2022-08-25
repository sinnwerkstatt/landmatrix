<script lang="ts">
  import { gql } from "@urql/svelte";
  import { createEventDispatcher } from "svelte";
  import { _ } from "svelte-i18n";
  import { goto } from "$app/navigation";
  import { page } from "$app/stores";
  import type { Investor } from "$lib/types/investor";
  import ManageOverlay from "$components/Management/ManageOverlay.svelte";
  import ManageHeader from "./ManageHeader.svelte";

  const dispatch = createEventDispatcher();

  export let investor: Investor;
  export let investorVersion: number | undefined;

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
          ) {
            change_investor_status(
              id: $id
              version: $version
              transition: $transition
              comment: $comment
              to_user_id: $to_user_id
            ) {
              investorId
              investorVersion
            }
          }
        `,
        {
          id: investor.id,
          version: investorVersion,
          transition,
          comment,
          to_user_id: toUser?.id,
        }
      )
      .toPromise()
      .then(async ({ data: { change_investor_status } }) => {
        console.log(change_investor_status);
        if (transition === "ACTIVATE") {
          await goto(`/investor/${change_investor_status.investorId}/`);
        } else if (investorVersion !== change_investor_status.investorVersion)
          await goto(
            `/investor/${change_investor_status.investorId}/${change_investor_status.investorVersion}/`
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
            add_investor_comment(
              id: $id
              version: $version
              comment: $comment
              to_user_id: $to_user_id
            ) {
              investorId
              investorVersion
            }
          }
        `,
        {
          id: investor.id,
          version: investorVersion ?? null,
          comment: comment,
          to_user_id: sendToUser?.id,
        }
      )
      .toPromise()
      .then(() => dispatch("reload"))
      .catch((error) => console.error(error));
  }

  function deleteInvestor({ detail: { comment } }) {
    $page.data.urqlClient
      .mutation(
        gql`
          mutation ($id: Int!, $version: Int, $comment: String) {
            investor_delete(id: $id, version: $version, comment: $comment)
          }
        `,
        { id: investor.id, version: investorVersion, comment }
      )
      .toPromise()
      .then(async (dat) => {
        //todo: if it was just a draft, and we deleted the whole thing, jump to investor list
        console.log(dat);
        if (investorVersion) await goto(`/investor/${investor.id}`);
        dispatch("reload");
      });
  }
</script>

<ManageHeader
  object={investor}
  objectVersion={investorVersion}
  otype="investor"
  on:addComment={addComment}
  on:changeStatus={changeStatus}
  on:delete={deleteInvestor}
  on:sendToReview={() => (showSendToReviewOverlay = true)}
>
  <div slot="heading">
    {investor.name} <small>#{investor.id}</small>
  </div>
</ManageHeader>

<ManageOverlay
  bind:visible={showSendToReviewOverlay}
  title={$_("Submit for review")}
  commentInput
  on:submit={sendToReview}
>
  <div class="mb-6">
    <label for="data-policy-checkbox" class="underline">{$_("Data policy")}</label>
    <label class="mt-1 block font-bold">
      <input required type="checkbox" id="data-policy-checkbox" />
      {$_("I've read and agree to the")}
      <a href="/about/data-policy/" target="_blank">{$_("Data policy")} </a>.
    </label>
  </div>
</ManageOverlay>
