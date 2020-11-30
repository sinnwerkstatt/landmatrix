<template>
  <div class="data-table">
    <LoadingPulse v-if="$apollo.loading" />
    <div class="table-top-area-wrapper">
      <div class="table-top-area">
        <div class="stats">
          <div class="rows-count">{{ rowData.length }} {{ modelLabel }}</div>
        </div>
        <div class="table-config">
          <a href="" @click.prevent v-b-modal.modal-select-fields
          ><i class="fa fa-cog"></i
          ></a>
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
                  v-model="displayFields[targetModel]"
                  :key="option"
                  :value="option"
                  name="select-deal-fields"
                >
                  {{ getLabel(option) }}
                </b-form-checkbox>
              </b-form-group>
            </div>
            <template #modal-footer="{ ok, cancel, hide }">
              <a href="" @click.prevent="resetFields">Reset to default columns</a>
              <button type="button" class="btn btn-primary" @click="ok()">OK</button>
            </template>
          </b-modal>
        </div>
      </div>
    </div>
    <div class="table-wrap" v-if="rowData.length > 0">
      <table class="sticky-header" :class="[this.targetModel]">
        <thead>
        <tr>
          <th
            v-for="fieldName in currentFields"
            :key="fieldName"
            @click="setSort(fieldName)"
            :class="{ selected: sortField === fieldName, asc: sortAscending }"
          >
            {{ getLabel(fieldName) }}
          </th>
        </tr>
        </thead>
        <tbody>
        <tr v-for="obj in rows">
          <td
            v-for="fieldName in currentFields"
            :key="fieldName"
            :style="getStyle(obj, fieldName)"
            v-html="getValue(obj, fieldName)"
          ></td>
        </tr>
        </tbody>
      </table>
      <scroll-loader
        :loader-method="getPagedRows"
        :loader-disable="disableScrollLoader"
      >
      </scroll-loader>
      <div class="spacer"></div>
    </div>
  </div>
</template>

<script>
  import LoadingPulse from "/components/Data/LoadingPulse";
  import { mapState } from "vuex";
  import { dealExtraFieldLabels, getDealValue, getInvestorValue, investorExtraFieldLabels } from "./table_mappings";
  import gql from "graphql-tag";
  import { data_deal_query } from "/views/Data/query";
  import { sortAnything } from "../../utils";

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
    "top_investors"
  ];

  const DEFAULT_DISPLAY_FIELDS = {
    deal: [
      "fully_updated_at",
      "id",
      "country",
      "intention_of_investment",
      "current_negotiation_status",
      "current_implementation_status",
      "deal_size",
      "operating_company",
      "top_investors"
    ],
    investor: [
      "modified_at",
      "id",
      "name",
      "country",
      "classification",
      "deals"
    ]
  };

  export default {
    name: "Table",
    components: { LoadingPulse },
    props: ["targetModel"],
    data() {
      return {
        deals: [],
        investors: [],
        displayFields: { ...DEFAULT_DISPLAY_FIELDS },
        valueMappings: {
          deal: getDealValue,
          investor: getInvestorValue
        },
        extraFieldLabels: {
          deal: dealExtraFieldLabels,
          investor: investorExtraFieldLabels
        },
        extraDealData: [],
        dealApiFields: [],
        investorApiFields: [],
        disableScrollLoader: false,
        page: 1,
        pageSize: 50,
        rows: [],
        sortField: "fully_updated_at",
        sortAscending: false
      };
    },
    apollo: {
      deals: data_deal_query,
      extraDealData: {
        skip() {
          return !this.extraDealFields.length;
        },
        query() {
          return gql`
            query Deals($limit: Int!, $subset: Subset, $filters: [Filter]) {
              extraDealData:deals(limit: $limit, subset: $subset, filters: $filters) {
                id ${this.extraDealFields.join(" ")}
              }
            }
          `;
        },
        variables() {
          let user = this.$store.state.page.user;
          return {
            limit: 0,
            filters: this.$store.getters.filtersForGQL,
            subset: user && user.is_authenticated ? "ACTIVE" : "PUBLIC"
          };
        }
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
            filters: this.investorFilters
          };
        }
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
        update: (data) => data.__type.fields.map((f) => f.name)
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
        update: (data) => data.__type.fields.map((f) => f.name)
      }
    },
    computed: {
      ...mapState({
        formfields: (state) => state.formfields
      }),
      extraDealFields() {
        return this.displayFields.deal
          .filter((f) => !DEAL_DEFAULT_QUERY_FIELDS.includes(f));
      },
      currentFields() {
        return this.displayFields[this.targetModel];
      },
      apiFields() {
        if (this.targetModel == "investor") {
          return this.investorApiFields;
        } else {
          return this.dealApiFields.sort((a, b) => {
            return (
              this.getLabel(a, "deal").toLowerCase() >
              this.getLabel(b, "deal").toLowerCase()
            );
          });
        }
      },
      investorFilters() {
        if (this.fetchAllInvestors) {
          return [];
        } else {
          return [
            {
              field: "deals.id",
              operation: "IN",
              value: this.deals.map((d) => d.id.toString())
            }
          ];
        }
      },
      fetchAllInvestors() {
        return this.deals.length > 1000;
      },
      filteredInvestors() {
        return this.investors.filter((investor, index, self) => {
          // remove duplicates
          if (self.indexOf(investor) !== index) return false;
          // filter on client
          if (this.fetchAllInvestors) {
            return investor.deals.some(d => this.dealIds.includes(d.id));
          }
          return true;
        });
      },
      dealIds() {
        return this.deals.map(d => d.id);
      },
      dealsLoaded() {
        if (this.extraDealFields.length) {
          if (!this.extraDealData.length || this.$apollo.queries.extraDealData.loading || this.deals.length !== this.extraDealData.length) {
            return false;
          }
        }
        return !this.$apollo.queries.deals.loading && this.deals.length;
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
      }
    },
    methods: {
      getLabel(fieldName, targetModel = null) {
        if (!targetModel) targetModel = this.targetModel;
        if (
          this.extraFieldLabels[targetModel] &&
          fieldName in this.extraFieldLabels[targetModel]
        ) {
          return this.extraFieldLabels[targetModel][fieldName];
        } else if (this.formfields[targetModel] && fieldName in this.formfields[targetModel]) {
          return this.formfields[targetModel][fieldName].label;
        } else {
          return fieldName;
        }
      },
      getStyle(obj, fieldName) {
        if (obj[fieldName] && !isNaN(obj[fieldName])) return { textAlign: "right" };
        else return {};
      },
      getValue(obj, fieldName) {
        return this.valueMappings[this.targetModel](this, obj, fieldName);
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
      }
    },
    watch: {
      rowData() {
        if (!this.$apollo.loading) {
          this.resetPages();
        }
      },
      targetModel() {
        if (this.targetModel === "investor") {
          this.sortField = "modified_at";
        }
        this.sortField = "fully_updated_at";
        this.sortAscending = false;
      }
    }
  };
</script>
<style lang="scss" scoped>
  @import "../../scss/colors";

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
          //position: absolute;
          //top: 0;
          display: inline-block;
        }

        .table-config {
          //position: absolute;
          float: right;
          display: inline-block;
          z-index: 1;

          a {
            color: black;
            display: inline-block;

            &:hover {
              color: $lm_orange;
            }
          }
        }
      }
    }

    .table-wrap {
      padding: 0 15px 2em 27px;
      overflow-x: hidden;
      overflow: auto; // just setting overflow-y gives different result (table not scrollable)
      max-height: calc( 100% - 50px );
      height: calc( 100% - 50px );
      position: relative;
    }


    table.sticky-header {
      width: 100%;
      overflow-y: auto;

      thead {
        tr {
          th {
            padding: 0.5em;
            position: sticky;
            top: 0px;
            background: #525252;
            color: white;
            vertical-align: bottom;
            min-width: 60px;
            font-weight: normal;

            &:hover {
              cursor: pointer;
            }

            &.selected {
              font-weight: normal;
              color: $lm_orange;

              &.asc:before {
                font-weight: 600;
                content: "\f077";
                font-family: "Font Awesome 5 Free";
              }

              &:not(.asc):before {
                font-weight: 600;
                content: "\f078";
                font-family: "Font Awesome 5 Free";
              }
            }
          }
        }
      }
      tr {
        td {
          padding: 0.3em 0.3em;
          border-bottom: 1px solid #c9c9c9;
        }

        &:nth-child(even) {
          background-color: white;
        }

        &:nth-child(odd) {
          background-color: darken(white, 3);
        }
      }



    }

    table.investor {
      th.selected {
        color: $lm_investor;
      }
    }

    .spacer {
      height: 25px;
    }
  }
</style>
<style lang="scss">
  @import "../../scss/colors";

  .data-table {
    .label {
      display: inline;
      padding: 0.2em 0.6em 0.3em;
      font-size: 75%;
      font-weight: 700;
      line-height: 1;
      color: #fff;
      text-align: center;
      white-space: nowrap;
      vertical-align: baseline;
      border-radius: 0.25em;

      &:hover {
        text-decoration: none;
        color: #fff;
      }

      &.label-deal {
        background-color: $lm_orange;

        &:hover {
          background-color: darken($lm_orange, 10%);
        }
      }

      &.label-investor {
        background-color: $lm-investor;

        &:hover {
          background-color: darken($lm-investor, 10%);
        }
      }
    }

    .ioi-label {
      background: rgba(0, 0, 0, 0.05);
      border-radius: 5px;
      padding: 0.15em 0.35em;
      white-space: nowrap;
      margin: 0.2em 0.05em 0 0;
      display: inline-block;
      border: 1px solid rgba(0, 0, 0, 0.05);
      color: rgba(black, 0.7)
    }

    .loader {
      color: transparent;
    }
  }

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
