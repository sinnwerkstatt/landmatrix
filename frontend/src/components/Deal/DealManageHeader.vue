<template>
  <ManageHeader
    :object="deal"
    :object-version="dealVersion"
    @add_comment="add_comment"
    @change_status="$emit('change_status', $event)"
    @delete="$emit('delete', $event)"
    @copy="$emit('copy', $event)"
    @send_to_review="show_send_to_review_overlay = true"
  >
    <template #heading>
      Deal #{{ deal.id }}
      <span v-if="deal.country" class="headercountry">{{ deal.country.name }}</span>
    </template>

    <template #visibility>
      <div class="visibility-container">
        <div v-if="deal.is_public" class="visibility">
          <i class="fas fa-eye fa-fw fa-lg orange"></i>
          <span>{{ $t("Publicly visible") }}</span>
        </div>
        <div v-else class="visibility">
          <i class="fas fa-eye-slash fa-fw fa-lg orange"></i>
          <span>{{ $t("Not publicly visible") }}</span>
        </div>
        <div v-if="is_editable" class="confidential-toggle">
          <b-form-checkbox
            :checked="deal.confidential"
            :class="{ active: deal.confidential }"
            class="confidential-switch"
            name="check-button"
            switch
            :title="$t('Toggle deal confidentiality')"
            @click.native.prevent="toggle_confidential({ force: false })"
          >
            {{ deal.confidential ? $t("Confidential") : $t("Not confidential") }}
          </b-form-checkbox>
          <a id="confidential-reason">
            <span v-if="deal.confidential">({{ $t("reason") }})</span>
          </a>
          <b-tooltip target="confidential-reason" triggers="click">
            <!-- <strong>{{ get_confidential_reason }}</strong> <br /> -->
            {{ deal.confidential_comment }}
          </b-tooltip>
        </div>
        <ul>
          <template v-if="!is_editable">
            <li v-if="!deal.confidential">
              <i class="fas fa-check fa-fw"></i>
              {{ $t("Not confidential") }}
            </li>
            <li v-else>
              <i class="fas fa-times fa-fw"></i>
              {{ $t("Confidential") }}
            </li>
          </template>
          <li v-if="deal.country">
            <i class="fas fa-check fa-fw"></i>
            {{ $t("Target country is set") }}
          </li>
          <li v-else>
            <i class="fas fa-times fa-fw"></i>
            {{ $t("Target country is NOT set") }}
          </li>

          <li v-if="deal.datasources.length > 0" class="whitespace-nowrap">
            <i class="fas fa-check fa-fw"></i>
            {{ $t("At least one data source") }} ({{ deal.datasources.length }})
          </li>
          <li v-else><i class="fas fa-times fa-fw"></i> {{ $t("No data source") }}</li>

          <li v-if="deal.has_known_investor">
            <i class="fas fa-check fa-fw"></i>
            {{ $t("At least one investor") }}
          </li>
          <li v-else>
            <i class="fas fa-times fa-fw"></i> {{ $t("No known investor") }}
          </li>
        </ul>

        <div v-if="deal.fully_updated" class="visibility">
          <i class="fas fa-check-circle fa-fw fa-lg orange"></i>
          <span>{{ $t("Fully updated") }}</span>
        </div>
        <div v-else class="visibility" style="color: gray !important">
          <i class="fas fa-minus fa-fw fa-lg"></i>
          <span>{{ $t("Not fully updated") }}</span>
        </div>
      </div>
    </template>
    <template #overlays>
      <Overlay
        v-if="show_send_to_review_overlay"
        :title="$t('Submit for review').toString()"
        :comment-input="true"
        @cancel="show_send_to_review_overlay = false"
        @submit="send_to_review"
      >
        <p class="mb-1">
          If you have checked the information entered for every single variable, please
          tick the box beside "I fully updated this deal" - even if no additional
          information was found, but a complete search through the deal was conducted.
        </p>
        <label>
          <input v-model="deal.fully_updated" type="checkbox" />
          {{ $t("I fully updated this deal.") }}
        </label>
        <div class="my-4" style="font-weight: bold">
          <label>
            <input required type="checkbox" />
            {{ $t("I've read and agree to the") }}
            <a href="/about/data-policy/" target="_blank">{{ $t("Data policy") }}</a
            >.
          </label>
        </div>
      </Overlay>
      <Overlay
        v-if="show_confidential_overlay"
        :title="
          $t(deal.confidential ? 'Unset confidential' : 'Set confidential').toString()
        "
        :comment-input="!deal.confidential"
        :comment-required="!deal.confidential"
        @cancel="show_confidential_overlay = false"
        @submit="toggle_confidential"
      >
        <p v-if="deal.confidential">
          {{
            $t(
              "If you unset the confidential flag, this deal will be publicly visible once it is set active. If you want to keep it confidential, click on 'Cancel'."
            )
          }}
        </p>
        <p v-else>
          {{
            $t(
              "If you set the confidential flag, this deal will not be publicly visible anymore. If you want to keep it public, click on 'Cancel'."
            )
          }}
        </p>
      </Overlay>
    </template>
  </ManageHeader>
</template>

<script lang="ts">
  import Overlay from "$components/Overlay.vue";
  import gql from "graphql-tag";
  import { is_authorized } from "$utils/user";
  import ManageHeader from "../Management/ManageHeader.vue";
  import Vue from "vue";
  import type { PropType } from "vue";
  import type { Deal } from "$types/deal";
  import type { User } from "$types/user";

  export default Vue.extend({
    name: "DealManageHeader",
    components: {
      ManageHeader,
      Overlay,
    },
    props: {
      deal: { type: Object as PropType<Deal>, required: true },
      dealVersion: { type: [Number, String], default: null },
    },
    data() {
      return {
        show_confidential_overlay: false,
        show_send_to_review_overlay: false,
        is_authorized,
      };
    },
    computed: {
      is_active_with_draft(): boolean {
        return !this.dealVersion && !!this.deal.draft_status;
      },
      is_editable(): boolean {
        // deal ist deleted
        if (!this.dealVersion && this.deal.status === 4) return false;
        if (this.is_active_with_draft) return false;
        return this.is_authorized(this.deal);
      },
    },
    methods: {
      send_to_review(args) {
        this.$emit("change_status", { ...args, transition: "TO_REVIEW" });
        this.show_send_to_review_overlay = false;
      },
      add_comment({ comment, send_to_user }: { comment: string; send_to_user: User }) {
        this.$apollo
          .mutate({
            mutation: gql`
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
            variables: {
              id: +this.deal.id,
              version: this.dealVersion ? +this.dealVersion : null,
              comment: comment,
              to_user_id: send_to_user ? +send_to_user.id : null,
            },
          })
          .then(() => {
            this.$emit("reload");
          })
          .catch((error) => console.error(error));
      },
      toggle_confidential(data: { [key: string]: string | boolean }) {
        if (!this.is_editable) return;
        if (data.force) {
          if (this.deal.confidential) {
            this.$emit("set_confidential", { confidential: false });
            this.show_confidential_overlay = false;
          } else {
            this.$emit("set_confidential", {
              confidential: true,
              comment: data.comment,
            });
            this.show_confidential_overlay = false;
          }
        } else {
          this.show_confidential_overlay = true;
        }
      },
    },
  });
</script>

<style scoped lang="scss">
  .headercountry {
    white-space: nowrap;
    display: block;
    font-size: 1rem;
  }
  .visibility-container {
    flex-grow: 1;
    width: 100%;
    .visibility {
      font-size: 0.9em;

      i {
        font-size: 1.8em;
      }

      span {
        font-size: 1.1em;
        font-weight: bold;
        padding-left: 0.5em;
      }
    }

    ul {
      font-size: 0.8em;
      list-style: none;
      padding: 0;

      li {
        margin-left: 0.8em;

        i {
          font-size: 0.8em;
          margin-right: 11px;
        }
      }

      .fa-check {
        color: black;
      }
    }
  }
</style>

<style lang="scss">
  .confidential-toggle {
    margin-left: 0.45em;
    margin-bottom: -3px;
    display: flex;
    align-items: center;

    .confidential-switch {
      padding-left: 2rem;
      font-size: 0.8em;
      display: flex;
      align-items: center;
      label {
        font-weight: normal;
        line-height: 1.9em;

        &:hover {
          cursor: pointer;
        }
      }
    }

    a#confidential-reason {
      font-size: 0.8em;
      padding-left: 0.3em;
      text-decoration: underline;

      &:hover {
        cursor: pointer;
      }
    }
  }
</style>
