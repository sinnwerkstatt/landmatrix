<template>
  <div>
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
      <div v-else-if="formfield.choices">
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
        :type="formfield.type || `text`"
        :placeholder="formfield.placeholder || formfield.label"
        :aria-label="formfield.placeholder || formfield.label"
        :name="formfield.name"
        class="form-control"
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
