<template>
  <div>
    <div @mouseover="showHint = true" @mouseout="showHint = false">
      <multiselect
        v-model="val"
        :options="target_countries"
        label="name"
        track-by="id"
        :allow-empty="!formfield.required"
        :disabled="disabled"
      />
      <span v-if="disabled && showHint" class="hint">
        You can only change the country when no locations are defined.
      </span>
    </div>
  </div>
</template>

<script>
  export default {
    props: {
      formfield: { type: Object, required: true },
      value: { type: Object, required: false, default: null },
      model: { type: String, required: true },
      disabled: { type: Boolean, default: false },
    },
    data() {
      return {
        showHint: false,
      };
    },
    computed: {
      val: {
        get() {
          return this.value;
        },
        set(v) {
          this.$emit("input", {
            id: v.id,
            name: v.name,
            code_alpha2: v.code_alpha2,
            point_lat_min: v.point_lat_min,
            point_lat_max: v.point_lat_max,
            point_lon_min: v.point_lon_min,
            point_lon_max: v.point_lon_max,
          });
        },
      },
      target_countries() {
        let countries = this.$store.state.countries;
        if (this.model !== "investor")
          countries = countries.filter((c) => !c.high_income);
        return countries;
      },
    },
  };
</script>
<style scoped>
  .hint {
    position: absolute;
    color: grey;
    font-size: 0.9rem;
  }
</style>
