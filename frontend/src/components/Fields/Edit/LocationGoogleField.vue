<template>
  <div>
    <div class="input-group">
      <input
        v-model="val"
        type="text"
        :placeholder="formfield.placeholder || formfield.label"
        :aria-label="formfield.placeholder || formfield.label"
        :name="formfield.name"
        class="form-control"
        id="location-input"
      />
    </div>
  </div>
</template>

<script>
  export default {
    props: {
      formfield: { type: Object, required: true },
      value: { type: String, required: false, default: "" },
      model: { type: String, required: true },
    },
    computed: {
      val: {
        get() {
          return this.value;
        },
        set(v) {
          this.$emit("input", v);
        },
      },
    },
    created() {
      this.$nextTick(() => {
        const autocomplete = new google.maps.places.Autocomplete(
          document.getElementById("location-input"),
          { fields: ["geometry"], strictBounds: false }
        );

        autocomplete.addListener("place_changed", () => {
          let geometry = autocomplete.getPlace().geometry;
          this.$store.dispatch("locationGoogleAutocomplete", {
            latLng: [geometry.location.lat(), geometry.location.lng()],
            viewport: geometry.viewport,
          });
        });
      });
    },
  };
</script>
