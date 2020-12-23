<template>
  <div class="jsonfield">
    <div v-for="val in vals" :class="{ 'is-current': val.current }">
      <span v-if="val.date || val.current" v-html="date_and_current(val)" />

      <span v-html="parseValues(val)" />
      <span class="mx-2" v-if="val.hectares">
        <i class="fas fa-circle-notch"></i> {{ val.hectares }} ha
      </span>
      <span class="mx-2" v-if="val.tons">
        <i class="fas fa-weight-hanging"></i> {{ val.tons }} tons
      </span>
      <span class="mx-2" v-if="val.percent">
        <i class="fas fa-plane-departure"></i> {{ val.percent }} %
      </span>
    </div>
  </div>
</template>

<script>
  import { flatten_choices } from "utils";

  export default {
    props: ["formfield", "value", "model"],
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
        // if (value.date) ret += `<span class="date">[${value.date}]</span> `;

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
