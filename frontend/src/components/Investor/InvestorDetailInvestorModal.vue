<template>
  <b-modal v-model="visible" :title="`${investor.name} (#${investor.id})`">
    <DisplayField
      :fieldname="fieldname"
      :readonly="true"
      v-model="investor[fieldname]"
      v-for="fieldname in fields"
      model="investor"
    />

    <div v-if="investor.involvement">
      <h3>Involvement</h3>
      <DisplayField
        :fieldname="fieldname"
        :readonly="true"
        v-model="investor.involvement[fieldname]"
        v-for="fieldname in involvement_fields"
        model="involvement"
      />
    </div>
    <template v-slot:modal-footer>
      <div class="w-100">
        <router-link
          :to="{
            name: 'investor_detail',
            params: { investor_id: investor.id },
          }"
          class="btn btn-investor investor-link float-right"
          target="_blank"
        >
          More details about this investor
        </router-link>
      </div>
    </template>
  </b-modal>
</template>

<script>
  import DisplayField from "/components/Fields/DisplayField";

  export default {
    props: ["investor", "value"],
    components: { DisplayField },
    data() {
      return {
        fields: ["classification", "country", "homepage", "comment"],
        involvement_fields: [
          "role",
          "investment_type",
          // "involvement_type",
          "percentage",
          "loans_amount",
          "loans_currency",
          "loans_date",
          "parent_relation",
          "comment",
        ],
      };
    },
    computed: {
      visible: {
        get() {
          return this.value;
        },
        set(val) {
          this.$emit("input", val);
        },
      },
    },
  };
</script>
