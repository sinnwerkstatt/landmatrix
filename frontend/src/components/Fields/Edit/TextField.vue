<template>
  <div class="text_field">
    <div class="input-group">
      <!--        :id="`type-${formfield.name}`"-->
      <textarea
        v-if="formfield.class === 'TextField'"
        v-model="val"
        :placeholder="formfield.placeholder || formfield.label"
        :aria-label="formfield.placeholder || formfield.label"
        :name="formfield.name"
        rows="5"
        class="form-control"
      />
      <div v-else-if="formfield.choices" class="select">
        <select v-model="val" :name="formfield.name" class="form-control">
          <option v-if="!formfield.required" :value="null">--------</option>
          <option v-for="(v, k) in formfield.choices" :key="k" :value="k">
            {{ v }}
          </option>
        </select>
      </div>
      <input
        v-else
        v-model="val"
        :type="formfield.class === 'URLField' ? 'url' : formfield.type || 'text'"
        :placeholder="formfield.placeholder || formfield.label"
        :aria-label="formfield.placeholder || formfield.label"
        :name="formfield.name"
        class="form-control validitychecker"
        :maxlength="formfield.max_length"
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
    computed: {
      val: {
        get() {
          return this.value;
        },
        set(v) {
          this.$emit("input", v);
        },
      },
    },
  };
</script>

<style scoped>
  .validitychecker:invalid {
    border-color: #dc3545;
    background-position: right calc(0.375em + 0.1875rem) center;
    background-repeat: no-repeat;
    background-size: calc(0.75em + 0.375rem) calc(0.75em + 0.375rem);
    background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' fill='none' stroke='%23dc3545' viewBox='0 0 12 12'%3e%3ccircle cx='6' cy='6' r='4.5'/%3e%3cpath stroke-linejoin='round' d='M5.8 3.6h.4L6 6.5z'/%3e%3ccircle cx='6' cy='8.2' r='.6' fill='%23dc3545' stroke='none'/%3e%3c/svg%3e");
  }
</style>
