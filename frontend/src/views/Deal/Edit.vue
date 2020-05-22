<template>
  <div class="container" v-if="deal">
    <b-tabs content-class="mt-3">
      <b-tab title="Location" active>
        <map-editor/>
      </b-tab>
      <b-tab title="General Info">
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
      <b-tab title="Other"></b-tab>
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
  import deal_fields from "./deal_fields";
  import MapEditor from "@/components/MapEditor";

  export default {
    components: { MapEditor, TextField, ValueDateField },
    name: "DealEdit",
    props: ["deal_id"],
    data() {
      return {
        formfields: deal_fields,
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
      store.dispatch("setCurrentDeal", {});
      next();
    },
  };
</script>
