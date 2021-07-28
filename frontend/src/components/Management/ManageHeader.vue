<template>
  <div>
    <div class="jumbotron jumbotron-fluid manage-interface">
      <div class="col-md-8 main-info">
        <div class="full-width-wrapper">
          <div class="container">
            <div class="row">
              <div class="col-md-8 content-area">
                <!-- only use left half, rest for comments -->
                <div class="container">
                  <div class="row">
                    <div class="col-sm-5 title-col">
                      <div class="version-nav-buttons">
                        <router-link
                          v-if="is_draft_with_active"
                          class="btn btn-gray"
                          :to="object_detail_path(object.id)"
                        >
                          {{ $t("Go to active version") }}
                        </router-link>
                        <router-link
                          v-if="has_newer_draft"
                          class="btn btn-gray"
                          :to="object_detail_path(object.id, last_revision.id)"
                        >
                          {{ $t("Go to current draft") }}
                        </router-link>
                      </div>
                      <h1><slot name="heading"></slot></h1>
                    </div>
                    <div class="col-sm-7 panel-container">
                      <HeaderDates :obj="object" />
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div v-if="object.status !== 1 && !objectVersion" class="status-wrapper">
            <div class="col-md-8">
              <div class="row fat-stati">
                <div v-if="object.status === 4" class="col deleted">
                  {{ $t("Deleted") }}
                </div>
                <div v-else class="col active">{{ $t("Activated") }}</div>
              </div>
            </div>
          </div>
          <div v-else class="status-wrapper">
            <div class="col-md-8">
              <div class="row fat-stati">
                <div class="col" :class="{ active: object.draft_status === 1 }">
                  <span>{{ $t("Draft") }}</span>
                </div>
                <div class="col" :class="{ active: object.draft_status === 2 }">
                  <span>{{ $t("Submitted for review") }}</span>
                </div>
                <div class="col" :class="{ active: object.draft_status === 3 }">
                  <span>{{ $t("Submitted for activation") }}</span>
                </div>
                <div class="col" :class="{ active: object.draft_status === null }">
                  <span>{{ $t("Activated") }}</span>
                </div>
              </div>
              <div class="row workflow-buttons">
                <div class="col text-right">
                  <a
                    v-if="object.draft_status === 1 && is_authorized(object)"
                    class="btn btn-secondary"
                    :class="{ disabled: last_revision.id !== +objectVersion }"
                    :title="submit_for_review_link_title"
                    @click="$emit('send_to_review')"
                  >
                    {{ $t("Submit for review") }}
                  </a>
                  <a
                    v-if="
                      (object.draft_status === 2 || object.draft_status === 3) &&
                      is_authorized(object)
                    "
                    class="btn btn-primary"
                    :class="{ disabled: last_revision.id !== +objectVersion }"
                    :title="request_improvement_link_title"
                    @click="show_to_draft_overlay = true"
                  >
                    {{ $t("Request improvement") }}
                  </a>
                </div>
                <div class="col text-center">
                  <a
                    v-if="object.draft_status === 2 && is_authorized(object)"
                    class="btn btn-secondary"
                    :class="{ disabled: last_revision.id !== +objectVersion }"
                    :title="submit_for_activation_link_title"
                    @click="$emit('change_status', { transition: 'TO_ACTIVATION' })"
                  >
                    {{ $t("Submit for activation") }}
                  </a>
                </div>
                <div class="col text-left">
                  <a
                    v-if="object.draft_status === 3 && is_authorized(object)"
                    class="btn btn-secondary"
                    :class="{ disabled: last_revision.id !== +objectVersion }"
                    :title="get_activate_description"
                    @click="$emit('change_status', { transition: 'ACTIVATE' })"
                  >
                    {{ $t("Activate") }}
                  </a>
                </div>
              </div>
            </div>
          </div>
          <div class="container">
            <div class="row">
              <div class="col-md-8 content-area">
                <div class="row d-flex align-items-center">
                  <div class="col-sm-8 col-md-7 col-lg-8">
                    <div v-if="last_revision" class="last-changes">
                      Last changes
                      <span v-if="last_revision.user">
                        by {{ last_revision.user.full_name }}
                      </span>
                      on
                      {{ last_revision.date_created | dayjs("dddd YYYY-MM-DD HH:mm") }}
                      <br />
                      <router-link
                        v-if="object.versions.length > 1"
                        :to="
                          object_compare_path(
                            object.id,
                            object.versions[1].revision.id,
                            object.versions[0].revision.id
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
                            class="btn btn-primary"
                            :class="{ disabled: is_old_draft }"
                            :to="object_edit_path(object.id, objectVersion)"
                            >{{ $t("Edit") }}
                          </router-link>
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
                    </div>
                  </div>
                  <slot name="visibility" />
                </div>
              </div>
            </div>
          </div>
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
      v-if="show_to_draft_overlay"
      :title="$t('Request improvement')"
      :comment-input="true"
      :comment-required="true"
      :assign-to-user-input="true"
      :to-user="transition_to_user"
      @cancel="show_to_draft_overlay = false"
      @submit="do_to_draft($event)"
    />
    <Overlay
      v-if="show_to_delete_overlay"
      :title="submit_to_delete_title"
      :comment-input="true"
      :comment-required="true"
      @cancel="show_to_delete_overlay = false"
      @submit="do_delete($event)"
    />
  </div>
</template>

<script>
  import HeaderDates from "$components/HeaderDates";
  import ManageHeaderComments from "$components/Management/ManageHeaderComments";
  import ManageHeaderMixin from "$components/Management/ManageHeaderMixin";
  import Overlay from "$components/Overlay";

  export default {
    name: "GenericManageHeader",
    components: {
      ManageHeaderComments,
      HeaderDates,
      Overlay,
    },
    mixins: [ManageHeaderMixin],
  };
</script>

<style scoped lang="scss">
  @import "node_modules/bootstrap/scss/functions";
  @import "node_modules/bootstrap/scss/variables";
  @import "node_modules/bootstrap/scss/mixins/_breakpoints";

  .manage-interface {
    margin-top: -10px;
    padding: 0;
    display: flex;
    flex-wrap: wrap;
    align-items: stretch;
    background-color: transparent;
    margin-bottom: 0;
    height: 482px;

    @include media-breakpoint-down(sm) {
      height: auto;
    }

    .main-info {
      background: #e5e5e5;
      margin: 1em 0;
      position: relative;
      padding-right: 0;
      height: 450px;

      @include media-breakpoint-down(sm) {
        margin-bottom: 0;
      }

      .full-width-wrapper {
        position: absolute;
        top: 0;
        left: 0;
        width: calc(100vw - 15px); // arghh, compensate for scrollbar

        > .container > .row {
          margin-right: -30px;
        }

        .content-area {
          padding-right: 0;

          .container {
            padding: 0;
          }
        }

        .panel-container {
          padding-right: 0;
          margin-top: 1.5em;
          text-align: right;

          .meta-panel {
            background: rgba(white, 0.2);
          }
        }
      }

      .status-wrapper {
        display: flex;
        min-height: 120px;
      }

      $arrow-height: 33px;
      $max-z-index: 10;

      .fat-stati {
        display: flex;
        flex-flow: row wrap;
        margin-top: 0;
        @media (max-width: 400px) {
          font-size: 0.9rem;
          line-height: 1.1;
        }

        & > .col {
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
            // arrow to the right
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

      .last-changes {
        font-size: 0.9rem;
      }
    }

    .action-button {
      &:not(:last-child) {
        margin-bottom: 7px;
      }

      align-items: center;

      .btn {
        width: 100%;
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

  .btn {
    border-radius: 0;
    color: white;

    &.btn-secondary {
      background: var(--color-lm-investor-light);
      border-color: var(--color-lm-investor);

      &:hover,
      &:active {
        background: var(--color-lm-investor);
        color: white;
      }
    }
  }

  h1 {
    font-size: 30px;
    font-weight: normal !important;
    color: black;
    text-align: left;
    text-transform: none;
    margin-top: 0.5em;
    margin-bottom: 0;

    &:before {
      content: none;
    }
  }

  .title-col {
    position: relative;
    .version-nav-buttons {
      position: absolute;
      left: 90%;
      top: -21px;
      z-index: 1;
      width: auto;
      white-space: nowrap;
      .btn {
        &:not(:last-child) {
          margin-right: 0.5em;
        }
      }
    }
  }
</style>

<style lang="scss">
  .btn-gray {
    background-color: #b1b1b1 !important;

    &:hover {
      color: white;
      background-color: darken(#b1b1b1, 5%) !important;
    }
  }
</style>
