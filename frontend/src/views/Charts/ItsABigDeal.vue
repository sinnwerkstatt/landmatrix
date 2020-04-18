<template>
  <div class="">
    <big-map @ready="pinTheMap" :center="latlng">
      <l-circle
        :radius="radius"
        :lat-lng="latlng"
        color="#fc941f"
        fillColor="#fc941f"
        @ready="makeCircleDraggable"
      >
        <l-tooltip>{{ hectares }} ha</l-tooltip>
      </l-circle>
    </big-map>
  </div>
</template>

<script>
  import store from "@/store";
  import BigMap from "@/components/BigMap";
  import { LCircle, LTooltip } from "vue2-leaflet";

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
      };
    },
    computed: {
      hectares() {
        return 160168350;
      },
      radius() {
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
