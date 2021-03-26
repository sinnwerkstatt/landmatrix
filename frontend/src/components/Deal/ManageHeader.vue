<template>
  <div class="row">
    <div class="col-md-10 manage-interface">
      <div class="row">
        <div class="col-sm-5 col-md-3">
          <h1>Deal #{{ deal.id }}</h1>
        </div>
        <div class="col-sm-7 col-md-9 panel-container">
          <DealDates :deal="deal"></DealDates>
        </div>
      </div>
      <div class="row fat-stati">
        <div class="col active">{{ $t("Draft") }}</div>
        <div class="col">Submitted for review</div>
        <div class="col">Submitted for activation</div>
        <div class="col">Activated</div>
      </div>
      <div class="row">
        <a href="" class="btn btn-secondary">Request improvement</a>
        <a href="" class="btn btn-primary">Submit for activation</a>
      </div>
      <div class="row d-flex align-items-center p-3">
        <div class="col-8">
          Last changes by Kurt
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
    </div>
    <div class="col-md-2 comments">
      Comments
    </div>
  </div>
</template>

<script>
  import DealDates from "./DealDates";
  export default {
    name: "ManageHeader",
    components: { DealDates },
    props: {
      deal: { type: Object, required: true },
    },
    methods: {
      get_confidential_reason(deal) {
        return {
          TEMPORARY_REMOVAL: this.$t("Temporary removal from PI after criticism"),
          RESEARCH_IN_PROGRESS: this.$t("Research in progress"),
          LAND_OBSERVATORY_IMPORT: this.$t("Land Observatory Import"),
        }[deal.confidential_reason];
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
