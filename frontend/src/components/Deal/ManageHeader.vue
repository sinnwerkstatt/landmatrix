<template>
  <div>
    <div class="jumbotron jumbotron-fluid manage-interface">
      <div class="col-sm-12 col-md-8 main-info">
        <div class="full-width-wrapper">
          <div class="container">
            <div class="row">
              <div class="col-sm-12 col-md-8 content-area">
                <!-- only use left half, rest for comments -->
                <div class="container">
                  <div class="row">
                    <div class="col-sm-4">
                      <h1>
                        Deal #{{ deal.id }}
                        <span class="headercountry">{{ deal.country.name }}</span>
                      </h1>
                    </div>
                    <div class="col-sm-8 panel-container">
                      <HeaderDates :obj="deal" />
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="status-wrapper">
            <div class="col-sm-12 col-md-8">
              <div class="row fat-stati">
                <div class="col" :class="{ active: deal.draft_status === 1 }">
                  <span>{{ $t("Draft") }}</span>
                </div>
                <div class="col" :class="{ active: deal.draft_status === 2 }">
                  <span>{{ $t("Submitted for review") }}</span>
                </div>
                <div class="col" :class="{ active: deal.draft_status === 3 }">
                  <span>{{ $t("Submitted for activation") }}</span>
                </div>
                <div class="col" :class="{ active: deal.draft_status === null }">
                  <span>{{ $t("Activated") }}</span>
                </div>
              </div>
              <div class="row workflow-buttons">
                <div class="col text-right">
                  <a
                    v-if="deal.draft_status === 1"
                    class="btn btn-secondary"
                    @click="$emit('change_deal_status', 'TO_REVIEW')"
                  >
                    {{ $t("Submit for review") }}
                  </a>
                  <a
                    v-if="deal.draft_status === 2 || deal.draft_status === 3"
                    class="btn btn-primary"
                    @click="$emit('change_deal_status', 'TO_DRAFT')"
                  >
                    {{ $t("Request improvement") }}
                  </a>
                </div>
                <div class="col text-center">
                  <a
                    v-if="deal.draft_status === 2"
                    class="btn btn-secondary"
                    @click="$emit('change_deal_status', 'TO_ACTIVATION')"
                  >
                    {{ $t("Submit for activation") }}
                  </a>
                </div>
                <div class="col text-left">
                  <a
                    v-if="deal.draft_status === 3"
                    class="btn btn-secondary"
                    @click="$emit('change_deal_status', 'ACTIVATE')"
                  >
                    {{ $t("Activate") }}
                  </a>
                </div>
              </div>
            </div>
          </div>
          <div class="container">
            <div class="row">
              <div class="col-sm-12 col-md-8 content-area">
                <!-- only use left half, rest for comments -->

                <div class="row d-flex align-items-center p-3">
                  <div
                    v-if="last_revision"
                    class="col-sm-8 col-md-7 col-lg-8 last-changes"
                  >
                    Last changes by {{ last_revision.user.full_name }} on
                    {{ last_revision.date_created | dayjs("dddd YYYY-MM-DD HH:mm")
                    }}<br />
                    <router-link
                      v-if="deal.versions.length > 1"
                      :to="{
                        name: 'deal_compare',
                        params: {
                          dealId: deal.id,
                          fromVersion: deal.versions[1].revision.id,
                          toVersion: deal.versions[0].revision.id,
                        },
                      }"
                    >
                      Show latest changes
                    </router-link>
                  </div>
                  <div class="col-sm-4 col-md-5 col-lg-4 visibility-container">
                    <div v-if="deal.is_public">
                      <i class="fas fa-eye fa-fw fa-lg"></i>
                      {{ $t("Publicly visible") }}
                    </div>
                    <div v-else>
                      <i class="fas fa-eye-slash fa-fw fa-lg"></i>
                      {{ $t("Not publicly visible") }}
                    </div>
                    <ul>
                      <li v-if="!deal.confidential">
                        <i class="fas fa-check fa-fw"></i> {{ $t("Not confidential") }}
                      </li>
                      <li v-else>
                        <i class="fas fa-times fa-fw"></i>
                        <b-button
                          id="confidential"
                          style="
                            color: black;
                            background: inherit;
                            border: 0;
                            padding: 0;
                          "
                        >
                          {{ $t("Confidential") }}
                        </b-button>
                        <b-tooltip target="confidential" triggers="hover">
                          <strong>{{ get_confidential_reason(deal) }}</strong>
                          <br />
                          {{ deal.confidential_comment }}
                        </b-tooltip>
                      </li>

                      <li v-if="deal.country">
                        <i class="fas fa-check fa-fw"></i>
                        {{ $t("Target country is set") }}
                      </li>
                      <li v-else>
                        <i class="fas fa-times fa-fw"></i>
                        {{ $t("Target country is NOT set") }}
                      </li>

                      <li v-if="deal.datasources.length > 0">
                        <i class="fas fa-check fa-fw"></i>
                        {{ $t("At least one data source") }}
                      </li>
                      <li v-else>
                        <i class="fas fa-times fa-fw"></i> {{ $t("No data source") }}
                      </li>

                      <li v-if="deal.has_known_investor">
                        <i class="fas fa-check fa-fw"></i>
                        {{ $t("At least one investor") }}
                      </li>
                      <li v-else>
                        <i class="fas fa-times fa-fw"></i> {{ $t("No investor") }}
                      </li>
                    </ul>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="col-sm-12 col-md-4 comments">
        <h3>Comments</h3>
        <div class="new-comment">
          <form action="." method="post">
            <div>
              <textarea v-model="comment" rows="2" required="required"></textarea>
            </div>
            <div class="send">
              <span>{{ $t("Send to:") }}</span>
              <multiselect
                v-model="send_to_user"
                :options="users"
                :multiple="false"
                :close-on-select="true"
                :allow-empty="true"
                placeholder="Send to"
                track-by="id"
                label="full_name"
              />
              <a class="btn btn-default" @click.prevent="add_deal_comment">
                {{ $t("Send") }}
              </a>
            </div>
          </form>
        </div>
        <div class="comments-list">
          <div v-for="wfi in deal.workflowinfos" :key="wfi.timestamp" class="comment">
            <div class="meta">
              <span class="date">{{ wfi.timestamp | dayjs("YYYY-MM-DD HH:mm") }}</span>
              <span class="from-to">
                {{ $t("From") }} {{ wfi.from_user.full_name }}
                <span v-if="wfi.to_user">
                  {{ $t("to") }} {{ wfi.to_user.full_name }}
                </span>
              </span>
            </div>
            <div
              v-if="get_draft_status(wfi)"
              class="status-change"
              v-html="get_draft_status(wfi)"
            ></div>
            <!-- eslint-disable-next-line vue/no-v-html -->
            <div
              v-if="wfi.comment"
              class="message"
              v-html="linebreaks(wfi.comment)"
            ></div>
          </div>
        </div>
      </div>
    </div>
    <div class="container edit-buttons">
      <div class="links">
        <router-link
          class="btn btn-primary"
          :to="{
            name: 'deal_edit',
            params: { dealId: deal.id, dealVersion: dealVersion },
          }"
        >
          Edit
        </router-link>
        <a href="" class="btn btn-danger btn-sm">Delete</a>
      </div>
    </div>
  </div>
</template>

<script>
  import { linebreaks } from "$utils/filters";
  import gql from "graphql-tag";
  import HeaderDates from "../HeaderDates";
  import { draft_status_map, status_map } from "$utils/choices";

  export default {
    name: "ManageHeader",
    components: { HeaderDates },
    props: {
      deal: { type: Object, required: true },
      dealVersion: { type: [Number, String], default: null },
    },
    data() {
      return {
        users: [],
        comment: "",
        send_to_user: null,
        linebreaks,
      };
    },
    apollo: {
      users: gql`
        {
          users {
            id
            full_name
          }
        }
      `,
    },
    computed: {
      last_revision() {
        return this.deal?.versions[0]?.revision ?? "";
      },
    },
    methods: {
      get_draft_status(wfi) {
        let before = wfi.draft_status_before;
        let after = wfi.draft_status_after;
        if (before !== after) {
          if (!before) {
            return `<div class="status">${draft_status_map[after]}</div>`;
          } else {
            let before_status = draft_status_map[before];
            let after_status;
            if (!after) {
              after_status = status_map[2];
            } else {
              after_status = draft_status_map[after];
            }
            let ret = `<div class="status">${before_status}</div>`;
            ret += `→`;
            ret += `<div class="status">${after_status}</div>`;
            return ret;
          }
        } else {
          return null;
        }
      },
      get_confidential_reason(deal) {
        return {
          TEMPORARY_REMOVAL: this.$t("Temporary removal from PI after criticism"),
          RESEARCH_IN_PROGRESS: this.$t("Research in progress"),
          LAND_OBSERVATORY_IMPORT: this.$t("Land Observatory Import"),
        }[deal.confidential_reason];
      },
      add_deal_comment() {
        if (this.comment) {
          this.$apollo
            .mutate({
              mutation: gql`
                mutation(
                  $id: Int!
                  $version: Int
                  $comment: String!
                  $to_user_id: Int
                ) {
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
                comment: this.comment,
                to_user_id: this.send_to_user ? +this.send_to_user.id : null,
              },
            })
            .then(() => {
              this.$emit("reload_deal");
              this.comment = "";
            })
            .catch((error) => console.error(error));
        }
      },
    },
  };
</script>

<style scoped lang="scss">
  @import "../../scss/colors";
  @import "node_modules/bootstrap/scss/functions";
  @import "node_modules/bootstrap/scss/variables";
  @import "node_modules/bootstrap/scss/mixins/_breakpoints";

  i {
    color: var(--primary);
  }

  .manage-interface {
    margin-top: -10px;
    padding: 0;
    display: flex;
    flex-wrap: wrap;
    align-items: stretch;
    background-color: transparent;
    margin-bottom: 0;
    height: 432px;

    @include media-breakpoint-down(sm) {
      height: auto;
    }

    .main-info {
      background: #e5e5e5;
      margin: 1em 0;
      position: relative;
      padding-right: 0;
      height: 400px;

      @include media-breakpoint-down(sm) {
        margin-bottom: 0;
      }

      .full-width-wrapper {
        position: absolute;
        top: 0;
        left: 0;
        width: calc(100vw - 12px); // arghh, compensate for scrollbar

        .container {
          padding: 0;
        }

        > .container > .row {
          margin-right: -30px;
        }

        .content-area {
          padding-right: 0;
        }

        .panel-container {
          padding-right: 0;
          margin-top: 1em;

          .meta-panel {
            background: rgba(white, 0.2);
            color: rgba(black, 0.5);
          }
        }
      }

      .status-wrapper {
        display: flex;
      }

      $arrow-height: 33px;
      $max-z-index: 10;

      .fat-stati {
        display: flex;
        flex-flow: row wrap;
        margin-top: 1em;
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

    .comments {
      background: #c4c4c4;
      padding: 0.7rem;
      color: rgba(black, 0.6);
      max-height: 100%;
      display: flex;
      flex-direction: column;

      h3 {
        margin-top: 0;
        font-weight: 600;
        margin-bottom: 0.2em;
        font-size: 1.2em;
      }

      .new-comment {
        font-size: 0.9em;

        textarea {
          width: 100%;
          border: 1px solid lightgrey;
          border-radius: 5px;
          z-index: 1;
          position: relative;
          font-size: 0.9em;

          &:focus {
            border-color: transparent;
            outline: none;
          }
        }

        .send {
          display: flex;
          align-items: center;

          span {
            white-space: nowrap;
          }

          input {
            flex: 1;
            width: 100px;
            margin: 0 2px 0 0.5em;
            border: 1px solid lightgrey;
            border-radius: 5px;
          }

          .btn {
            background: $lm_investor;
            padding: 0.38em 0.7em;
            font-size: 0.9em;
            border-radius: 5px;

            &:hover {
              background-color: lighten($lm_investor, 5%);
            }

            &:focus,
            &:active {
              outline: none;
            }
          }
        }
      }

      .comments-list {
        margin-top: 1em;
        overflow-y: scroll;

        .comment {
          font-size: 0.8em;
          margin-bottom: 0.5em;

          .meta {
            .date {
              font-weight: 600;
            }
          }

          .status-change {
            margin-bottom: 2px;
          }

          .message {
            background: #e5e5e5;
            padding: 0.3em 0.5em;
            border-radius: 5px;
          }
        }
      }
    }
  }

  .edit-buttons {
    position: relative;

    .links {
      position: absolute;
      top: -2.3em;

      @include media-breakpoint-down(sm) {
        position: relative;
        top: 0;
        margin-top: 2em;
        margin-bottom: 1em;
      }

      .btn {
        border-radius: 0;
        color: white;

        &.btn-primary {
          padding: 0.3em 2.5em;
        }

        &.btn-danger {
          border-color: red;
          color: red;
          background: white;
          margin-left: 1.5em;
          font-size: 0.8em;

          &:hover {
            border-color: red;
            color: white;
            background: lighten(red, 20);
          }
        }
      }
    }
  }

  .visibility-container {
    div {
      margin-left: -1.6em;
      font-weight: bold;
      font-size: 0.9em;

      i {
        font-size: 1.2em;
      }
    }

    ul {
      font-size: 0.8em;
      list-style: none;
      padding: 0;

      li {
        margin-left: -1.4em;

        i {
          font-size: 0.8em;
          margin-right: 5px;
        }
      }

      .fa-check {
        color: black;
      }
    }
  }

  .btn {
    border-radius: 0;
    color: white;

    &.btn-secondary {
      background: rgba($lm_investor, 0.8);
      border-color: $lm_investor;

      &:hover,
      &:active {
        background: rgba($lm_investor, 1);
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
    margin-top: 1em;
    margin-bottom: 0;

    &:before {
      content: none;
    }
  }

  .headercountry {
    white-space: nowrap;
    display: block;
    font-size: 1rem;
  }
</style>
<style lang="scss">
  @import "../../scss/colors";

  .status-change .status {
    display: inline-block;
    padding: 2px 5px 3px;
    line-height: 1;
    background-color: darken(#e4e4e4, 8%);
    color: #5e5e64;
    border-radius: 8px;
    filter: drop-shadow(-1px 1px 1px rgba(0, 0, 0, 0.1));

    &:last-child {
      background-color: #93c7c8;
      color: white;
    }
  }

  .send {
    .multiselect,
    .multiselect__tags {
      min-height: 30px;
    }

    .multiselect {
      min-width: auto;
    }
    .multiselect__tags {
      padding-top: 4px;
      padding-left: 2px;
      padding-right: 25px;
    }

    .multiselect__select {
      height: 32px;
      width: 32px;
      padding-left: 0px;
      padding-right: 0px;
    }

    .multiselect__placeholder,
    .multiselect__single {
      margin-bottom: 0 !important;
    }
    .multiselect__placeholder {
      padding-top: 0;
      padding-left: 5px;
    }
    .multiselect__input {
      font-size: 1em;
      margin-bottom: 2px;
    }
  }
  .comment .message p:last-child {
    margin-bottom: 0;
  }
</style>
