<template>
  <div class="container" v-if="deal">
    <b-tabs content-class="mt-3">
      <b-tab title="General Info" active>
        <div>
          <h3>Land area</h3>
          <div
            v-for="formfield in formfields"
            :key="formfield.name"
            :class="['row', 'mt-3', formfield.name]"
          >
            <div class="col-md-3">
              <label :for="`type-${formfield.name}`">{{ formfield.label }}:</label>
            </div>
            <div class="col-md-9">
              <component
                :is="formfield.component"
                :formfield="formfield"
                v-model="deal[formfield.name]"
              ></component>
            </div>
          </div>
        </div>
      </b-tab>
      <b-tab title="Other"> </b-tab>
    </b-tabs>
    <button class="btn btn-primary" type="submit">Submit</button>

  </div>
</template>

<style lang="scss">
  .logo {
    width: 300px;
    text-align: center;
  }
</style>

<script>
  import store from "@/store";
  import TextField from "@/components/Fields/TextField";
  import ValueDateField from "@/components/Fields/ValueDateField";

  export default {
    components: { TextField, ValueDateField },
    name: "DealEdit",
    props: ["deal_id"],
    data() {
      return {
        formfields: [
          {
            name: "intended_size",
            component: "TextField",
            label: "Intended size (in ha)",
            placeholder: "Size",
            unit: "ha",
          },
          {
            name: "contract_size",
            component: "ValueDateField",
            label: "Size under contract (leased or purchased area, in ha)",
            placeholder: "Size",
            unit: "ha",
          },
          {
            name: "operation_size",
            component: "ValueDateField",
            label: "Size in operation (production, in ha)",
            placeholder: "Size",
            unit: "ha",
          },
        ],
      };
    },
    computed: {
      deal() {
        return this.$store.state.deal.current_deal;
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
