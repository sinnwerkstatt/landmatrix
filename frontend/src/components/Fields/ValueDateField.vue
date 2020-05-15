<template>
  <div>
    <div v-for="(val, i) in vals" :key="i" class="my-1">
      <!--  <div>-->
      <!--    {{formfield}}-->
      <!--  </div>-->
      <div class="input-group">
        <input
          :type="formfield.type || `text`"
          :placeholder="formfield.placeholder"
          class="form-control year-based"
          :aria-label="formfield.placeholder"
          v-model="val.value"
          @input="emitVals"
        />
        <div class="input-group-append">
          <div class="input-group-text">{{ formfield.unit }}</div>
        </div>
        <input
          type="text"
          class="form-control year-based-year"
          :aria-label="formfield.placeholder"
          placeholder="YYYY-MM-DD"
          v-model="val.date"
          @input="emitVals"
        />
        <div class="form-check form-check-inline">
          <input
            class="form-check-input"
            type="radio"
            :name="`${formfield.name}_current`"
            :id="`${formfield.name}_current_${i}`"
            :value="i"
            v-model="current"
            @input="emitVals"
          />
          <label class="form-check-label" :for="`${formfield.name}_current_${i}`">
            Current
          </label>
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
        current: null,
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
        let vals_with_current = this.vals;
        if(this.current)
          vals_with_current[this.current].current = true;
        this.$emit("input", vals_with_current);
      },
    },
  };
</script>
