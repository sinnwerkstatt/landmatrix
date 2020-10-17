<template>
  <div class="table-wrap" v-if="deals.length > 0">
    <table class="sticky-header">
      <thead>
      <tr>
        <th v-for="fieldName in currentFields">
          {{ getLabel(fieldName) }}
        </th>
      </tr>
      </thead>
      <tbody>
      <tr v-for="obj in rows">
        <td v-for="fieldName in currentFields" :style="getStyle(fieldName)" v-html="getValue(obj, fieldName)">
      </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import {data_deal_query} from "/views/Data/query";
import {mapState} from "vuex";
import {
  getDealValue,
  getInvestorValue,
  dealExtraFieldLabels,
  investorExtraFieldLabels
} from "./table_mappings";
import gql from "graphql-tag";

export default {
  name: "Table",
  props: ['deals', 'targetModel'],
  data() {
    return {
      investors: [],
      fields: {
        deal: [
          "id",
          "country",
          "intention_of_investment",
          "current_negotiation_status",
          "current_implementation_status",
          "deal_size"
        ],
        investor: [
          "id",
          "name",
          "country",
          "classification",
          "deals",
        ],
      },
      valueMappings: {
        deal: getDealValue,
        investor: getInvestorValue,
      },
      extraFields: {
        deal: dealExtraFieldLabels,
        investor: investorExtraFieldLabels,
      }
    };
  },
  apollo: {
    investors: {
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
  },
  computed: {
    ...mapState({
      formfields: (state) => state.formfields,
    }),
    currentFields() {
      return this.fields[this.targetModel];
    },
    investorFilters() {
      return [{
        field: "deals.id",
        operation: "IN",
        value: this.deals.map(d => d.id.toString())
      }];
    },
    uniqueInvestors() {
      return this.investors.filter( (investor, index, self) => {
        return self.indexOf(investor) === index;
      });
    },
    rows() {
      if (this.targetModel === "deal") {
        return this.deals;
      } else if (this.targetModel === "investor") {
        return this.uniqueInvestors;
      } else {
        return [];
      }
    }
  },
  methods: {
    getLabel(fieldName) {
      if (this.formfields[this.targetModel] && fieldName in this.formfields[this.targetModel]) {
        return this.formfields[this.targetModel][fieldName].label;
      } else if (this.extraFields[this.targetModel] && fieldName in this.extraFields[this.targetModel]) {
        return this.extraFields[this.targetModel][fieldName];
      } else {
        return fieldName;
      }
    },
    getStyle(fieldName) {
      return {};
    },
    getValue(deal, fieldName) {
      return this.valueMappings[this.targetModel](this, deal, fieldName);
    }
  }
};
</script>
<style lang="scss">
.table-wrap {
  padding: 0 15px 2em 27px;
  border-top: solid white 3.4em;
  overflow-x: hidden;
  max-height: 100%;
  height: 100%;

  overflow: auto;
}

table.sticky-header {
  width: 100%;
  overflow-y: auto;

  height: 100px;

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
    //display: inline-block;
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
</style>
