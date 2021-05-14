<template>
  <div class="row">
    <div class="col-md-10 manage-interface">
      <div class="row">
        <div class="col-sm-5 col-md-3">
          <h1>Deal #{{ deal.id }}</h1>
        </div>
        <div class="col-sm-7 col-md-9 panel-container">
          <HeaderDates :obj="deal" />
        </div>
      </div>
      <div class="row fat-stati">
        <div class="col" :class="{ active: deal.draft_status === 1 }">
          {{ $t("Draft") }}
        </div>
        <div class="col" :class="{ active: deal.draft_status === 2 }">
          {{ $t("Submitted for review") }}
        </div>
        <div class="col" :class="{ active: deal.draft_status === 3 }">
          {{ $t("Submitted for activation") }}
        </div>
        <div class="col" :class="{ active: deal.draft_status === null }">
          {{ $t("Activated") }}
        </div>
      </div>
      <div class="row workflow-buttons">
        <div class="col text-right">
          <a
            v-if="deal.draft_status === 1"
            class="btn btn-primary"
            @click="change_deal_status('TO_REVIEW')"
          >
            {{ $t("Submit for review") }}
          </a>
          <a
            v-if="deal.draft_status === 2 || deal.draft_status === 3"
            class="btn btn-secondary"
            @click="change_deal_status('TO_DRAFT')"
          >
            {{ $t("Request improvement") }}
          </a>
        </div>
        <div class="col text-center">
          <a
            v-if="deal.draft_status === 2"
            class="btn btn-primary"
            @click="change_deal_status('TO_ACTIVATION')"
          >
            {{ $t("Submit for activation") }}
          </a>
        </div>
        <div class="col text-left">
          <a
            v-if="deal.draft_status === 3"
            class="btn btn-primary"
            @click="change_deal_status('ACTIVATE')"
          >
            {{ $t("Activate") }}
          </a>
        </div>
      </div>
      <div class="row d-flex align-items-center p-3">
        <div v-if="last_revision" class="col-8">
          Last changes by {{ last_revision.user.full_name }} on
          {{ last_revision.date_created | dayjs("dddd YYYY-MM-DD HH:mm") }}<br />
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
        <div class="col-4 visibility-container">
          <span v-if="deal.is_public">
            <i class="far fa-check-circle fa-fw fa-lg"></i> {{ $t("Publicly visible") }}
          </span>
          <span v-else>
            <i class="far fa-times-circle fa-fw fa-lg"></i>
            {{ $t("Not publicly visible") }}
          </span>
          <br />
          <ul>
            <li v-if="!deal.confidential">
              <i class="fas fa-check fa-fw"></i> {{ $t("Not confidential") }}
            </li>
            <li v-else>
              <i class="fas fa-times fa-fw"></i>
              <b-button
                id="confidential"
                style="color: black; background: inherit; border: 0; padding: 0;"
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
              <i class="fas fa-check fa-fw"></i> {{ $t("Target country is set") }}
            </li>
            <li v-else>
              <i class="fas fa-times fa-fw"></i> {{ $t("Target country is NOT set") }}
            </li>

            <li v-if="deal.datasources.length > 0">
              <i class="fas fa-check fa-fw"></i> {{ $t("At least one data source") }}
            </li>
            <li v-else>
              <i class="fas fa-times fa-fw"></i> {{ $t("No data source") }}
            </li>

            <li v-if="deal.has_known_investor">
              <i class="fas fa-check fa-fw"></i> {{ $t("At least one investor") }}
            </li>
            <li v-else><i class="fas fa-times fa-fw"></i> {{ $t("No investor") }}</li>
          </ul>
        </div>
      </div>
      <div class="row edit-button">
        <div class="col" style="margin-bottom: -1rem;">
          <router-link
            class="btn btn-primary btn-lg"
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
    <div class="col-md-2 comments">
      Comments
    </div>
  </div>
</template>

<script>
  import gql from "graphql-tag";
  import HeaderDates from "../HeaderDates";

  export default {
    name: "ManageHeader",
    components: { HeaderDates },
    props: {
      deal: { type: Object, required: true },
      dealVersion: { type: [Number, String], default: null },
    },
    computed: {
      last_revision() {
        return this.deal?.versions[0]?.revision ?? "";
      },
    },
    methods: {
      get_confidential_reason(deal) {
        return {
          TEMPORARY_REMOVAL: this.$t("Temporary removal from PI after criticism"),
          RESEARCH_IN_PROGRESS: this.$t("Research in progress"),
          LAND_OBSERVATORY_IMPORT: this.$t("Land Observatory Import"),
        }[deal.confidential_reason];
      },
      change_deal_status(transition) {
        this.$apollo
          .mutate({
            mutation: gql`
              mutation($id: Int!, $transition: WorkflowTransition) {
                change_deal_status(id: $id, transition: $transition)
              }
            `,
            variables: { id: this.deal.id, transition },
          })
          .then((data) => {
            this.$router.push({
              name: "deal_manage",
              params: {
                dealId: this.deal.id,
                dealVersion: data.data.change_deal_status,
              },
            });
          })
          .catch((error) => console.error(error));
      },
    },
  };
</script>

<style scoped lang="scss">
  i {
    color: var(--primary);
  }
  .manage-interface {
    background: #e5e5e5;
    margin-bottom: 2rem;
  }
  .fat-stati > .col {
    margin: 0.5rem;
    padding: 0.5rem 2rem;
    background: #dbdbdb;
    &.active {
      background: #93c7c8;
    }
  }
  .comments {
    padding: 0.5rem;
    height: 300px;
    width: 100%;
    background: #c4c4c4;
  }
  .visibility-container ul {
    list-style: none;
    padding: 0;
  }
</style>
