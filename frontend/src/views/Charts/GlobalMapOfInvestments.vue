<template>
  <div class="">
    <div class="row">
      <div class="col-6">
        <p>
          Choose between investor or target countries using the menu below. Click on the
          bubbles to visualise the selected country's involvement in the global land
          acquisition phenomenon.
        </p>
        <div class="current-country" style="display: none;">
          <p><strong>Country</strong></p>
          <p>
            <span class="total-deals">0 acquisitions/targets</span>
            <span class="related-country">to/from Country</span>
            <span class="self-deals">whereof 0 with itself</span>
            <br />
            <b><a href="#">Go to Table</a></b>
          </p>
        </div>
        <div class="btn-group views">
          <a class="btn show-all disabled" href="#">Reset</a>
          <a class="btn active" href="?filter=investor">Investor&nbsp;Countries</a>
          <a class="btn" href="?filter=target">Target&nbsp;Countries</a>
        </div>
      </div>
      <div class="col-6">
        <ul class="legend media-list">
          <li>
            <i class="icon icon-none" style="background-color: #44b7b6;"></i>
            Investor Countries
          </li>
          <li>
            <i class="icon icon-none" style="background-color: #ed881b;"></i>
            Target Countries
          </li>
        </ul>
      </div>
    </div>

    <big-map @ready="pinTheMap">
      <l-geo-json v-if="mapGeojson" :geojson="mapGeojson" />
    </big-map>
  </div>
</template>

<script>
  import store from "@/store";
  import BigMap from "@/components/BigMap";

  let MAP;

  export default {
    components: {
      BigMap,
    },
    data: function () {
      return {
        mapGeojson: null,
      };
    },
    methods: {
      pinTheMap(x) {
        MAP = x;
        console.log(MAP);
        // import vectors from "@/assets/world.min";

        // this.mapGeojson = require('@/assets/countries.geo.json');
      },
    },
    beforeRouteEnter(to, from, next) {
      let title = "Global Map of Investments";
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

<!--  <script type="text/javascript" src="{% static "raphael/raphael-min.js" %}"></script>-->
<!--  <script src="{% static "js/vendor/raphael-svg-import.js" %}" type="text/javascript" charset="utf-8"></script>-->
<!--  <script src="{% static "js/world.min.js" %}" type="text/javascript" charset="utf-8"></script>-->
<!--  <script src="{% static "js/investor-target-countries.js" %}" type="text/javascript" charset="utf-8"></script>-->
<!--  <script type="text/javascript">-->
<!--    function draw(callback) {-->
<!--      drawMap(callback);-->
<!--    }-->

<!--    $(function () {-->
<!--      $(".views .btn").click(function (e) {-->
<!--        var c_self = this;-->
<!--        e.preventDefault();-->
<!--        // Filter button clicked?-->
<!--        if ($(c_self).attr("href").indexOf("filter") > -1) {-->
<!--          $("#map").removeClass("investor").removeClass("target").addClass($(c_self).attr("href").replace("?filter=", ""));-->
<!--          $(".views .active").removeClass("active");-->
<!--          $(c_self).addClass("active");-->
<!--          $(c_self).button('loading');-->
<!--        }-->
<!--        draw(function () {-->
<!--          $(c_self).button('reset');-->
<!--        });-->
<!--        return false;-->
<!--      });-->
<!--      $(".views .btn.active").click();-->
<!--      $(".deal_scope").hide();-->
<!--    });-->
<!--    URL_PREFIX = '/';-->
<!--  </script>-->
