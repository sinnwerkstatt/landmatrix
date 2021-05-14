<template>
  <div>
    <div v-for="fieldname in fields" :key="fieldname">
      <EditField
        v-model="involvement[fieldname]"
        :fieldname="fieldname"
        model="involvement"
        :label-classes="['display-field-value', 'col-md-3']"
        :value-classes="['display-field-label', 'col-md-9']"
      />
    </div>
  </div>
</template>

<script>
  import EditField from "../Fields/EditField";

  export default {
    name: "InvolvementEdit",
    components: { EditField },
    props: {
      involvement: { type: Object, required: true },
      type: { type: String, default: "parent" },
    },
    data() {
      let fields = [
        "investor",
        "investment_type",
        "percentage",
        "loans_amount",
        "loans_currency",
        "loans_date",
      ];
      if (this.type === "parent") fields.push("parent_relation");
      fields.push("comment");
      return {
        fields,
      };
    },
  };
</script>

<style scoped></style>
