<template>
  <div>
    <div v-for="val in vals">
      <!--  <div>-->
      <!--    {{formfield}}-->
      <!--  </div>-->
      <b-input-group :append="formfield.unit">
        <b-form-input
          :id="`type-${formfield.class}`"
          :type="formfield.type || `text`"
          :placeholder="formfield.placeholder"
          class="year-based"
        />
        <b-form-input
          :id="`type-${formfield.class}_date`"
          type="text"
          class="year-based-year"
          placeholder="YYYY-MM-DD"
        />
      </b-input-group>
      <a class="btn add-ybd add-row" :click="addSet">
        <i class="lm lm-plus"></i> Add more</a
      >
      <a class="btn remove-ybd delete-row" style="display: none;">
        <i class="lm lm-minus"></i> Remove</a
      >
    </div>
  </div>
</template>

<script>
  export default {
    props: ["formfield", "value"],
    data() {
      return {
        sets: [{ date: null, value: null }],
      };
    },
    computed: {
      //   vals: {
      //     get() {
      //       console.log(this.value[this.formfield.class]);
      //       return this.value[this.formfield.class];
      //     },
      //     set(value) {
      //       console.log(value);
      //       // this.$emit('input', value)
      //     }
      //   }
    },
    methods: {
      addSet() {
        this.sets.append({ date: null, value: null });
      },
    },
  };
</script>
