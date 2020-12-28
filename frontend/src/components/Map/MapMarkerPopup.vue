<template>
  <div class="deal-popup">
    <h3>Deal #{{ deal.id }}</h3>
    <div class="deal-summary">
      <DisplayField
        :wrapper-classes="['map-marker-popup-wrapper']"
        :label-classes="['map-marker-popup-label']"
        :value-classes="['map-marker-popup-value']"
        fieldname="level_of_accuracy"
        model="location"
        :value="location.level_of_accuracy"
      />
      <DisplayField
        :wrapper-classes="['map-marker-popup-wrapper']"
        :label-classes="['map-marker-popup-label']"
        :value-classes="['map-marker-popup-value']"
        fieldname="current_intention_of_investment"
        :value="deal.current_intention_of_investment"
      />
      <DisplayField
        :wrapper-classes="['map-marker-popup-wrapper']"
        :label-classes="['map-marker-popup-label']"
        :value-classes="['map-marker-popup-value']"
        fieldname="deal_size"
        :value="deal.deal_size"
      />
      <DisplayField
        :wrapper-classes="['map-marker-popup-wrapper']"
        :label-classes="['map-marker-popup-label']"
        :value-classes="['map-marker-popup-value']"
        fieldname="operating_company"
        :value="deal.operating_company"
      />
    </div>
    <router-link
      :to="{ name: 'deal_detail', params: { dealId: deal.id } }"
      class="btn btn-primary"
      target="_blank"
    >
      {{ $t("More details") }}
    </router-link>
  </div>
</template>

<script>
  import DisplayField from "../Fields/DisplayField";
  export default {
    name: "MapPopup",
    components: { DisplayField },
    props: ["deal", "location"],
  };
</script>

<style lang="scss">
  .map-marker-popup-wrapper {
    margin-bottom: 1em;
  }
  .map-marker-popup-label {
    font-weight: bold;
  }
</style>
