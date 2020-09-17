<template>
  <div class="form-field row">
    <div class="label" :class="labelClasses">
      {{ formfield.label }}
    </div>
    <div class="val" :class="valClasses">
      <div v-if="readonly">
        {{ val }}
      </div>
    </div>
  </div>
</template>

<script>
  import {fieldMixin} from "./fieldMixin";

  export default {
    mixins: [fieldMixin],
  };
</script>
