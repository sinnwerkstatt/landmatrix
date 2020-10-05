<template>
  <div>
    <DataContainer>
      <template v-slot:default>
        <LoadingPulse v-if="$apollo.queries.deals.loading" />
        <div>
          <div
            class="sideBuffer float-left"
            :class="{ collapsed: !$store.state.map.showFilterOverlay }"
          ></div>
          <div
            class="sideBuffer float-right"
            :class="{ collapsed: !$store.state.map.showScopeOverlay }"
          ></div>
          <div style="overflow: hidden; padding: 1em;">
            Bavaria ipsum dolor sit amet nia need hod dahoam Deandlgwand di Sauwedda
            Marei auf’d Schellnsau. Amoi Reiwadatschi Graudwiggal woaß nia need fei
            ozapfa, wea nia ausgähd, kummt nia hoam wuid a so a Schmarn. Engelgwand wo
            hi Lewakaas, Schbozal sog i Guglhupf Milli fensdaln und bitt aba: Mamalad
            back mas Blosmusi gwihss Ledahosn hogg di hera vo de i moan scho aa,
            Spotzerl Schuabladdla unbandig! Leonhardifahrt umma jo mei is des schee
            ghupft wia gsprunga Gaudi is des liab, sodala mehra. Boarischer wuid so
            schee woaß Buam unbandig Bradwurschtsemmal mi. I waar soweid i hab an Buam
            no a Maß, allerweil mim Watschnpladdla a Hoiwe? Des Greichats Fünferl
            obandeln do des muas ma hoid kenna a bissal Schneid. Moand a bravs i hob di
            narrisch gean und sei Heimatland, des auf gehds beim Schichtl.
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

  export default {
    name: "DataList",
    components: { LoadingPulse, DataContainer },
    apollo: {
      deals: {
        query: gql`
          query Deals($limit: Int!, $filters: [Filter]) {
            deals(limit: $limit, filters: $filters) {
              id
              deal_size
              country {
                id
                fk_region {
                  id
                }
              }
              # top_investors { id name }
              intention_of_investment
              current_negotiation_status
              current_implementation_status
              locations {
                id
                point
                level_of_accuracy
              }
            }
          }
        `,
        variables() {
          return {
            limit: 0,
            filters: this.$store.getters.filtersForGQL,
          };
        },
      },
    },
    data() {
      return {
        deals: [],
      };
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
  //.filterBuffer {
  //  float: left;
  //}
</style>
