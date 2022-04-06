<script>
  import JSONFieldMixin from "../JSONFieldMixin";
  import { date_and_current } from "$components/Fields/Display/jsonHelpers.ts";

  export default {
    mixins: [JSONFieldMixin],
    data() {
      return {
        vals: this.value ? this.value : [{ date: null, value: null }],
      };
    },
  };
</script>

<div class="jsondatearea_field whitespace-nowrap">
  {#each vals as val}
    <div class={() => (val.current ? "font-weight-bold" : "")}>
      <span>{date_and_current(val)}</span>
      {#if val.area}
        {val.area.toLocaleString("fr")}} ha
      {/if}
    </div>
  {/each}
</div>
