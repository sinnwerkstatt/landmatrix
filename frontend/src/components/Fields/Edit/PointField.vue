<template>
  <div class="row">
    <div class="col-md-6">
      Lat:
      <LowLevelDecimalField
        v-model="val.lat"
        :min-value="-90"
        :max-value="90"
        :decimals="8"
      />
    </div>
    <div class="col-md-6">
      Lng:
      <LowLevelDecimalField
        v-model="val.lng"
        :min-value="-180"
        :max-value="180"
        :decimals="8"
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
      val: {
        deep: true,
        handler(v) {
          this.$emit("input", v);
          // this.$store.dispatch("changeLocationPoint", v);
        },
      },
    },
  };
</script>
