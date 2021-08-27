<template>
  <div>
    <div>
      <input
        v-if="formfield.required"
        v-model="val"
        required
        type="text"
        style="width: 0; height: 0; position: absolute; z-index: -10"
      />
      <multiselect
        v-model="val"
        :options="investors"
        label="name"
        :custom-label="(mdl) => `${mdl.name} (#${mdl.id})`"
        track-by="id"
        :taggable="true"
        :tag-placeholder="$t('Press enter to create a new Investor')"
        :allow-empty="false"
        deselect-label=""
        select-label=""
        @tag="openNewInvestorDialog"
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
    <div v-if="show_new_investor_form" class="investor">
      <form id="new_investor" @submit.prevent="addNewInvestor">
        <div class="container">
          <EditField
            v-for="fieldname in general_fields"
            :key="fieldname"
            v-model="new_investor[fieldname]"
            :fieldname="fieldname"
            :label-classes="['col-md-3']"
            :value-classes="['col-md-9']"
            :wrapper-classes="['row', 'my-3']"
            model="investor"
          />
        </div>
        <button type="submit" class="btn btn-primary">{{ $t("Save") }}</button>
      </form>
    </div>
  </div>
</template>

<script>
  import gql from "graphql-tag";

  export default {
    components: { EditField: () => import("$components/Fields/EditField") },
    props: {
      formfield: { type: Object, required: true },
      value: { type: Object, required: false, default: null },
      model: { type: String, required: true },
    },
    data() {
      return {
        show_new_investor_form: false,
        investors: [],
        new_investor: {},
        general_fields: [
          "name",
          "country",
          "classification",
          "homepage",
          "opencorporates",
          "comment",
        ],
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
      openNewInvestorDialog(newInv) {
        this.$emit("input", null);
        this.new_investor.name = newInv;
        this.show_new_investor_form = true;
      },
      addNewInvestor() {
        let form = document.querySelector("#new_investor");
        if (!form.checkValidity()) form.reportValidity();
        else this.investor_save();
      },
      investor_save() {
        this.saving_in_progress = true;
        return this.$apollo
          .mutate({
            mutation: gql`
              mutation ($payload: Payload) {
                investor_edit(id: -1, payload: $payload) {
                  investorId
                  investorVersion
                }
              }
            `,
            variables: { payload: this.new_investor },
          })
          .then(({ data: { investor_edit } }) => {
            this.saving_in_progress = false;
            let new_i = { id: investor_edit.investorId, name: this.new_investor.name };
            this.investors.push(new_i);
            this.$emit("input", new_i);
            this.new_investor = {};
            this.show_new_investor_form = false;
          });
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
