<template>
  <div>
    <div v-if="readonly">
      {{ parseVal(val) }}
    </div>
    <div v-else class="input-group">
      <input
        v-if="!formfield.multiline"
        :id="`type-${formfield.name}`"
        :type="formfield.type || `text`"
        class="form-control"
        :placeholder="formfield.placeholder || formfield.label"
        :aria-label="formfield.placeholder || formfield.label"
        v-model="val"
        @input="emitVal"
      />
      <textarea
        v-else
        rows="5"
        :id="`type-${formfield.name}`"
        class="form-control"
        :placeholder="formfield.placeholder || formfield.label"
        :aria-label="formfield.placeholder || formfield.label"
        v-model="val"
        @input="emitVal"
      />
      <div v-if="formfield.unit" class="input-group-append">
        <span class="input-group-text">{{ formfield.unit }}</span>
      </div>
    </div>
  </div>
</template>

<script>
  import {flatten_choices} from "/utils";

  export default {
    props: ["formfield", "value", "readonly"],
    data() {
      return {
        val: this.value,
      };
    },
    methods: {
      emitVal() {
        this.$emit("input", this.val);
      },
      parseVal(val) {
        let choices = flatten_choices(this.formfield.choices);
        if (choices) return choices[val];
        else return val;
      },
    },
  };
</script>
