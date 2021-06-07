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
    <div v-if="value" class="investor">
      <router-link
        target="_blank"
        :to="{ name: 'investor_detail', params: { investorId: value.id } }"
        class="id-display investor-id-display"
      >
        {{ value.id }}
      </router-link>
      <router-link
        target="_blank"
        :to="{ name: 'investor_detail', params: { investorId: value.id } }"
        style="padding-left: 0.3em; font-size: 0.9em; color: black"
      >
        {{ value.name }}
      </router-link>
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
          investors(sort: "name", limit: 0, subset: UNFILTERED) {
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
        new_investor_window.onbeforeunload = () => {
          this.$apollo.queries.investors.refetch().then(() => {
            this.val = this.investors.filter(
              (i) => i.name.lower() === newInv.lower()
            )[0];
          });
        };
      },
    },
  };
</script>

<style lang="scss" scoped>
  .investor {
    padding: 0.5em 0.3em 1em 0.7em;
    background-color: rgba(0, 0, 0, 0.05);
    border-bottom-left-radius: 10px;
    border-bottom-right-radius: 10px;
    a {
      &:hover {
        text-decoration: none;
      }
    }
  }
</style>
