<template>
  <div>
    <DataContainer>
      <template v-slot:default>
        <LoadingPulse v-if="$apollo.queries.deals.loading" />
        <div class="h-100">
          <div
            class="sideBuffer float-left"
            :class="{ collapsed: !$store.state.map.showFilterOverlay }"
          ></div>
          <div
            class="sideBuffer float-right"
            :class="{ collapsed: !$store.state.map.showScopeOverlay }"
          ></div>
          <!--          <div style="float: bottom;min-height: 31px; "></div>-->
          <div class="table-wrap" v-if="deals.length > 0">
            <table class="sticky-header">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Target country</th>
                  <th>Intention of investment</th>
                  <th>
                    Negotiation Status<br /><span style="font-weight: normal;"
                      >Implementation Status</span
                    >
                  </th>
                  <th>Deal size</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="deal in enriched_deals">
                  <td>
                    <router-link
                      :to="{ name: 'deal_detail', params: { deal_id: deal.id } }"
                      >{{ deal.id }}</router-link
                    >
                  </td>
                  <td v-html="deal.country"></td>
                  <td v-html="deal.intention_of_investment"></td>
                  <td>
                    {{ deal.current_negotiation_status }}<br />
                    {{ deal.current_implementation_status }}
                  </td>
                  <td class="text-right">{{ deal.deal_size }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </template>
    </DataContainer>
  </div>
</template>

<script>
  import gql from "graphql-tag";
  import DataContainer from "./DataContainer";
  import LoadingPulse from "/components/Data/LoadingPulse";
  import {
    implementation_status_choices,
    intention_of_investment_map,
    negotiation_status_map,
  } from "/choices";
  import { data_deal_query } from "./query";

  export default {
    name: "DataList",
    components: { LoadingPulse, DataContainer },
    apollo: {
      deals: data_deal_query,
    },
    data() {
      return {
        deals: [],
      };
    },
    computed: {
      enriched_deals() {
        if (this.deals.length === 0) return [];
        return this.deals.map((deal) => {
          let cor = this.$store.getters.getCountryOrRegion({
            type: "country",
            id: deal.country.id,
          });
          cor = cor ? cor.name : "";

          let intentions;
          if (deal.current_intention_of_investment) {
            intentions = deal.current_intention_of_investment
              .map((ioi) => {
                let [intention, icon] = intention_of_investment_map[ioi];
                return `<span class="ioi-label"><i class="${icon}"></i> ${this.$t(
                  intention
                )}</span> `;
              })
              .join(" ");
          }
          let [neg_status, neg_status_group] = negotiation_status_map[
            deal.current_negotiation_status
          ];
          return {
            id: deal.id,
            country: `<a>${cor}</a>`,
            intention_of_investment: intentions,
            current_negotiation_status: neg_status_group
              ? `${neg_status_group} (${neg_status})`
              : neg_status,
            current_implementation_status: deal.current_implementation_status
              ? implementation_status_choices[deal.current_implementation_status]
              : "None",
            deal_size: deal.deal_size.toLocaleString(),
          };
        });
      },
    },
  };
</script>
<style lang="scss">
  .sideBuffer {
    min-width: 230px;
    width: 20%;
    min-height: 3px;
    transition: width 0.5s, min-width 0.5s;
    &.collapsed {
      width: 0;
      min-width: 0;
    }
  }

  .table-wrap {
    padding: 0 23px 1em;
    border-top: solid white 3em;
    overflow-x: hidden;
    max-height: 100%;
    height: 100%;

    overflow-y: auto;
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
      white-space: nowrap;
      position: sticky;
      top: 0;
      background: #525252;
      color: white;
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

  //::-webkit-scrollbar {
  //  width: 14px;
  //  height: 18px;
  //}
  //::-webkit-scrollbar-thumb {
  //  height: 6px;
  //  border: 4px solid rgba(0, 0, 0, 0);
  //  background-clip: padding-box;
  //  -webkit-border-radius: 7px;
  //  background-color: rgba(0, 0, 0, 0.15);
  //  -webkit-box-shadow: inset -1px -1px 0px rgba(0, 0, 0, 0.05),
  //    inset 1px 1px 0px rgba(0, 0, 0, 0.05);
  //}
  //::-webkit-scrollbar-button {
  //  width: 0;
  //  height: 0;
  //  display: none;
  //}
  //::-webkit-scrollbar-corner {
  //  background-color: transparent;
  //}
</style>
