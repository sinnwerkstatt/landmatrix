<template>
  <div>
    <div id="stats">
      <div class="row">
        <div class="col-sm-12">
          <h3>
            We currently have information about:
            <a
              class="toggle-tooltip bottom"
              href="/faq/#what-is-a-land-deal"
              data-original-title=""
              title=""
              ><i class="icon icon-question-sign"></i
            ></a>
          </h3>
        </div>
      </div>
      <div class="row">
        <div class="col-sm-6">
          <h4>Size</h4>
          <p class="number number-concluded">0 ha</p>
          <div class="progress progress-concluded">
            <div class="bar" style="width: 0"></div>
          </div>
          <p class="percentage percentage-concluded">0%</p>
          <p class="number number-intended">0 ha</p>
          <div class="progress progress-intended">
            <div class="bar" style="width: 0"></div>
          </div>
          <p class="percentage percentage-intended">0%</p>
          <p class="number number-failed">0 ha</p>
          <div class="progress progress-failed">
            <div class="bar" style="width: 0"></div>
          </div>
          <p class="percentage percentage-failed">0%</p>
        </div>
        <div class="col-sm-6">
          <h4>No of deals</h4>
          <p class="number number-concluded">0</p>
          <div class="progress progress-concluded">
            <div class="bar" style="width: 0"></div>
          </div>
          <p class="percentage percentage-concluded">0%</p>
          <p class="number number-intended">0</p>
          <div class="progress progress-intended">
            <div class="bar" style="width: 0"></div>
          </div>
          <p class="percentage percentage-intended">0%</p>
          <p class="number number-failed">0</p>
          <div class="progress progress-failed">
            <div class="bar" style="width: 0"></div>
          </div>
          <p class="percentage percentage-failed">0%</p>
        </div>
      </div>
      <div class="well-square legend">
        <ul class="list-inline">
          <li>
            <i class="icon icon-none" style="background-color: #ed881b"></i>
            Concluded
          </li>
          <li>
            <i class="icon icon-none" style="background-color: #b96c12"></i>
            Intended
          </li>
          <li>
            <i class="icon icon-none" style="background-color: #884e0e"></i>
            Failed
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
  export default {};
</script>

<style>
  .icon-none {
    width: 14px;
    height: 14px;
    display: inline-block;
    border: 1px solid #c1c1c1;
  }
</style>
<!--<script type="text/javascript">-->
<!--      $(document).ready(function () {-->
<!--        $.get(-->
<!--          "/api/statistics.json?disable_filters=1{% if country %}&country={{ country.id }}{% elif region %}&region={{ region.id }}{% endif %}",-->
<!--          function (data) {-->
<!--            var stats = $("#stats"),-->
<!--              size = stats.find(".size"),-->
<!--              deals = stats.find(".deals"),-->
<!--              by_deals = [0, 0, 0, 0],-->
<!--              by_size = [0, 0, 0, 0],-->
<!--              item;-->
<!--            for (var i = 0; i < data.length; i++) {-->
<!--              item = data[i];-->
<!--              // Update numbers-->
<!--              // Concluded-->
<!--              if (["Oral agreement", "Contract signed"].indexOf(item[0]) > -1) {-->
<!--                by_deals[1] += item[1];-->
<!--                by_size[1] += item[2];-->
<!--                // Intended-->
<!--              } else if (-->
<!--                [-->
<!--                  "Expression of interest",-->
<!--                  "Under negotiation",-->
<!--                  "Memorandum of understanding",-->
<!--                ].indexOf(item[0]) > -1-->
<!--              ) {-->
<!--                by_deals[2] += item[1];-->
<!--                by_size[2] += item[2];-->
<!--                // Failed-->
<!--              } else if (-->
<!--                [-->
<!--                  "Negotiations failed",-->
<!--                  "Contract canceled",-->
<!--                  "Contract expired",-->
<!--                ].indexOf(item[0]) > -1-->
<!--              ) {-->
<!--                by_deals[3] += item[1];-->
<!--                by_size[3] += item[2];-->
<!--              }-->
<!--              // Update totals-->
<!--              by_deals[0] += item[1];-->
<!--              by_size[0] += item[2];-->
<!--            }-->
<!--            // Update by size-->
<!--            size.find(".number-concluded").text(numberWithCommas(by_size[1]) + " ha");-->
<!--            percentage =-->
<!--              (by_size[0] > 0 && Math.round((by_size[1] / by_size[0]) * 100)) || 0;-->
<!--            size.find(".progress-concluded .bar").css("width", percentage + "%");-->
<!--            size.find(".percentage-concluded").text(percentage + "%");-->
<!--            size.find(".number-intended").text(numberWithCommas(by_size[2]) + " ha");-->
<!--            percentage =-->
<!--              (by_size[0] > 0 && Math.round((by_size[2] / by_size[0]) * 100)) || 0;-->
<!--            size.find(".progress-intended .bar").css("width", percentage + "%");-->
<!--            size.find(".percentage-intended").text(percentage + "%");-->
<!--            size.find(".number-failed").text(numberWithCommas(by_size[3]) + " ha");-->
<!--            percentage =-->
<!--              (by_size[0] > 0 && Math.round((by_size[3] / by_size[0]) * 100)) || 0;-->
<!--            size.find(".progress-failed .bar").css("width", percentage + "%");-->
<!--            size.find(".percentage-failed").text(percentage + "%");-->

<!--            // Update by deals-->
<!--            deals.find(".number-concluded").text(numberWithCommas(by_deals[1]));-->
<!--            percentage =-->
<!--              (by_deals[0] > 0 && Math.round((by_deals[1] / by_deals[0]) * 100)) || 0;-->
<!--            deals.find(".progress-concluded .bar").css("width", percentage + "%");-->
<!--            deals.find(".percentage-concluded").text(percentage + "%");-->
<!--            deals.find(".number-intended").text(numberWithCommas(by_deals[2]));-->
<!--            percentage =-->
<!--              (by_deals[0] > 0 && Math.round((by_deals[2] / by_deals[0]) * 100)) || 0;-->
<!--            deals.find(".progress-intended .bar").css("width", percentage + "%");-->
<!--            deals.find(".percentage-intended").text(percentage + "%");-->
<!--            deals.find(".number-failed").text(numberWithCommas(by_deals[3]));-->
<!--            percentage =-->
<!--              (by_deals[0] > 0 && Math.round((by_deals[3] / by_deals[0]) * 100)) || 0;-->
<!--            deals.find(".progress-failed .bar").css("width", percentage + "%");-->
<!--            deals.find(".percentage-failed").text(percentage + "%");-->
<!--          }-->
<!--        );-->
<!--      });-->
<!--    </script>-->
