<template>
  <div class="form-field row">
    <div class="label" :class="labelClasses">
      {{ formfield.label }}
    </div>
    <div class="val" :class="valClasses">
      <div v-for="val in vals" :class="{ 'is-current': val.current }">
        <span v-if="val.date || val.current">
          [
          <span v-if="val.date">{{ val.date }}</span>
          <span v-if="val.date && val.current">,</span>
          <span v-if="val.current">current</span>
          ]
        </span>
        <span class="" v-html="parseValues(val)"></span>
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
  </div>
</template>

<script>
  import { flatten_choices } from "/utils";
  import { fieldMixin } from "./fieldMixin";

  export default {
    mixins: [fieldMixin],
    data() {
      return {
        current: 0,
        vals: [{ date: null, value: null }],
      };
    },
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
  .is-current {
    font-weight: bold;
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
