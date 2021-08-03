<template>
  <div class="goals-table">
    <table class="goals">
      <!--<tr><th></th><th colspan="2">Public</th><th></th><th colspan="2">Globald default</th></tr>-->
      <tr>
        <td></td>
        <th>Count</th>
        <th>Ratio</th>
        <td></td>
        <td><!--Count--></td>
        <td><!--Ratio--></td>
        <td></td>
      </tr>
      <tr>
        <th class="label">Publicly visible deals<sup class="tiny">1</sup></th>
        <td>{{ goal_statistics.deals_public_count }}</td>
        <td></td>
        <td></td>
        <td></td>
        <td></td>
      </tr>
      <tr>
        <th class="label">Deals with with multiple data sources</th>
        <td>{{ goal_statistics.deals_public_multi_ds_count }}</td>
        <td>
          {{
            percentRatio(
              goal_statistics.deals_public_multi_ds_count,
              goal_statistics.deals_public_count
            )
          }}
        </td>
        <td></td>
        <td></td>
        <td></td>
      </tr>
      <tr>
        <th class="label">
          Deals georeferenced with high accuracy<sup class="tiny">2</sup>
        </th>
        <td>{{ goal_statistics.deals_public_high_geo_accuracy }}</td>
        <td>
          {{
            percentRatio(
              goal_statistics.deals_public_high_geo_accuracy,
              goal_statistics.deals_public_count
            )
          }}
        </td>
        <td></td>
        <td></td>
        <td></td>
      </tr>
      <tr>
        <th class="label">Deals with polygon data</th>
        <td>{{ goal_statistics.deals_public_polygons }}</td>
        <td>
          {{
            percentRatio(
              goal_statistics.deals_public_polygons,
              goal_statistics.deals_public_count
            )
          }}
        </td>
        <td></td>
        <td></td>
        <td></td>
      </tr>
    </table>
    <p class="small mt-3">
      <sup>1</sup> Active deals with public filter ok, not confidential.<br />
      <sup>2</sup> Deals with at least one location with either accuracy level
      'Coordinates' or 'Exact location' or at least one polygon.
    </p>
  </div>
</template>

<script>
  export default {
    name: "GoalsTable",
    props: {
      goalStatistics: { type: Object, required: true },
    },
    methods: {
      percentRatio(partialValue, totalValue) {
        if (totalValue) {
          let ratio = ((100 * partialValue) / totalValue).toFixed(1);
          return `${ratio} %`;
        }
        return "";
      },
    },
  };
</script>

<style lang="scss" scoped>
  table.goals {
    th,
    td {
      padding: 0.3em;
    }

    th {
      text-align: center;
      white-space: nowrap;

      &.label {
        text-align: left;
      }
    }

    td {
      text-align: right;
      padding: 0.3em 1.5em;
    }
  }
</style>
