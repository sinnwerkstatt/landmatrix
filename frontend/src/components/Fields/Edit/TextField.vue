<template>
  <div>
    <div class="input-group">
      <!--        :id="`type-${formfield.name}`"-->
      <textarea
        v-if="formfield.class === 'TextField'"
        :placeholder="formfield.placeholder || formfield.label"
        :aria-label="formfield.placeholder || formfield.label"
        :value="value"
        :name="formfield.name"
        rows="5"
        class="form-control"
        @input="emitVal"
      />
      <div v-else-if="formfield.choices">
        <select
          :value="value"
          :name="formfield.name"
          class="form-control"
          @input="emitVal"
        >
          <option v-if="!formfield.required" value=""></option>
          <option v-for="(v, k) in formfield.choices" :key="k" :value="k">
            {{ v }}
          </option>
        </select>
      </div>
      <input
        v-else
        :type="formfield.type || `text`"
        :placeholder="formfield.placeholder || formfield.label"
        :aria-label="formfield.placeholder || formfield.label"
        :value="value"
        :name="formfield.name"
        class="form-control"
        @input="emitVal"
      />
    </div>
    <!--      <div v-if="formfield.unit" class="input-group-append">-->
    <!--        <span class="input-group-text">{{ formfield.unit }}</span>-->
    <!--      </div>-->
  </div>
</template>

<script>
  export default {
    props: {
      formfield: { type: Object, required: true },
      value: { type: String, required: false, default: "" },
      model: { type: String, required: true },
    },
    methods: {
      emitVal() {
        this.$emit("input", this.val);
      },
    },
  };
</script>
