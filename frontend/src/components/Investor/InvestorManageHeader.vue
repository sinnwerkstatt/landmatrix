<template>
  <div>
    <ManageHeader
      :object="investor"
      :object-version="investorVersion"
      otype="investor"
      @add_comment="add_comment"
      @change_status="$emit('change_status', $event)"
      @delete="$emit('delete', $event)"
      @copy="$emit('copy', $event)"
      @send_to_review="show_send_to_review_overlay = true"
    >
      <template #heading>
        {{ investor.name }} <small>#{{ investor.id }}</small>
      </template>
      <template #overlays>
        <Overlay
          v-if="show_send_to_review_overlay"
          :title="$t('Submit for review')"
          :comment-input="true"
          @cancel="show_send_to_review_overlay = false"
          @submit="send_to_review"
        >
          <div class="mt-2" style="font-weight: bold">
            <label>
              <input required type="checkbox" />
              {{ $t("I've read and agree to the") }}
              <a href="/about/data-policy/" target="_blank">{{ $t("Data policy") }} </a
              >.
            </label>
          </div>
        </Overlay>
      </template>
    </ManageHeader>
  </div>
</template>

<script>
  import ManageHeader from "$components/Management/ManageHeader";
  import Overlay from "$components/Overlay";
  import gql from "graphql-tag";

  export default {
    name: "InvestorManageHeader",
    components: {
      Overlay,
      ManageHeader,
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
            this.$emit("reload");
          })
          .catch((error) => console.error(error));
      },
    },
  };
</script>
