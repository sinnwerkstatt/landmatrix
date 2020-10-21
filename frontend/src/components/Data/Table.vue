<template>
  <div class="data-table">
    <LoadingPulse v-if="$apollo.loading"/>
    <div class="table-config">
      <a href="" @click.prevent v-b-modal.modal-select-fields><i class="fa fa-cog"></i></a>
      <b-modal id="modal-select-fields" title="Select columns to display" @show="pauseUpdate" @hide="updateTable">
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
    <div class="table-wrap" v-if="rowData.length > 0">
      <div class="stats">
        <div class="rows-count">{{ rowData.length }} {{ modelLabel }}</div>
      </div>
      <table class="sticky-header" :class="[this.targetModel]">
        <thead>
        <tr>
          <th v-for="fieldName in currentFields"
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
          <td v-for="fieldName in currentFields"
              :key="fieldName"
              :style="getStyle(obj, fieldName)"
              v-html="getValue(obj, fieldName)"
          >
        </tr>
        </tbody>
      </table>
      <scroll-loader :loader-method="getPagedRows" :loader-disable="disableScrollLoader">
      </scroll-loader>
      <div class="spacer"></div>
    </div>
  </div>
</template>

<script>
import LoadingPulse from "/components/Data/LoadingPulse";
import {mapState} from "vuex";
import {dealExtraFieldLabels, getDealValue, getInvestorValue, investorExtraFieldLabels} from "./table_mappings";
import gql from "graphql-tag";
import {data_deal_query} from "/views/Data/query";
import {sortAnything} from "../../utils";

const DEAL_DEFAULT_QUERY_FIELDS = [
  "id",
  "deal_size",
  "country",
  "current_intention_of_investment",
  "current_negotiation_status",
  "current_implementation_status",
  "locations"
]

const DEFAULT_DISPLAY_FIELDS = {
  deal: [
    "id",
    "country",
    "intention_of_investment",
    "current_negotiation_status",
    "current_implementation_status",
    "deal_size",
    "intended_size"
  ],
  investor: [
    "id",
    "name",
    "country",
    "classification",
    "deals",
  ]
}

export default {
  name: "Table",
  components: {LoadingPulse},
  props: ['targetModel'],
  data() {
    return {
      deals: [],
      investors: [],
      displayFields: {...DEFAULT_DISPLAY_FIELDS},
      valueMappings: {
        deal: getDealValue,
        investor: getInvestorValue,
      },
      extraFieldLabels: {
        deal: dealExtraFieldLabels,
        investor: investorExtraFieldLabels,
      },
      extraDealData: [],
      dealApiFields: [],
      investorApiFields: [],
      disableScrollLoader: false,
      page: 1,
      pageSize: 30,
      rows: [],
      sortField: "id",
      sortAscending: true,
    };
  },
  apollo: {
    deals: data_deal_query,
    extraDealData: {
      query() {
        return gql`
        query Deals($limit: Int!, $filters: [Filter]) {
          extraDealData:deals(limit: $limit, filters: $filters) {
            id ${this.displayFields.deal.filter(f => !DEAL_DEFAULT_QUERY_FIELDS.includes(f)).join(' ')}
          }
        }
      `
      },
      variables() {
        return {
          limit: 0,
          filters: this.$store.getters.filtersForGQL,
        };
      },
    },
    investors: {
      skip() {
        return this.targetModel !== "investor"
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
            status_display
            draft_status
            draft_status_display
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
            fields { name }
          }
        }
      `,
      update: (data) => data.__type.fields.map(f => f.name),
    },
    investorApiFields: {
      query: gql`
        query {
          __type(name: "Investor") {
            fields { name }
          }
        }
      `,
      update: (data) => data.__type.fields.map(f => f.name),
    }
  },
  computed: {
    ...mapState({
      formfields: (state) => state.formfields,
    }),
    currentFields() {
      return this.displayFields[this.targetModel];
    },
    apiFields() {
      if (this.targetModel == "investor") {
        return this.investorApiFields;
      } else {
        return this.dealApiFields.sort((a, b) => {
          return this.getLabel(a, "deal").toLowerCase() > this.getLabel(b, "deal").toLowerCase();
        });
      }
    },
    investorFilters() {
      return [{
        field: "deals.id",
        operation: "IN",
        value: this.deals.map(d => d.id.toString())
      }];
    },
    uniqueInvestors() {
      return this.investors.filter((investor, index, self) => {
        return self.indexOf(investor) === index;
      });
    },
    extendedDeals() {
      if (this.extraDealData.length) {
        return this.deals.map(d => {
          return {
            ...d,
            ...this.extraDealData.find(e => e.id === d.id)
          }
        });
      } else {
        return this.deals;
      }
    },
    rowData() {
      let data = [];
      if (this.targetModel === "deal") {
        data = this.extendedDeals;
      } else if (this.targetModel === "investor") {
        data = this.uniqueInvestors;
      }
      return sortAnything(data, this.sortField, this.sortAscending);
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
      if (this.formfields[targetModel] && fieldName in this.formfields[targetModel]) {
        return this.formfields[targetModel][fieldName].label;
      } else if (this.extraFieldLabels[targetModel] && fieldName in this.extraFieldLabels[targetModel]) {
        return this.extraFieldLabels[targetModel][fieldName];
      } else {
        return fieldName;
      }
    },
    getStyle(obj, fieldName) {
      if (obj[fieldName] && !isNaN(obj[fieldName])) return { textAlign: "right"};
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
      this.sortField = 'id';
      this.sortAscending = true;
    },
  }
};
</script>
<style lang="scss" scoped>
@import "../../scss/colors";

.data-table {
  height: 100%;
  max-height: 100%;

  .table-wrap {
    padding: 0 15px 2em 27px;
    border-top: solid white 3.4em;
    overflow-x: hidden;
    max-height: 100%;
    height: 100%;

    overflow: auto;
  }

  .table-config {
    position: absolute;
    right: 30px;
    top: 20px;
    z-index: 1001;

    a {
      color: black;
      display: inline-block;

      &:hover {
        color: $lm_orange;
      }
    }
  }

  table.sticky-header {
    width: 100%;
    overflow-y: auto;

    tr {
      border: 1px solid #c9c9c9;
    }

    td {
      padding: 0.5em;
    }

    th {
      padding: 0.5em;
      position: sticky;
      top: 0;
      background: #525252;
      color: white;
      vertical-align: bottom;
      min-width: 60px;
      &:hover {
        cursor: pointer;
      }
      &.selected {
        font-weight: 600;
        color: $lm_orange;

        &.asc:before {
          content: "\f077";
          font-family: "Font Awesome 5 Free";
        }

        &:not(.asc):before {
          content: "\f078";
          font-family: "Font Awesome 5 Free";
        }
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

  .stats {
    position: absolute;
    top: 20px;
  }

}

</style>
<style lang="scss">
@import "../../scss/colors";

.data-table {
  .label {
    display: inline;
    padding: .2em .6em .3em;
    font-size: 75%;
    font-weight: 700;
    line-height: 1;
    color: #fff;
    text-align: center;
    white-space: nowrap;
    vertical-align: baseline;
    border-radius: .25em;

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
    background: #f4f4f4;
    border-radius: 5px;
    padding: 0.2em;
    white-space: nowrap;
    margin: 0.1em;
    display: inline-block;
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
