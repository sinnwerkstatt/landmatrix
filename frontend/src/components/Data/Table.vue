<template>
  <div class="data-table">
    <LoadingPulse v-if="$apollo.loading" />
    <div class="table-top-area-wrapper">
      <div class="table-top-area">
        <div class="stats">
          <div class="rows-count">{{ rowData.length }} {{ modelLabel }}</div>
        </div>
        <div class="table-config">
          <a v-b-modal.modal-select-fields href="" @click.prevent>
            <i class="fa fa-cog"></i>
          </a>
          <b-modal
            id="modal-select-fields"
            title="Select columns to display"
            @show="pauseUpdate"
            @hide="updateTable"
          >
            <div class="inner-scroll-container">
              <b-form-group>
                <b-form-checkbox
                  v-for="option in apiFields"
                  :key="option"
                  v-model="displayFields[targetModel]"
                  :value="option"
                  name="select-deal-fields"
                >
                  {{ getLabel(option) }}
                </b-form-checkbox>
              </b-form-group>
            </div>
            <template #modal-footer="{ ok }">
              <a href="" @click.prevent="resetFields">Reset to default columns</a>
              <button type="button" class="btn btn-primary" @click="ok()">OK</button>
            </template>
          </b-modal>
        </div>
      </div>
    </div>
    <div v-if="rowData.length > 0" class="table-wrap">
      <table class="bigtable" :class="targetModel">
        <thead>
          <tr>
            <th
              v-for="fieldName in currentFields"
              :key="fieldName"
              :class="{ selected: sortField === fieldName, asc: sortAscending }"
              @click="setSort(fieldName)"
            >
              <FieldLabel
                :fieldname="fieldName"
                :label-classes="[]"
                :model="targetModel"
              />
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="obj in rows" :key="obj.id">
            <td
              v-for="fieldName in currentFields"
              :key="fieldName"
              :style="getStyle(obj, fieldName)"
            >
              <DisplayField
                :wrapper-classes="[]"
                :value-classes="[]"
                :fieldname="fieldName"
                :value="obj[fieldName]"
                :model="targetModel"
                :show-label="false"
              />
            </td>
          </tr>
        </tbody>
      </table>
      <scroll-loader
        :loader-method="getPagedRows"
        :loader-disable="disableScrollLoader"
      >
      </scroll-loader>
    </div>
  </div>
</template>

<script>
  import LoadingPulse from "$components/Data/LoadingPulse";
  import DisplayField from "$components/Fields/DisplayField";
  import FieldLabel from "$components/Fields/FieldLabel";
  import { sortAnything } from "$utils";
  import { data_deal_query } from "$views/Data/query";
  import gql from "graphql-tag";
  import { mapState } from "vuex";

  const DEAL_DEFAULT_QUERY_FIELDS = [
    "id",
    "deal_size",
    "country",
    "current_intention_of_investment",
    "current_negotiation_status",
    "current_implementation_status",
    "locations",
    "fully_updated_at",
    "operating_company",
    "top_investors",
  ];

  const DEFAULT_DISPLAY_FIELDS = {
    deal: [
      "fully_updated_at",
      "id",
      "country",
      "current_intention_of_investment",
      "current_negotiation_status",
      "current_implementation_status",
      "deal_size",
      "operating_company",
      "top_investors",
    ],
    investor: ["modified_at", "id", "name", "country", "classification", "deals"],
  };

  export default {
    name: "Table",
    components: { FieldLabel, DisplayField, LoadingPulse },
    props: {
      targetModel: { type: String, required: true },
    },
    data() {
      return {
        deals: [],
        investors: [],
        displayFields: { ...DEFAULT_DISPLAY_FIELDS },
        extraDealData: [],
        dealApiFields: [],
        investorApiFields: [],
        disableScrollLoader: false,
        page: 1,
        pageSize: 50,
        rows: [],
        sortField: "fully_updated_at",
        sortAscending: false,
      };
    },
    apollo: {
      deals: data_deal_query,
      extraDealData: {
        skip() {
          return !this.extraDealFields.length;
        },
        query() {
          return `
            query Deals($limit: Int!, $subset: Subset, $filters: [Filter]) {
              extraDealData:deals(limit: $limit, subset: $subset, filters: $filters) {
                id ${this.extraDealFields.join(" ")}
              }
            }
          `;
        },
        variables() {
          return {
            limit: 0,
            filters: this.$store.getters.filtersForGQL,
            subset: this.$store.getters.userAuthenticated
              ? this.$store.state.filters.publicOnly
                ? "ACTIVE"
                : "UNFILTERED"
              : "PUBLIC",
          };
        },
      },
      investors: {
        skip() {
          return this.targetModel !== "investor";
        },
        query: gql`
          query Investors($limit: Int!, $filters: [Filter]) {
            investors(limit: $limit, filters: $filters) {
              id
              name
              country {
                id
                name
              }
              classification
              homepage
              opencorporates
              comment
              #involvements
              deals {
                id
              }
              status
              draft_status
              created_at
              modified_at
              is_actually_unknown
            }
          }
        `,
        variables() {
          return {
            limit: 0,
            filters: this.investorFilters,
          };
        },
      },
      dealApiFields: {
        query: gql`
          query {
            __type(name: "Deal") {
              fields {
                name
              }
            }
          }
        `,
        update: (data) => data.__type.fields.map((f) => f.name),
      },
      investorApiFields: {
        query: gql`
          query {
            __type(name: "Investor") {
              fields {
                name
              }
            }
          }
        `,
        update: (data) => data.__type.fields.map((f) => f.name),
      },
    },
    computed: {
      ...mapState({
        formfields: (state) => state.formfields,
      }),
      extraDealFields() {
        return this.displayFields.deal.filter(
          (f) => !DEAL_DEFAULT_QUERY_FIELDS.includes(f)
        );
      },
      currentFields() {
        return this.displayFields[this.targetModel];
      },
      apiFields() {
        if (this.targetModel === "investor") {
          return this.investorApiFields;
        } else {
          return [...this.dealApiFields].sort((a, b) => {
            let label_a = this.getLabel(a).toLowerCase();
            let label_b = this.getLabel(b).toLowerCase();
            return label_a.localeCompare(label_b);
          });
        }
      },
      investorFilters() {
        if (this.fetchAllInvestors) {
          return [];
        } else {
          let filters = [
            {
              field: "child_deals.id",
              operation: "IN",
              value: this.deals.map((d) => d.id.toString()),
            },
          ];

          let store_state_filters = this.$store.state.filters.filters;
          if (store_state_filters.investor) {
            filters.push({
              field: "id",
              value: store_state_filters.investor.id.toString(),
            });
          }
          if (store_state_filters.investor_country_id) {
            filters.push({
              field: "country_id",
              value: store_state_filters.investor_country_id.toString(),
            });
          }
          return filters;
        }
      },
      fetchAllInvestors() {
        return this.deals.length > 2500;
      },
      filteredInvestors() {
        return this.investors.filter((investor, index, self) => {
          // remove duplicates
          if (self.indexOf(investor) !== index) return false;
          // filter on client
          if (this.fetchAllInvestors) {
            return investor.deals.some((d) => this.dealIds.includes(d.id));
          }
          return true;
        });
      },
      dealIds() {
        return this.deals.map((d) => d.id);
      },
      dealsLoaded() {
        if (this.extraDealFields.length) {
          if (
            !this.extraDealData.length ||
            (this.$apollo.queries.extraDealData &&
              this.$apollo.queries.extraDealData.loading) ||
            this.deals.length !== this.extraDealData.length
          ) {
            return false;
          }
        }
        return (
          !(this.$apollo.queries.deals && this.$apollo.queries.deals.loading) &&
          this.deals.length
        );
      },
      extendedDeals() {
        if (this.dealsLoaded) {
          if (this.extraDealData.length) {
            let idMap = {};
            // map by id first, searching each time is too expensive
            for (let extraData of this.extraDealData) {
              idMap[extraData.id] = extraData;
            }
            for (let deal of this.deals) {
              let extraData = idMap[deal.id];
              for (let field of this.extraDealFields) {
                deal[field] = extraData[field];
              }
            }
            return this.deals;
          } else {
            return this.deals;
          }
        } else {
          return [];
        }
      },
      rowData() {
        let data = [];
        if (this.targetModel === "deal") {
          data = this.extendedDeals;
        } else if (this.targetModel === "investor") {
          data = this.filteredInvestors;
        }
        data = sortAnything(data, this.sortField, this.sortAscending);
        return data;
      },
      modelLabel() {
        if (this.targetModel === "investor") {
          return this.$t("Investors");
        } else {
          return this.$t("Deals");
        }
      },
    },
    watch: {
      rowData() {
        if (!this.$apollo.loading) {
          this.resetPages();
        }
      },
      targetModel() {
        this.sortField =
          this.targetModel === "investor" ? "modified_at" : "fully_updated_at";
        this.sortAscending = false;
      },
    },
    created() {
      this.sortField =
        this.targetModel === "investor" ? "modified_at" : "fully_updated_at";
    },
    methods: {
      getLabel(fieldName, targetModel = "deal") {
        if (!targetModel) targetModel = this.targetModel;
        if (this.formfields[targetModel] && fieldName in this.formfields[targetModel]) {
          return this.formfields[targetModel][fieldName].label;
        } else {
          return fieldName;
        }
      },
      getStyle(obj, fieldName) {
        if (obj[fieldName] && !isNaN(obj[fieldName])) return { textAlign: "right" };
        else return {};
      },
      setSort(field) {
        if (this.sortField === field) this.sortAscending = !this.sortAscending;
        this.sortField = field;
      },
      pauseUpdate() {
        this.$apollo.skipAllQueries = true;
      },
      updateTable() {
        this.$apollo.skipAllQueries = false;
        this.$apollo.queries.extraDealData.refetch();
      },
      resetFields() {
        this.displayFields[this.targetModel] = DEFAULT_DISPLAY_FIELDS[this.targetModel];
      },
      getPagedRows() {
        let startIndex = (this.page - 1) * this.pageSize;
        let endIndex = Math.min(this.page * this.pageSize, this.rowData.length);
        this.disableScrollLoader = this.page * this.pageSize > this.rowData.length;
        this.page++;
        this.rows = [...this.rows, ...this.rowData.slice(startIndex, endIndex)];
      },
      resetPages() {
        this.rows = [];
        this.page = 1;
        this.disableScrollLoader = false;
      },
    },
  };
</script>
<style lang="scss" scoped>
  .data-table {
    height: 100%;
    max-height: 100%;
    background-color: darken(white, 10);
    font-size: 0.9rem;
    line-height: 1.1;

    .table-top-area-wrapper {
      padding: 30px 2em 0 27px;
      overflow-x: hidden;
      position: relative;

      .table-top-area {
        width: 100%;
        height: 20px;

        .stats {
          display: inline-block;
        }

        .table-config {
          float: right;
          display: inline-block;
          z-index: 1;
          display: none; // TODO: decide how change column settings

          a {
            color: black;
            display: inline-block;

            &:hover {
              color: var(--color-lm-orange);
            }
          }
        }
      }
    }

    .table-wrap {
      padding: 0 15px 2em 27px;
      overflow: auto;
      max-height: calc(100% - 50px);
      height: calc(100% - 50px - 25px);
      position: relative;
    }
  }
</style>
<style lang="scss">
  //.data-table {
  //  .label {
  //    display: inline;
  //    padding: 0.2em 0.6em 0.3em;
  //    font-size: 75%;
  //    font-weight: 700;
  //    line-height: 1;
  //    color: #fff;
  //    text-align: center;
  //    white-space: nowrap;
  //    vertical-align: baseline;
  //    border-radius: 0.25em;
  //
  //    &:hover {
  //      text-decoration: none;
  //      color: #fff;
  //    }
  //
  //    &.label-deal {
  //      background-color: var(--color-lm-orange);
  //
  //      &:hover {
  //        background-color: var(--color-lm-orange-dark);
  //      }
  //    }
  //
  //    &.label-investor {
  //      background-color: var(--color-lm-investor);
  //
  //      &:hover {
  //        background-color: var(--color-lm-investor-dark);
  //      }
  //    }
  //  }
  //
  //  .loader {
  //    color: transparent;
  //  }
  //}

  #modal-select-fields {
    .modal-body {
      height: 75%;
      max-height: 75vh;
      overflow-x: scroll;
      padding-bottom: 0;
    }

    footer {
      justify-content: space-between;
    }
  }
</style>
