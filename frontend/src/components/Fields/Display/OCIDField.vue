<template>
  <div>
    <div>{{ value }}</div>
    <div><a :href="ocidUrl" target="_blank">{{ $t("Access more information about this contract on OpenLandContracts.org") }}</a></div>
  </div>
</template>

<script>
  export default {
    props: {
      formfield: { type: Object, required: true },
      value: { type: String, required: true },
      model: { type: String, required: true },
    },
    computed: {
      ocidUrl() {
        return `https://www.openlandcontracts.org/contract/${this.value}/view#/pdf`;
      }
    }
  };
</script>
