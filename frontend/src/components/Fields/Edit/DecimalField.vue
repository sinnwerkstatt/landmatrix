<template>
  <div>
    <div class="input-group">
      <input
        type="text"
        class="form-control"
        aria-describedby="validatedInputGroupPrepend"
        :value="value"
        :required="formfield.required"
      />
      <div v-if="formfield.help_text" class="input-group-append">
        <span id="validatedInputGroupPrepend" class="input-group-text">
          {{ formfield.help_text }}
        </span>
      </div>
    </div>
  </div>
</template>

<script>
  export default {
    props: {
      formfield: { type: Object, required: true },
      value: { type: Number, required: true },
      model: { type: String, required: true },
    },
  };
</script>
