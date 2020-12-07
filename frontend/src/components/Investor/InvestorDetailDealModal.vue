<template>
  <b-modal v-model="visible" :title="`Deal ${deal.name}`">
    <DisplayField
      :fieldname="fieldname"
      :readonly="true"
      v-model="deal[fieldname]"
      v-for="fieldname in fields"
      model="deal"
    />
    <template v-slot:modal-footer>
      <div class="w-100">
        <router-link
          :to="{
            name: 'deal_detail',
            params: { deal_id: deal._id },
          }"
          class="btn btn-primary deal-link float-right"
          target="_blank"
        >
          More details about this deal
        </router-link>
      </div>
    </template>
  </b-modal>
</template>

<script>
  import DisplayField from "/components/Fields/DisplayField";

  export default {
    props: ["deal", "value"],
    components: { DisplayField },
    data() {
      return {
        fields: [
          "country",
          "intention_of_investment",
          "implementation_status",
          "negotiation_status",
          "intended_size",
          "contract_size",
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
