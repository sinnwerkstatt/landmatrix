<template>
  <div class="row">
    <div class="col-md-6">
      <div class="small">Lat:</div>
      <LowLevelDecimalField
        v-model="val.lat"
        :min-value="-90"
        :max-value="90"
        :decimals="5"
      />
    </div>
    <div class="col-md-6">
      <div class="small">Lng:</div>
      <LowLevelDecimalField
        v-model="val.lng"
        :min-value="-180"
        :max-value="180"
        :decimals="5"
      />
    </div>
  </div>
</template>

<script>
  import LowLevelDecimalField from "$components/Fields/Edit/LowLevelDecimalField";

  export default {
    components: { LowLevelDecimalField },
    props: {
      value: { type: Object, required: false, default: () => ({}) },
    },
    data() {
      return {
        val: JSON.parse(JSON.stringify(this.value)),
      };
    },
    watch: {
      value(newValue, oldValue) {
        if (newValue.lat === oldValue.lat && newValue.lng === oldValue.lng) return;
        this.val = JSON.parse(JSON.stringify(newValue));
      },
      val: {
        deep: true,
        handler(v) {
          this.$emit("input", v);
        },
      },
    },
  };
</script>
