<template>
  <div class="container" v-if="deal">
    <b-tabs
      id="tabNav"
      :key="dealId + dealVersion"
      content-class="mb-3"
      vertical
      pills
      nav-wrapper-class="col-12 col-sm-5 col-md-3 position-relative"
      nav-class="sticky-nav"
    >
      <DealEditSection
        :title="deal_sections.general_info.label"
        :deal="deal"
        :sections="deal_sections.general_info.subsections"
        :active="active_tab === '#general'"
        @activated="updateRoute('#general')"
      />
      <!--      <b-tab title="Location">-->
      <!--        <map-editor />-->
      <!--      </b-tab>-->
      <DealEditSection
        :title="deal_sections.employment.label"
        :deal="deal"
        :sections="deal_sections.employment.subsections"
        :active="active_tab === '#employment'"
        @activated="updateRoute('#employment')"
      />
      <DealEditSection
        :title="deal_sections.produce_info.label"
        :deal="deal"
        :sections="deal_sections.produce_info.subsections"
        :active="active_tab === '#produce_info'"
        @activated="updateRoute('#produce_info')"
      />
      <DealEditSection
        :title="deal_sections.guidelines_and_principles.label"
        :deal="deal"
        :sections="deal_sections.guidelines_and_principles.subsections"
        :active="active_tab === '#guidelines_and_principles'"
        @activated="updateRoute('#guidelines_and_principles')"
      />
    </b-tabs>
  </div>
</template>

<script>
  import DealEditSection from "components/Deal/DealEditSection";
  import MapEditor from "../../components/MapEditor";
  import { deal_gql_query } from "../../store/queries";
  import { deal_sections } from "./deal_sections";

  export default {
    name: "DealEdit",
    components: { MapEditor, DealEditSection },
    props: {
      dealId: { type: [Number, String], required: true },
      dealVersion: { type: [Number, String], default: null },
    },
    data() {
      return {
        deal: null,
        deal_sections,
      };
    },
    apollo: {
      deal: {
        query: deal_gql_query,
        variables() {
          return {
            id: +this.dealId,
            version: +this.dealVersion,
            subset: this.$store.state.page.user ? "UNFILTERED" : "PUBLIC",
          };
        },
        update(data) {
          if (!data.deal) {
            this.$router.push({
              name: "404",
              params: [this.$router.currentRoute.path],
              replace: true,
            });
          }
          return data.deal;
        },
      },
    },
    computed: {
      active_tab() {
        return location.hash ? location.hash : "#locations";
      },
    },
    methods: {
      updateRoute(emiter) {
        if (location.hash !== emiter) this.$router.push(this.$route.path + emiter);
      },
    },
  };
</script>
