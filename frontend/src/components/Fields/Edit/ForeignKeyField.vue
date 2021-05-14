<template>
  <div>
    <multiselect
      v-model="val"
      :options="choices"
      label="name"
      :custom-label="fancyName"
      track-by="id"
    />
  </div>
</template>

<script>
  import gql from "graphql-tag";

  export default {
    props: {
      formfield: { type: Object, required: true },
      value: { type: Object, required: false, default: null },
      model: { type: String, required: true },
    },
    data() {
      return {
        currencies: [],
        investors: [],
      };
    },
    apollo: {
      currencies: gql`
        query {
          currencies {
            id
            name
            code
          }
        }
      `,
      investors: gql`
        query {
          investors(sort: "name", limit: 0) {
            id
            name
          }
        }
      `,
    },
    computed: {
      val: {
        get() {
          return this.value;
        },
        set(v) {
          let ret = { id: v.id, name: v.name };
          if (this.formfield.related_model === "Currency") ret["code"] = v.code;
          this.$emit("input", ret);
        },
      },

      choices() {
        let options = {
          Country: this.$store.state.page.countries,
          Currency: this.currencies,
          Investor: this.investors,
        };
        return options[this.formfield.related_model];
      },
    },
    methods: {
      fancyName(model) {
        switch (this.formfield.related_model) {
          case "Investor":
            return `${model.name} (#${model.id})`;
          case "Currency":
            return `${model.name} (${model.code})`;
          default:
            return model.name;
        }
      },
    },
  };
</script>
