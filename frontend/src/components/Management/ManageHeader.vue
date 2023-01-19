<template>
  <div class="generic-manage-header-container">
    <div class="manage-header">
      <div class="manage-header-left-side">
        <div class="version-nav-buttons">
          <router-link
            v-if="is_draft_with_active"
            :to="object_detail_path(object.id)"
            class="btn btn-gray"
          >
            {{ $t("Go to active version") }}
          </router-link>
          <router-link
            v-if="has_newer_draft"
            :to="object_detail_path(object.id, last_version.id)"
            class="btn btn-gray"
          >
            {{ $t("Go to current draft") }}
          </router-link>
        </div>

        <div class="title-and-date-bar">
          <div>
            <h1>
              <slot name="heading"></slot>
            </h1>
          </div>
          <div>
            <HeaderDates :is-version="!!objectVersion" :obj="object" />
          </div>
        </div>

        <div v-if="object.status === 4" class="status-and-progress-buttons">
          <div class="fat-stati">
            <div class="deleted">
              {{ $t("Deleted") }}
            </div>
          </div>
        </div>
        <div
          v-else-if="object.status !== 1 && !objectVersion"
          class="status-and-progress-buttons"
        >
          <div class="fat-stati">
            <div class="active">{{ $t("Activated") }}</div>
          </div>
        </div>
        <div v-else class="status-and-progress-buttons">
          <div class="fat-stati">
            <div
              :class="{
                active: object.draft_status === 1 || object.draft_status === 4,
              }"
            >
              <span>{{ $t("Draft") }}</span>
              <span
                v-if="object.draft_status === 4"
                class="pl-2 font-bold text-red-600"
              >
                ({{ $t("Rejected") }})
              </span>
            </div>
            <div :class="{ active: object.draft_status === 2 }">
              <span>{{ $t("Submitted for review") }}</span>
            </div>
            <div :class="{ active: object.draft_status === 3 }">
              <span>{{ $t("Submitted for activation") }}</span>
            </div>
            <div :class="{ active: object.draft_status === null }">
              <span>{{ $t("Activated") }}</span>
            </div>
          </div>

          <div class="row workflow-buttons">
            <div class="col text-right">
              <a
                v-if="object.draft_status === 1 && is_authorized(object)"
                :class="{ disabled: last_version.id !== +objectVersion }"
                :title="submit_for_review_link_title"
                class="btn btn-pelorous"
                @click="$emit('send_to_review')"
              >
                {{ $t("Submit for review") }}
              </a>
              <a
                v-if="
                  (object.draft_status === 2 || object.draft_status === 3) &&
                  is_authorized(object)
                "
                :class="{ disabled: last_version.id !== +objectVersion }"
                :title="request_improvement_link_title"
                class="btn btn-primary"
                @click="show_to_draft_overlay = true"
              >
                {{ $t("Request improvement") }}
              </a>
            </div>
            <div class="col text-center">
              <a
                v-if="object.draft_status === 2 && is_authorized(object)"
                :class="{ disabled: last_version.id !== +objectVersion }"
                :title="submit_for_activation_link_title"
                class="btn btn-pelorous"
                @click="show_send_to_activation_overlay = true"
              >
                {{ $t("Submit for activation") }}
              </a>
            </div>
            <div class="col text-left">
              <a
                v-if="object.draft_status === 3 && is_authorized(object)"
                :class="{ disabled: last_version.id !== +objectVersion }"
                :title="get_activate_description"
                class="btn btn-pelorous"
                @click="show_activate_overlay = true"
              >
                {{ $t("Activate") }}
              </a>
            </div>
          </div>
        </div>

        <div class="bottom-row">
          <div class="left-side">
            <div v-if="last_version" class="last-changes">
              Last changes
              <span v-if="last_version.created_by">
                by {{ last_version.created_by.full_name }}
              </span>
              on
              {{ last_version.created_at | dayjs("YYYY-MM-DD HH:mm") }}
              <br />
              <router-link
                v-if="object.versions.length > 1"
                :to="
                  object_compare_path(
                    object.id,
                    object.versions[1].id,
                    object.versions[0].id
                  )
                "
              >
                Show latest changes
              </router-link>
            </div>
            <div class="action-buttons">
              <div v-if="is_editable" class="action-button">
                <div class="d-inline-block">
                  <router-link
                    v-if="
                      !objectVersion ||
                      (object.modified_by &&
                        $store.state.user.id === object.modified_by.id)
                    "
                    :class="{ disabled: is_old_draft }"
                    :to="object_edit_path(object.id, objectVersion)"
                    class="btn btn-primary"
                    >{{ $t("Edit") }}
                  </router-link>
                  <button
                    v-else
                    class="btn btn-primary"
                    @click.prevent="show_new_draft_overlay = true"
                  >
                    {{ $t("Edit") }}
                  </button>
                </div>
                <div class="d-inline-block button-description">
                  {{ get_edit_description }}
                </div>
              </div>
              <div v-if="is_deletable" class="action-button">
                <div class="d-inline-block">
                  <button
                    class="btn btn-danger"
                    @click.prevent="show_to_delete_overlay = true"
                  >
                    {{ get_delete_text }}
                  </button>
                </div>
                <div class="d-inline-block button-description">
                  {{ get_delete_description }}
                </div>
              </div>
              <div
                v-if="$store.state.user.role === 3 && otype === 'deal'"
                class="action-button"
              >
                <div class="d-inline-block">
                  <button class="btn btn-gray btn-sm" @click.prevent="$emit('copy')">
                    {{ $t("Copy deal") }}
                  </button>
                </div>
                <div class="d-inline-block button-description">
                  {{
                    otype === "deal" ? $t("Copy this deal") : $t("Copy this investor")
                  }}
                </div>
              </div>
            </div>
          </div>
          <slot name="visibility" />
        </div>
      </div>
      <ManageHeaderComments
        :object="object"
        :object-version="objectVersion"
        :users="users"
        @add_comment="$emit('add_comment', $event)"
      />
    </div>
    <slot name="overlays"></slot>
    <Overlay
      v-if="show_new_draft_overlay"
      :comment-input="false"
      :title="$t('Create a new draft').toString()"
      @cancel="show_new_draft_overlay = false"
      @submit="() => $router.push(object_edit_path(object.id, objectVersion))"
    >
      {{
        $t(
          "You are not the author of this version. Therefore, a new version will be created if you proceed."
        )
      }}
    </Overlay>
    <Overlay
      v-if="show_to_draft_overlay"
      :assign-to-user-input="true"
      :comment-input="true"
      :comment-required="true"
      :title="$t('Request improvement')"
      :to-user="transition_to_user"
      @cancel="show_to_draft_overlay = false"
      @submit="do_to_draft($event)"
    />
    <Overlay
      v-if="show_to_delete_overlay"
      :comment-input="true"
      :comment-required="true"
      :title="get_submit_to_delete_title"
      @cancel="show_to_delete_overlay = false"
      @submit="do_delete($event)"
    />
    <Overlay
      v-if="show_send_to_activation_overlay"
      :comment-input="true"
      @cancel="show_send_to_activation_overlay = false"
      @submit="send_to_activation"
    />
    <Overlay
      v-if="show_activate_overlay"
      :comment-input="true"
      @cancel="show_activate_overlay = false"
      @submit="activate"
    />
  </div>
</template>

<script lang="ts">
  import HeaderDates from "$components/HeaderDates.vue";
  import ManageHeaderComments from "$components/Management/ManageHeaderComments.vue";
  import Overlay from "$components/Overlay.vue";
  import type { Obj, ObjVersion } from "$types/generics";
  import type { User } from "$types/user";
  import { is_authorized } from "$utils/user";
  import gql from "graphql-tag";
  import Vue from "vue";
  import type { PropType } from "vue";
  import type { Location } from "vue-router/types/router";

  export default Vue.extend({
    name: "ManageHeader",
    components: {
      ManageHeaderComments,
      HeaderDates,
      Overlay,
    },
    props: {
      object: { type: Object as PropType<Obj>, required: true },
      objectVersion: { type: [Number, String], default: null },
      otype: { type: String, default: "deal" },
    },
    data() {
      return {
        users: [],
        show_to_draft_overlay: false,
        show_to_delete_overlay: false,
        show_send_to_activation_overlay: false,
        show_activate_overlay: false,
        show_new_draft_overlay: false,
        is_authorized,
        submit_for_review_link_title:
          this.otype === "deal"
            ? this.$t("Submits the deal for review")
            : this.$t("Submits the investor for review"),
        request_improvement_link_title:
          this.otype === "deal"
            ? this.$t(
                "Send a request of improvent and create a new draft version of the deal"
              )
            : this.$t(
                "Send a request of improvent and create a new draft version of the investor"
              ),
        submit_for_activation_link_title:
          this.otype === "deal"
            ? this.$t("Submits the deal for activation")
            : this.$t("Submits the investor for activation"),
      };
    },
    apollo: {
      users: gql`
        {
          users {
            id
            full_name
            username
          }
        }
      `,
    },
    computed: {
      last_version(): ObjVersion {
        return this.object?.versions[0] ?? {};
      },
      is_active_with_draft(): boolean {
        return !this.objectVersion && !!this.object.draft_status;
      },
      is_editable(): boolean {
        // object ist deleted
        if (!this.objectVersion && this.object.status === 4) return false;
        if (this.is_active_with_draft) return false;
        if (this.object.draft_status === 4) return this.$store.state.user.role === 3;
        return is_authorized(this.object);
      },
      is_deletable(): boolean {
        if (this.is_active_with_draft) return false;
        if (this.is_old_draft) return false;

        if (
          this.object.draft_status === null ||
          this.object.draft_status === 4 // 4 = rejected
        )
          return this.$store.state.user.role === 3;
        return is_authorized(this.object);
      },
      is_deleted(): boolean {
        // active and deleted
        return !this.objectVersion && this.object.status === 4;
      },
      is_draft_with_active(): boolean {
        // current draft with active object
        if (this.objectVersion && [2, 3].includes(this.object.status)) return true;
        // old draft with activated object
        return this.is_old_draft && [2, 3].includes(this.latest_object_version.status);
      },
      is_old_draft(): boolean {
        return !!this.objectVersion && this.last_version.id !== +this.objectVersion;
      },
      has_newer_draft(): boolean {
        if (this.is_active_with_draft) return true;
        // old with newer draft
        return this.is_old_draft && !!this.latest_object_version.draft_status;
      },
      has_active(): boolean {
        return !!this.object.status;
      },
      latest_object_version(): Obj {
        return this.object.versions.find(
          (v: ObjVersion) => v.id === this.last_version.id
        )[this.otype];
      },
      get_edit_description(): string {
        if (this.object.draft_status === 1) {
          if (!this.has_active) {
            // only for new drafts without active
            return this.otype === "deal"
              ? this.$t("Starts editing this deal").toString()
              : this.$t("Starts editing this investor").toString();
          } else {
            // only for new drafts with active
            return this.otype === "deal"
              ? this.$t("Edits this draft version").toString()
              : this.$t("Edits this investor version").toString();
          }
        } else
          return this.otype === "deal"
            ? this.$t("Creates a new draft version of this deal").toString()
            : this.$t("Creates a new draft version of this investor").toString();
      },
      get_delete_text(): string {
        if (this.is_deleted) return this.$t("Undelete").toString();
        else if (!this.objectVersion && !this.object.draft_status) {
          // active without draft
          return this.otype === "deal"
            ? this.$t("Delete deal").toString()
            : this.$t("Delete investor").toString();
        } else return this.$t("Delete").toString();
      },
      get_delete_description(): string {
        if (this.is_deleted)
          return this.otype === "deal"
            ? this.$t("Reactivate this deal").toString()
            : this.$t("Reactivate this investor").toString();
        if (this.objectVersion && this.has_active) {
          // is draft and has active
          return this.otype === "deal"
            ? this.$t("Deletes this draft version of the deal").toString()
            : this.$t("Deletes this draft version of the investor").toString();
        } else
          return this.otype === "deal"
            ? this.$t("Deletes this deal").toString()
            : this.$t("Deletes this investor").toString();
      },
      get_submit_to_delete_title(): string {
        if (this.objectVersion)
          return this.otype === "deal"
            ? this.$t("Delete deal version").toString()
            : this.$t("Delete investor version").toString();

        if (this.object.status === 4)
          return this.otype === "deal"
            ? this.$t("Reactivate deal").toString()
            : this.$t("Reactivate investor").toString();

        return this.otype === "deal"
          ? this.$t("Delete deal").toString()
          : this.$t("Delete investor").toString();
      },
      get_activate_description(): string {
        return this.has_active
          ? this.$t(
              "Activates submitted version replacing currently active version"
            ).toString()
          : this.otype === "deal"
          ? this.$t("Sets the deal active").toString()
          : this.$t("Sets the investor active").toString();
      },
      transition_to_user(): User {
        let latest_draft_creation = this.object.workflowinfos.find((v) => {
          return !v.draft_status_before && v.draft_status_after === 1;
        });
        if (!latest_draft_creation)
          latest_draft_creation = this.object.workflowinfos.find((v) => {
            return !v.draft_status_before && v.draft_status_after === 2;
          });
        return latest_draft_creation.from_user;
      },
    },
    methods: {
      object_detail_path(obID: number, obV?: number): Location {
        if (this.otype === "deal") {
          return {
            name: "deal_detail",
            params: obV
              ? {
                  dealId: obID.toString(),
                  dealVersion: obV.toString(),
                }
              : { dealId: obID.toString() },
          };
        }
        return {
          name: "investor_detail",
          params: obV
            ? { investorId: obID.toString(), investorVersion: obV?.toString() }
            : { investorId: obID.toString() },
        };
      },
      object_edit_path(obID: number, obV: number | string): Location {
        return this.otype === "deal"
          ? {
              name: "deal_edit",
              params: { dealId: obID.toString(), dealVersion: obV?.toString() },
            }
          : {
              name: "investor_edit",
              params: { investorId: obID.toString(), investorVersion: obV?.toString() },
            };
      },
      object_compare_path(
        oID: number,
        fromVersion: number,
        toVersion: number
      ): Location {
        return this.otype === "deal"
          ? {
              name: "deal_compare",
              params: {
                dealId: oID.toString(),
                fromVersion: fromVersion.toString(),
                toVersion: toVersion.toString(),
              },
            }
          : {
              name: "investor_compare",
              params: {
                investorId: oID.toString(),
                fromVersion: fromVersion.toString(),
                toVersion: toVersion.toString(),
              },
            };
      },
      do_delete({ comment }): void {
        this.$emit("delete", comment);
        this.show_to_delete_overlay = false;
      },
      do_to_draft({ comment, to_user }): void {
        console.log("to_draft", { comment, to_user });
        this.$emit("change_status", { transition: "TO_DRAFT", comment, to_user });
        this.show_to_draft_overlay = false;
      },
      send_to_activation({ comment }) {
        this.$emit("change_status", { comment, transition: "TO_ACTIVATION" });
        this.show_send_to_activation_overlay = false;
      },
      activate({ comment }) {
        this.$emit("change_status", { comment, transition: "ACTIVATE" });
        this.show_activate_overlay = false;
      },
    },
  });
</script>

<style lang="scss" scoped>
  @import "node_modules/bootstrap/scss/functions";
  @import "node_modules/bootstrap/scss/variables";
  @import "node_modules/bootstrap/scss/mixins/_breakpoints";

  $arrow-height: 34px;
  $max-z-index: 10;

  .btn {
    border-radius: 0;
    color: white;
  }

  .generic-manage-header-container {
    margin-top: 1.5rem;
    margin-bottom: 1.5rem;
  }

  .manage-header {
    padding: 0;
    display: flex;
    flex-flow: column;

    @media screen and (min-width: 992px) {
      flex-flow: row;
    }
  }

  .manage-header-left-side {
    background: #e5e5e5;
    flex-grow: 2;
  }

  .version-nav-buttons {
    display: flex;
    justify-content: center;
    gap: 1em;
    margin-top: -1.1875em;
    z-index: 1;
  }

  .title-and-date-bar {
    margin-top: 1rem;
    padding: 1rem;
    display: flex;
    flex-flow: row;
    justify-content: space-between;
    width: 100%;
    gap: 1rem;

    h1 {
      font-size: 1.85rem;
      font-weight: normal !important;
      color: black;
      text-align: left;
      text-transform: none;
      margin-bottom: 0;

      &:before {
        content: none;
      }
    }
  }

  .status-and-progress-buttons {
    display: flex;
    flex-flow: column;
    margin-bottom: 2rem;

    > div {
      width: 100%;
    }

    .fat-stati {
      display: flex;
      flex-flow: row wrap;
      margin-top: 1rem;

      @media (max-width: 400px) {
        font-size: 0.9rem;
        line-height: 1.1;
      }

      > div {
        position: relative;
        margin: 0.5rem 0.3rem;
        padding: 0.5rem 0 0.5rem 1.3rem;
        background: #dbdbdb;
        flex-grow: 1;
        text-align: center;
        height: $arrow-height * 2;
        display: flex;
        align-items: center;
        justify-content: center;
        opacity: 0.7;

        &.active {
          background: #93c7c8;
          color: white;

          &:after {
            border-left-color: #93c7c8;
          }
        }

        &.deleted {
          background: hsl(0, 33%, 68%);
          color: white;
        }

        @for $i from 0 to $max-z-index {
          &:nth-child(#{$i + 1}) {
            z-index: ($max-z-index - $i);
          }
        }

        &:before {
          // arrow from the left
          content: "";
          border-left: $arrow-height/2 solid #e5e5e5;
          border-top: $arrow-height solid transparent;
          border-bottom: $arrow-height solid transparent;
          height: 0;
          width: 0;
          position: absolute;
          left: 0;
          top: 0;
          bottom: 0;
        }

        &:after {
          // arrow to the right
          content: "";
          border-left: $arrow-height/2 solid #dbdbdb;
          border-top: $arrow-height solid transparent;
          border-bottom: $arrow-height solid transparent;
          height: 0;
          width: 0;
          position: absolute;
          right: -($arrow-height - 1)/2;
          top: 0;
          bottom: 0;
        }

        &:first-child {
          margin-left: 0;
          padding-left: 0.2rem;

          &:before {
            display: none;
          }
        }

        &:last-child {
          margin-right: 0;

          &:after {
            display: none;
          }
        }
      }
    }
  }

  .bottom-row {
    padding: 1rem;
    display: flex;
    width: 100%;
    flex-flow: row;
    gap: 1rem;

    > div {
      flex-basis: 0;
      //width: 100%;
    }

    .left-side {
      flex-grow: 2;
    }

    .last-changes {
      font-size: 0.9rem;
      margin-bottom: 1em;
    }

    .action-button {
      margin-bottom: 0.5em;

      &:not(:last-child) {
        margin-bottom: 7px;
      }

      align-items: center;

      .btn {
        min-width: 4.5em;

        &.btn-danger {
          border: 1px dotted red;
          color: red;
          background: transparent;

          &:hover {
            border-color: red;
            color: white;
            background: lighten(red, 20);
          }
        }
      }

      .button-description {
        margin-left: 1rem;
        color: rgba(0, 0, 0, 0.5);
        font-style: italic;
      }
    }
  }
</style>
