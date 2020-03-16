<template>
  <div v-if="deal">
    <b-tabs content-class="mt-3">
      <b-tab title="General Info" active>
        <div>
          <h3>Land area</h3>
          <b-row :class="formfield.class" v-for="formfield in formfields"
                 :key="formfield.class">
            <b-col md="3">
              <label :for="`type-${formfield.class}`">{{ formfield.label }}:</label>
            </b-col>
            <b-col md="9">
              <keep-alive>
                <component :is="formfield.component" :formfield="formfield" v-model="deal"></component>
              </keep-alive>
            </b-col>
          </b-row>
        </div>
      </b-tab>
      <b-tab title="Other">
      </b-tab>
    </b-tabs>
  </div>
</template>

<style lang="scss">
  .logo {
    width: 300px;
    text-align: center;
  }
</style>
<script>
  import store from '../store';
  import TextField from "@/components/TextField";
  import ValueDateField from "@/components/ValueDateField";

  export default {
    components:{ TextField, ValueDateField },
    name: 'DealEdit',
    props: ['deal_id'],
    data() {
      return {
        formfields: [
          {
            class: 'intended_size',
            component: "TextField",
            label: "Intended size (in ha)",
            placeholder: "Size",
            unit: "ha",
          },
          {
            class: "contract_size",
            component: "ValueDateField",
            label: "Size under contract (leased or purchased area, in ha)",
            placeholder: "Size",
            unit: "ha",
          }
        ]
      }
    },
    computed: {
      deal: {
        get() {
          return this.$store.state.current_deal;
        },
        set(val) {
          console.log(val);
        }
      }
    },
    beforeRouteEnter(to, from, next) {
      let title = (to.params.deal_id) ? `Change Deal #${to.params.deal_id}` : `Add a Deal`;

      store.dispatch('setCurrentDeal', to.params.deal_id);
      store.dispatch('setPageContext', {
        title: title,
        breadcrumbs: [{href: "/newdeal/", name: "Data"}, {name: title}],
      });
      next()
    },
    beforeRouteLeave(to, from, next) {
      store.dispatch('setCurrentDeal', null);
      next()
    },

  };


  //     bounds() {
  //       return L.latLngBounds(L.geoJSON(this.deal.geojson).getBounds()).pad(1.5);
  //     },
  //     geojson_options() {
  //       return {
  //         onEachFeature: this.onEachFeatureFunction
  //       };
  //     },
  //     geojson_styleFunction() {
  //       let styles = {
  //         contract_area: {
  //           dashArray: '5, 5',
  //           dashOffset: '0',
  //           fillColor: "#ffec03",
  //         },
  //         intended_area: {
  //           dashArray: '5, 5',
  //           dashOffset: '0',
  //           fillColor: "#ff8900",
  //         },
  //         production_area: {
  //           fillColor: "#ff0000",
  //         }
  //       };
  //       return (feature, layer) => {
  //         return {
  //           weight: 2,
  //           color: "#000000",
  //           opacity: 1,
  //           fillOpacity: 0.2,
  //           ...styles[feature.properties.type]
  //         };
  //       };
  //     },
  //     onEachFeatureFunction() {
  //       return (feature, layer) => {
  //         layer.bindTooltip(`<div>Name: ${feature.properties.name}</div>` +
  //             `<div>Type: ${feature.properties.type}</div>`,
  //             {permanent: false, sticky: true}
  //         );
  //       };
  //     }
  //   },
  //   methods: {
  //     general_info(deal) {
  //       return deal
  //     }
  //   },
  //   beforeRouteEnter(to, from, next) {
  //     store.dispatch('setTitle', `Deal #${to.params.deal_id}`);
  //     store.dispatch('setCurrentDeal', to.params.deal_id);
  //     next()
  //   },
  //   beforeRouteLeave(to, from, next) {
  //     store.dispatch('setCurrentDeal', null);
  //     next()
  //   },
  // }
</script>
