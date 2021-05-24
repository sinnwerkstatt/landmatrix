<template>
  <div>
    <div>
      <multiselect
        v-model="val"
        :options="choices"
        label="name"
        :custom-label="fancyName"
        track-by="id"
        :taggable="formfield.related_model === 'Investor'"
        :tag-placeholder="$t('Press enter to create a new Investor')"
        @tag="addInvestor"
        :allow-empty="!formfield.required"
      />
    </div>
    <div style="margin: 0.3rem;" v-if="value && formfield.related_model === 'Investor'">
      <router-link
        target="_blank"
        :to="{ name: 'investor_detail', params: { investorId: value.id } }"
      >
        <span class="id-display investor-id-display">{{ value.id }}</span>
        {{ value.name }}</router-link
      >
    </div>
  </div>
</template>

<script>
  import AutoField from "$components/Fields/Display/AutoField";
  import gql from "graphql-tag";

  export default {
    components: { AutoField },
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
      addInvestor(newInv) {
        console.log(newInv);
        // const tag = {
        //   name: newTag,
        //   code: newTag.substring(0, 2) + Math.floor((Math.random() * 10000000))
        // }
        // this.options.push(tag)
        // this.value.push(tag)
      },
    },
  };
</script>
