<template>
  <div class="form-field row">
    <div class="label" :class="labelClasses">
      {{ formfield.label }}
    </div>
    <div class="val" :class="valClasses">
      <div v-if="readonly">
        {{ parseValues(val) }}
      </div>
    </div>
  </div>
</template>

<script>
  import { flatten_choices } from "/utils";
  import { fieldMixin } from "./fieldMixin";

  export default {
    mixins: [fieldMixin],
    methods: {
      parseValues: function (value) {
        let ret = "";

        let choices = flatten_choices(this.formfield.choices);

        if (value instanceof Array) {
          if (choices) {
            ret += value.map((v) => choices[v]).join(", ");
          } else ret += value.join(", ");
        } else {
          if (choices) ret += choices[value];
          else ret += value;
        }
        return ret;
      },
    },
  };
</script>
