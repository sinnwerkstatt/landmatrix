<template>
  <div class="input-group">
    <input
      id="location-input"
      v-model="val"
      :placeholder="$t('Location')"
      :aria-label="$t('Location')"
      class="form-control"
    />
  </div>
</template>

<script>
  export default {
    props: {
      value: { type: String, required: false, default: "" },
      countryCode: { type: String, required: false, default: "" },
    },
    data() {
      return { autocomplete: null };
    },
    computed: {
      val: {
        get() {
          return this.value;
        },
        set() {},
      },
    },
    watch: {
      countryCode(cCode) {
        this.autocomplete.setComponentRestrictions({ country: cCode });
      },
    },
    created() {
      this.$nextTick(() => {
        const input_field = document.getElementById("location-input");

        let opts = { fields: ["geometry"], strictBounds: true };
        if (this.countryCode)
          opts.componentRestrictions = { country: this.countryCode };

        // eslint-disable-next-line no-undef
        this.autocomplete = new google.maps.places.Autocomplete(input_field, opts);

        this.autocomplete.addListener("place_changed", () => {
          const geometry = this.autocomplete.getPlace().geometry;
          this.$emit("change", {
            latLng: [geometry.location.lat(), geometry.location.lng()],
            viewport: geometry.viewport,
          });
          this.$emit("input", input_field.value);
        });
      });
    },
  };
</script>
