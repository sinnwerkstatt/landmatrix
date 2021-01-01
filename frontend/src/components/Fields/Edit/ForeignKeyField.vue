<template>
  <div>
    <select v-model="val" class="form-control">
      <option v-for="choice in choices" :key="choice.id" :value="choice.id">
        {{ choice.name }}
      </option>
    </select>
  </div>
</template>

<script>
  import gql from "graphql-tag";

  export default {
    props: {
      formfield: { type: Object, required: true },
      value: { type: Object, required: true },
      model: { type: String, required: true },
    },
    data() {
      return {
        currencies: [],
      };
    },
    apollo: {
      currencies: gql`
        query {
          currencies {
            id
            name
          }
        }
      `,
    },
    computed: {
      val: {
        get() {
          return this.value.id;
        },
        set(v) {
          this.$emit("input", v);
        },
      },

      choices() {
        let options = {
          Country: this.$store.state.page.countries,
          Currency: this.currencies,
        };
        return options[this.formfield.related_model];
      },
    },
  };
</script>
