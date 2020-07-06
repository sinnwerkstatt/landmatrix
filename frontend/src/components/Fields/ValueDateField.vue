<template>
  <div>
    <div v-if="readonly">
      {{vals}}
<!--      <div v-for="val in vals">-->
<!--        <span v-if="val.date">[{{ val.date }}]</span> {{ val.value.join(', ') }}<br />-->
<!--      </div>-->
    </div>
    <div v-else>
      <div v-for="(val, i) in vals" :key="i" class="my-1">
        <!--  <div>-->
        <!--    {{formfield}}-->
        <!--  </div>-->
        <div :class="{ 'input-group': true, 'current-value': current === i }">
          <div class="form-check form-check-inline">
            <input
              class="form-check-input"
              type="radio"
              :name="`${formfield.name}_current`"
              :id="`${formfield.name}_current_${i}`"
              :value="i"
              v-model="current"
              @change="updateVals"
            />
          </div>
          <multiselect
            class="multiselect"
            v-if="formfield.multiselect"
            :options="formfield.multiselect.options"
            :multiple="formfield.multiselect.multiple"
            :closeOnSelect="!formfield.multiselect.multiple"
            :group-values="formfield.multiselect.with_categories && 'options'"
            :group-label="formfield.multiselect.with_categories && 'category'"
            :customLabel="(x) => formfield.multiselect.labels[x]"
            :placeholder="formfield.placeholder"
            v-model="val.value"
          />
          <input
            v-else
            :type="formfield.type || `text`"
            :placeholder="formfield.placeholder"
            class="form-control year-based"
            :aria-label="formfield.placeholder"
            v-model="val.value"
            @change="updateVals"
          />
          <div class="input-group-append" v-if="formfield.unit">
            <div class="input-group-text">{{ formfield.unit }}</div>
          </div>
          <input
            type="text"
            class="form-control year-based-year"
            :aria-label="formfield.placeholder"
            placeholder="YYYY-MM-DD"
            v-model="val.date"
            @change="updateVals"
          />
          <a
            :class="{ disabled: vals.length <= 1 }"
            class="btn remove-ybd delete-row"
            @click.prevent="removeSet(i)"
          >
            <i class="lm lm-minus"></i
          ></a>
        </div>
      </div>
      <a class="btn add-ybd add-row" @click.prevent="addSet">
        <i class="lm lm-plus"></i> Add more</a
      >
    </div>
  </div>
</template>

<script>
  export default {
    props: ["formfield", "value", "readonly"],
    data() {
      return {
        current: 0,
        vals: [{ date: null, value: null }],
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
      updateVals() {
        let vals_with_current = this.vals.map((val, i) => {
          let current = i === this.current ? { current: true } : {};
          return { value: val.value, date: val.date, ...current };
        });
        this.$emit("input", vals_with_current);
      },
    },
    created() {
      if (this.value) {
        this.current = this.value.map((e) => e.current).indexOf(true);
        this.vals = this.value;
      }
    },
  };
</script>
<style lang="scss" scoped>
  @import "../../scss/colors";

  .input-group {
    padding: 0.4em;
  }

  .current-value {
    background: rgba($primary, 0.5);

    &::before {
      content: "Current";
      position: absolute;
      bottom: -5px;
      font-size: 0.7em;
    }
  }

  .multiselect {
    width: 60%;
  }
</style>
<style></style>
