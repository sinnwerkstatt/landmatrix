<template>
  <div class="">
    <big-map>
      <l-circle
          :radius="radius"
          :lat-lng="latlng"
          color="rgba(237, 136, 27, 1)"
          fillColor="rgba(237, 136, 27, 0.8)"
          @ready="mymethod"
      />
    </big-map>
  </div>
</template>

<script>
  import store from "@/store";
  import BigMap from "@/components/BigMap";
  import {LCircle} from "vue2-leaflet";


  export default {
    name: "Charts",
    components: {
      BigMap,
      LCircle
    },
    data: function () {
      return {
        latlng: [40.416775, -3.703790],
      }
    },
    computed: {
      radius() {
        let hectares = 160168350;
        return Math.sqrt((hectares * 10000) / Math.PI);
      }
    },
    methods: {
      mymethod(x) {
        // x.on({
        //   mousedown: function () {
        //     map.on('mousemove', function (e) {
        //       circle.setLatLng(e.latlng);
        //     });
        //   }
        // });
        console.log(x);
        console.log(this)
      }
    },
    beforeRouteEnter(to, from, next) {
      let title = "It's a big deal";
      store.dispatch("setPageContext", {
        title: title,
        breadcrumbs: [
          {link: {name: "wagtail"}, name: "Home"},
          {link: {name: "charts"}, name: "Charts"},
          {name: title},
        ],
      });
      next();
    },
  };
</script>

<style scoped></style>
