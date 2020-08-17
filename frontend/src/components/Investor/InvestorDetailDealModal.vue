<template>
  <b-modal v-model="visible" :title="`Deal ${deal.name}`">
    <Field
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
          v-slot="{ href }"
        >
          <a :href="href">More details about this deal</a>
        </router-link>
      </div>
    </template>
  </b-modal>
</template>

<script>
  import Field from "/components/Fields/Field";

  export default {
    props: ["deal", "value"],
    components: { Field },
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
