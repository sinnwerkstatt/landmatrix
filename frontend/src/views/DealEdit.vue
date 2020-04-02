<template>
  <div class="container" v-if="deal">
    <b-tabs content-class="mt-3">
      {{deal}}
      <b-tab title="General Info" active>
        <div>
          <h3>Land area</h3>
          <div
            class="row mt-3"
            :class="formfield.class"
            v-for="formfield in formfields"
            :key="formfield.class"
          >
            <div class="col-md-3">
              <label :for="`type-${formfield.class}`">{{ formfield.label }}:</label>
            </div>
            <div class="col-md-9">
              <component
                :is="formfield.component"
                :formfield="formfield"
                v-model="deal"
              ></component>
            </div>
          </div>
        </div>
      </b-tab>
      <b-tab title="Other"> </b-tab>
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
  import store from "../store";
  import TextField from "../components/Fields/TextField";
  import ValueDateField from "../components/Fields/ValueDateField";

  export default {
    components: { TextField, ValueDateField },
    name: "DealEdit",
    props: ["deal_id"],
    data() {
      return {
        formfields: [
          {
            class: "intended_size",
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
          },
        ],
      };
    },
    computed: {
      deal: {
        get() {
          return this.$store.state.current_deal;
        },
        set(val) {
          console.log(val);
        },
      },
    },
    beforeRouteEnter(to, from, next) {
      let title = to.params.deal_id
        ? `Change Deal #${to.params.deal_id}`
        : `Add a Deal`;

      store.dispatch("setCurrentDeal", to.params.deal_id);
      store.dispatch("setPageContext", {
        title: title,
        breadcrumbs: [
          { link: { name: "wagtail" }, name: "Home" },
          { link: { name: "deal_list" }, name: "Data" },
          { name: title },
        ],
      });
      next();
    },
    beforeRouteLeave(to, from, next) {
      store.dispatch("setCurrentDeal", null);
      next();
    },
  };
</script>
