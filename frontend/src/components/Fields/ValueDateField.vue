<template>
  <div>
    <div v-for="(val, i) in vals" :key="i" class="my-1">
      <!--  <div>-->
      <!--    {{formfield}}-->
      <!--  </div>-->
      <div class="input-group">
        <b-form-input
          :type="formfield.type || `text`"
          :placeholder="formfield.placeholder"
          class="year-based"
          v-model="val.value"
          @input="emitVals"
        />
        <b-form-input
          type="text"
          class="year-based-year"
          placeholder="YYYY-MM-DD"
          v-model="val.date"
          @input="emitVals"
        />
        <div class="input-group-append">
          <div class="input-group-text">{{ formfield.unit }}</div>
        </div>
        <a
          :class="{ disabled: vals.length <= 1 }"
          class="btn remove-ybd delete-row"
          @click.prevent="removeSet(i)"
        >
          <i class="lm lm-minus"></i> Remove</a
        >
      </div>
    </div>
    <a class="btn add-ybd add-row" @click.prevent="addSet">
      <i class="lm lm-plus"></i> Add more</a
    >
  </div>
</template>

<script>
  export default {
    props: ["formfield", "value"],
    data() {
      return {
        vals: this.value || [{ date: null, value: null }],
      };
    },
    computed: {},
    methods: {
      addSet() {
        this.vals.push({ date: null, value: null });
      },
      removeSet(index) {
        this.vals.splice(index, 1);
      },
      emitVals() {
        this.$emit("input", this.vals);
      }
    },
  };
</script>
