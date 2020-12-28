<template>
  <div class="jsonfield">
    <div v-for="val in vals" :class="{ 'is-current': val.current }">
      <span v-if="val.date || val.current">{{ date_and_current(val) }}</span>

      <span>{{ parseValues(val) }}</span>
      <span v-if="val.hectares" class="mx-2">
        <i class="fas fa-circle-notch"></i> {{ val.hectares }} ha
      </span>
      <span v-if="val.tons" class="mx-2">
        <i class="fas fa-weight-hanging"></i> {{ val.tons }} tons
      </span>
      <span v-if="val.percent" class="mx-2">
        <i class="fas fa-plane-departure"></i> {{ val.percent }} %
      </span>
      <span v-if="val.role" class="mx-2">
        <i class="fas fa-bullhorn"></i> {{ val.role }}
      </span>
    </div>
  </div>
</template>

<script>
  import { flatten_choices } from "utils";

  export default {
    props: {
      formfield: { type: Object, required: true },
      value: { type: [Array, Object], required: true },
      model: { type: String, required: true },
    },
    data() {
      return {
        vals: this.value ? this.value : [{ date: null, value: null }],
      };
    },
    methods: {
      date_and_current(val) {
        let ret = "[";
        if (val.date) ret += val.date;
        if (val.date && val.current) ret += ", ";
        if (val.current) ret += this.$t("current");
        ret += "]";
        return ret;
      },
      parseValues: function (value) {
        let ret = "";
        let choices = flatten_choices(this.formfield.choices);

        if (value.value instanceof Array) {
          if (choices) {
            ret += value.value.map((v) => choices[v]).join(", ");
          } else ret += value.value.join(", ");
        } else {
          if (choices) ret += choices[value.value];
          else ret += value.value;
        }
        return ret;
      },
    },
  };
</script>
<style lang="scss" scoped>
  .jsonfield {
    white-space: nowrap;
  }
  .is-current {
    font-weight: bold;
  }
</style>
