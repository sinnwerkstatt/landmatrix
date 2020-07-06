<template>
  <div class="container">
    <div>In total: {{ hectares.toLocaleString() }}ha in {{ deals_count }} deals.</div>
    <big-map @ready="pinTheMap" :center="latlng">
      <l-circle
        v-if="hectares"
        :radius="radius"
        :lat-lng="latlng"
        color="#fc941f"
        fillColor="#fc941f"
        @ready="makeCircleDraggable"
      >
        <l-tooltip>{{ hectares.toLocaleString() }} ha</l-tooltip>
      </l-circle>
    </big-map>
  </div>
</template>

<script>
  import store from "/store";
  import BigMap from "/components/BigMap";
  import { LCircle, LTooltip } from "vue2-leaflet";
  import axios from "axios";

  let MAP;

  export default {
    name: "Charts",
    components: {
      BigMap,
      LCircle,
      LTooltip,
    },
    data: function () {
      return {
        latlng: [40.416775, -3.70379],
        hectares: null,
        deals_count: null,
      };
    },
    computed: {
      radius() {
        if (!this.hectares) return null;
        return Math.sqrt((this.hectares * 10000) / Math.PI);
      },
    },
    methods: {
      makeCircleDraggable(circle) {
        circle.on({
          mousedown: function () {
            MAP.dragging.disable();
            MAP.on("mousemove", function (e) {
              circle.setLatLng(e.latlng);
            });
          },
        });
        MAP.on("mouseup", function (e) {
          MAP.removeEventListener("mousemove");
          MAP.dragging.enable();
        });
      },
      pinTheMap(x) {
        MAP = x;
      },
    },
    created() {
      let query = `{ deals(limit: 0) { deal_size } }`;
      axios.post("/graphql/", { query: query }).then((response) => {
        this.deals_count = response.data.data.deals.length;
        this.hectares = response.data.data.deals.reduce((num, d) => {
          return d.deal_size + num;
        }, 0);
      });
    },
    beforeRouteEnter(to, from, next) {
      let title = "It's a big deal";
      store.dispatch("setPageContext", {
        title: title,
        breadcrumbs: [
          { link: { name: "wagtail" }, name: "Home" },
          { link: { name: "charts" }, name: "Charts" },
          { name: title },
        ],
      });
      next();
    },
  };
</script>

<style scoped></style>
