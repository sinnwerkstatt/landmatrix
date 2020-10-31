<template>
  <div class="form-field row">
    <div class="label" :class="labelClasses">
      {{ formfield.label }}
    </div>
    <div class="val" :class="valClasses">
      <div v-if="readonly">
        <span v-if="val">
          Yes
        </span>
        <span v-else-if="val === false">
          No
        </span>
        <span v-else>
          NULL
        </span>
      </div>
    </div>
  </div>
</template>

<script>
  import { fieldMixin } from "./fieldMixin";

  export default {
    mixins: [fieldMixin],
  };
</script>
