<script lang="ts">
  import { gql } from "@apollo/client/core";
  import { createEventDispatcher } from "svelte";
  import { _ } from "svelte-i18n";
  import { page } from "$app/stores";
  import type { Investor } from "$lib/types/investor";
  import ManageOverlay from "$components/Management/ManageOverlay.svelte";
  import ManageHeader from "./ManageHeader.svelte";

  const dispatch = createEventDispatcher();

  export let investor: Investor;
  export let investorVersion: number | undefined;

  let showSendToReviewOverlay = false;

  async function sendToReview() {
    await changeStatus({ transition: "TO_REVIEW" });
    showSendToReviewOverlay = false;
  }
  function addComment({ detail: { comment, send_to_user } }) {
    $page.stuff.secureApolloClient
      .mutate({
        mutation: gql`
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
        variables: {
          id: investor.id,
          version: investorVersion ?? null,
          comment: comment,
          to_user_id: send_to_user?.id,
        },
      })
      .then(() => dispatch("reload"))
      .catch((error) => console.error(error));
  }

  function changeStatus({ transition, comment = "", to_user = null }) {
    $page.stuff.secureApolloClient
      .mutate({
        mutation: gql`
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
        variables: {
          id: investor.id,
          version: investorVersion,
          transition,
          comment,
          to_user_id: to_user?.id,
        },
      })
      .then(({ data: { change_investor_status } }) => {
        console.log(change_investor_status);
        // if (transition === "ACTIVATE") {
        //   this.$router.push({
        //     name: "investor_detail",
        //     params: { investorId: change_investor_status.investorId.toString() },
        //   });
        // } else {
        //   if (
        //     parseInt(this.investorVersion) !== change_investor_status.investorVersion
        //   ) {
        //     this.$router.push({
        //       name: "investor_detail",
        //       params: {
        //         investorId: change_investor_status.investorId.toString(),
        //         investorVersion: change_investor_status.investorVersion.toString(),
        //       },
        //     });
        //   } else {
        //     console.log("Investor detail: reload");
        //     this.reloadInvestor();
        //   }
        // }
      })
      .catch((error) => console.error(error));
  }
  function copyInvestor(): void {
    $page.stuff.secureApolloClient
      .mutate({
        mutation: gql`
          mutation ($id: Int!) {
            object_copy(otype: "investor", obj_id: $id) {
              objId
              objVersion
            }
          }
        `,
        variables: { id: investor.id },
      })
      .then(({ data }) => {
        // window.open(
        //   this.$router.resolve({
        //     name: "investor_detail",
        //     params: {
        //       investorId: data.object_copy.objId,
        //       investorVersion: data.object_copy.objVersion,
        //     },
        //   }).href,
        //   "_blank"
        // );
      });
  }
  function deleteInvestor(comment) {
    $page.stuff.secureApolloClient
      .mutate({
        mutation: gql`
          mutation ($id: Int!, $version: Int, $comment: String) {
            investor_delete(id: $id, version: $version, comment: $comment)
          }
        `,
        variables: {
          id: investor.id,
          version: investorVersion ?? null,
          comment,
        },
      })
      .then(() => {
        if (investorVersion) {
          // this.$router
          //   .push({
          //     name: "investor_detail",
          //     params: { investorId: this.investorId.toString() },
          //   })
          //   .then(this.reloadInvestor);
        }
        dispatch("reload");
      });
  }
</script>

<ManageHeader
  object={investor}
  objectVersion={investorVersion}
  otype="investor"
  on:addComment={addComment}
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
    <label class="font-bold block mt-1">
      <input required type="checkbox" id="data-policy-checkbox" />
      {$_("I've read and agree to the")}
      <a href="/about/data-policy/" target="_blank">{$_("Data policy")} </a>.
    </label>
  </div>
</ManageOverlay>
