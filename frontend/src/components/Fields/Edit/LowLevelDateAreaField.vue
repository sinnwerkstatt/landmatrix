<template>
  <tr>
    <td>
      <input
        :value="val.date"
        type="text"
        class="form-control year-based-year"
        placeholder="YYYY-MM-DD"
      />
    </td>
    <td>
      <LowLevelDecimalField
        :value="val.area"
        :name="formfield.name"
        :required="formfield.required"
        unit="ha"
      />
    </td>

    <td>
      <a class="btn" @click.prevent="addEntry"><i class="fa fa-plus"></i></a>
      <a
        :class="{ disabled: vals.length <= 1 }"
        class="btn"
        @click.prevent="removeEntry(i)"
      >
        <i class="fa fa-minus"></i
      ></a>
    </td>
  </tr>
</template>

<script>
  import JSONFieldMixin from "../JSONFieldMixin";
  import LowLevelDecimalField from "./LowLevelDecimalField";
  export default {
    components: { LowLevelDecimalField },
    mixins: [JSONFieldMixin],
    data() {
      return {
        current: -1,
        vals: this.value
          ? JSON.parse(JSON.stringify(this.value))
          : [{ date: null, area: null, current: true }],
      };
    },
    // watch: {
    //   // value() {
    //   //   this.vals = JSON.parse(JSON.stringify(this.value));
    //   // },
    //   current() {
    //     this.updateEntries();
    //   },
    //   vals: {
    //     handler(newValue, oldValue) {
    //       if (newValue !== oldValue) {
    //         this.updateEntries(newValue);
    //       }
    //     },
    //     deep: true,
    //   },
    // },
    // created() {
    //   if (this.value) {
    //     this.current = this.value.map((e) => e.current).indexOf(true);
    //   }
    // },
    // methods: {
    //   updateEntries(vals) {
    //     let relevant_val = vals ? vals : this.vals;
    //     // console.log(this.current);
    //     let vals_with_current = relevant_val.map((v, i) => {
    //       let current = i === this.current ? { current: true } : {};
    //       delete v.current;
    //       return { ...v, ...current };
    //     });
    //     this.$emit("input", vals_with_current);
    //   },
    //   addEntry() {
    //     // this.current = this.vals.length;
    //     this.vals.push({ date: null, area: null });
    //     // console.log(this.vals.length);
    //     // console.log(this.current);
    //   },
    //   removeEntry(index) {
    //     this.vals.splice(index, 1);
    //   },
    // },
  };
</script>

<style lang="scss" scoped>
  @import "../../../scss/colors";

  td {
    padding: 0.4em;
  }

  .is-current {
    font-weight: bold;
    background: rgba($primary, 0.5);
    border-radius: 3px;
  }
</style>
