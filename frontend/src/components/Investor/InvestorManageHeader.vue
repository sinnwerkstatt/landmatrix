<!-- eslint-disable vue/no-v-html -->
<template>
  <div>
    <GenericManageHeader
      :object="investor"
      :object-version="investorVersion"
      otype="investor"
      @add_comment="add_comment"
      @change_status="$emit('change_status', $event)"
      @delete="$emit('delete', $event)"
      @send_to_review="show_send_to_review_overlay = true"
    >
      <template #overlays>
        <Overlay
          v-if="show_send_to_review_overlay"
          :title="$t('Submit for review')"
          @cancel="show_send_to_review_overlay = false"
          @submit="send_to_review"
        >
          <p>Normal text, requiring accept button.</p>
        </Overlay>
      </template>
    </GenericManageHeader>
  </div>
</template>

<script>
  import GenericManageHeader from "$components/Management/ManageHeader";
  import Overlay from "$components/Overlay";
  import gql from "graphql-tag";

  export default {
    name: "InvestorManageHeader",
    components: {
      Overlay,
      GenericManageHeader,
    },
    props: {
      investor: { type: Object, required: true },
      investorVersion: { type: [Number, String], default: null },
    },
    data() {
      return {
        show_send_to_review_overlay: false,
      };
    },
    methods: {
      send_to_review() {
        this.$emit("change_status", { transition: "TO_REVIEW" });
        this.show_send_to_review_overlay = false;
      },
      add_comment({ comment, send_to_user }) {
        this.$apollo
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
              id: +this.investor.id,
              version: this.investorVersion ? +this.investorVersion : null,
              comment: comment,
              to_user_id: send_to_user ? +send_to_user.id : null,
            },
          })
          .then(() => {
            this.$emit("reload_investor");
          })
          .catch((error) => console.error(error));
      },
    },
  };
</script>
