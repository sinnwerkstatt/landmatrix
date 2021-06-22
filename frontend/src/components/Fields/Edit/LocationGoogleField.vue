<template>
  <div class="input-group">
    <input
      :id="`location-input-${randomhash}`"
      v-model="val"
      :placeholder="$t('Location')"
      :aria-label="$t('Location')"
      class="form-control"
      @keydown.enter.prevent=""
    />
  </div>
</template>

<script>
  import { Loader } from "@googlemaps/js-api-loader";

  const loader = new Loader({
    apiKey: import.meta.env.VITE_GAPI_KEY,
    libraries: ["places"],
  });

  export default {
    props: {
      value: { type: String, required: false, default: "" },
      countryCode: { type: String, required: false, default: "" },
    },
    data() {
      return {
        autocomplete: null,
        randomhash: Math.random().toString(36).substring(2),
      };
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
        const input_field = document.getElementById(
          `location-input-${this.randomhash}`
        );

        let opts = { fields: ["geometry"], strictBounds: true };
        if (this.countryCode)
          opts.componentRestrictions = { country: this.countryCode };

        loader.load().then(() => {
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
      });
    },
  };
</script>
