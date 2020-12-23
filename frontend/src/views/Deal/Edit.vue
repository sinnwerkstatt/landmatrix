<template>
  <div class="container" v-if="deal">
    <b-tabs content-class="mb-3">
      <b-tab title="Location" active>
        <map-editor />
      </b-tab>
      <b-tab title="General Info">
        <DealSection :deal="deal" :sections="general_info" />
      </b-tab>
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
  import store from "store";
  import MapEditor from "components/MapEditor";
  import DealSection from "components/Deal/DealSection";

  export default {
    components: { MapEditor, DealSection },
    name: "DealEdit",
    props: ["deal_id"],
    data() {
      return {
        general_info: "gi",
      };
    },
    computed: {
      deal() {
        return {};
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
      next((vm) => {
        if (!vm.$store.getters.userAuthenticated) {
          window.location = `/accounts/login/?next=${to.path}`;
        }
      });
    },
  };
</script>
