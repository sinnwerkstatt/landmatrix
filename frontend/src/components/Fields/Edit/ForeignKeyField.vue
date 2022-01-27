<!-- this field is only used for Currency at the moment-->
<template>
  <div>
    <div>
      <multiselect
        v-model="val"
        :options="currencies"
        label="name"
        select-label=""
        :custom-label="(mdl) => `${mdl.name} (${mdl.code})`"
        track-by="id"
        :allow-empty="!formfield.required"
      />
    </div>
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
    },
    computed: {
      val: {
        get() {
          return this.value;
        },
        set(v) {
          let em = v ? { id: v.id, name: v.name, code: v.code } : null;
          this.$emit("input", em);
        },
      },
    },
  };
</script>
