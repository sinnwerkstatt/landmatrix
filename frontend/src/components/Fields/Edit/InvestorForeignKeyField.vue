<template>
  <div>
    <div>
      <multiselect
        v-model="val"
        :options="investors"
        label="name"
        :custom-label="(mdl) => `${mdl.name} (#${mdl.id})`"
        track-by="id"
        :taggable="true"
        :tag-placeholder="$t('Press enter to create a new Investor')"
        :allow-empty="!formfield.required"
        @tag="addInvestor"
      />
    </div>
    <div v-if="value" style="margin: 0.3rem">
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
  import gql from "graphql-tag";

  export default {
    props: {
      formfield: { type: Object, required: true },
      value: { type: Object, required: false, default: null },
      model: { type: String, required: true },
    },
    data() {
      return {
        investors: [],
      };
    },
    apollo: {
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
          this.$emit("input", { id: v.id, name: v.name });
        },
      },
    },
    methods: {
      addInvestor(newInv) {
        let props = this.$router.resolve({
          name: "investor_add",
        });
        let new_investor_window = window.open(
          `${props.href}?newName=${newInv}`,
          "_blank",
          "menubar=no"
        );
        new_investor_window.onbeforeunload = function (x) {
          console.log(x);
          // this.$apollo.queries.investors.refetch();
        };
      },
    },
  };
</script>
