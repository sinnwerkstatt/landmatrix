<template>
  <b-modal v-model="visible" :title="`${investor.name} (#${investor.id})`">
    <DisplayField
      v-for="fieldname in fields"
      :key="fieldname"
      :fieldname="fieldname"
      :value="investor[fieldname]"
      :visible="!!investor[fieldname]"
      model="investor"
    />

    <div v-if="investor.involvement">
      <h3>Involvement</h3>
      <DisplayField
        v-for="fieldname in involvement_fields"
        :key="fieldname"
        :value="investor.involvement[fieldname]"
        :visible="!!investor.involvement[fieldname]"
        :fieldname="fieldname"
        model="involvement"
      />
    </div>
    <template #modal-footer>
      <div class="w-100">
        <router-link
          :to="{ name: 'investor_detail', params: { investorId: investor.id } }"
          class="btn btn-investor investor-link float-right"
          target="_blank"
        >
          {{ $t("More details about this investor") }}
        </router-link>
      </div>
    </template>
  </b-modal>
</template>

<script>
  import DisplayField from "components/Fields/DisplayField";

  export default {
    components: { DisplayField },
    props: {
      investor: { type: Object, required: true },
      value: { type: Boolean, required: true },
    },
    data() {
      return {
        fields: ["classification", "country", "homepage", "comment"],
        involvement_fields: [
          "role",
          "investment_type",
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
