<template>
  <div class="row">
    <div class="col-md-3 font-weight-bold">
      {{ formfield.label }}
    </div>
    <div class="col-md-9">
      <div v-if="readonly">
        <div v-for="val in vals" v-html="parseValues(val)"></div>
      </div>
    </div>
  </div>
</template>

<script>
  import { flatten_choices } from "/utils";

  export default {
    props: ["formfield", "value", "readonly"],
    data() {
      return {
        current: 0,
        vals: [{ date: null, value: null }],
      };
    },
    computed: {},
    methods: {
      addSet() {
        this.vals.push({ date: null, value: null });
      },
      removeSet(index) {
        this.vals.splice(index, 1);
      },
      updateVals() {
        let vals_with_current = this.vals.map((val, i) => {
          let current = i === this.current ? { current: true } : {};
          return { value: val.value, date: val.date, ...current };
        });
        this.$emit("input", vals_with_current);
      },
      parseValues: function (value) {
        let ret = "";
        if (value.date) ret += `<span class="date">[${value.date}]</span> `;

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
    created() {
      if (this.value) {
        this.current = this.value.map((e) => e.current).indexOf(true);
        this.vals = this.value;
      }
    },
  };
</script>
<style lang="scss" scoped>
  @import "../../scss/colors";

  .input-group {
    padding: 0.4em;
  }

  .current-value {
    background: rgba($primary, 0.5);

    &::before {
      content: "Current";
      position: absolute;
      bottom: -5px;
      font-size: 0.7em;
    }
  }

  .multiselect {
    width: 60%;
  }
</style>
<style></style>
