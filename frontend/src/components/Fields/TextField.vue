<template>
  <div class="form-field row">
    <div class="label" :class="labelClasses">
      {{ formfield.label }}
    </div>
    <div class="val" :class="valClasses">
      <div v-if="readonly">
        <template v-if="formfield.type === 'url'">
          <a :href="val" target="_blank">{{ val }}</a>
        </template>
        <template v-else>
          {{ parseVal(val) }}
        </template>
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
  </div>
</template>

<script>
  import { flatten_choices } from "/utils";
  import { fieldMixin } from "./fieldMixin";
  import { parseFormFieldValue } from "./fieldHelpers";

  export default {
    mixins: [fieldMixin],
    methods: {
      parseVal(val) {
        return parseFormFieldValue(this.formfield, val);
      },
    },
  };
</script>
