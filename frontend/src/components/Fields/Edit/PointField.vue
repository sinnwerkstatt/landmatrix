<template>
  <div>
    <div>
      Lat:
      <LowLevelDecimalField
        v-model="val.lat"
        :min-value="-90"
        :max-value="90"
        :decimals="8"
      />
    </div>
    <div>
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
      formfield: { type: Object, required: true },
      value: { type: Object, required: false, default: () => ({}) },
      model: { type: String, required: true },
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
          this.$store.dispatch("changeLocationPoint", v);
        },
      },
    },
  };
</script>
