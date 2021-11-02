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

<script lang="ts">
  import { Loader } from "@googlemaps/js-api-loader";
  import Vue from "vue";

  const loader = new Loader({
    apiKey: import.meta.env.VITE_GAPI_KEY,
    libraries: ["places"],
  });

  export default Vue.extend({
    props: {
      value: { type: String, required: false, default: "" },
      countryCode: { type: String, required: false, default: "" },
    },
    data() {
      return {
        autocomplete: null as unknown,
        randomhash: Math.random().toString(36).substring(2),
      };
    },
    computed: {
      val: {
        get(): string {
          return this.value;
        },
        set(): void {},
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
        ) as HTMLInputElement;
        if (!input_field) return;

        loader.load().then((google) => {
          const autocomplete = new google.maps.places.Autocomplete(input_field, {
            fields: ["geometry"],
            strictBounds: true,
            componentRestrictions: this.countryCode
              ? { country: this.countryCode }
              : undefined,
          });
          this.autocomplete = autocomplete;

          autocomplete?.addListener("place_changed", () => {
            const geometry = autocomplete.getPlace().geometry;
            if (!geometry) return;
            this.$emit("change", {
              latLng: [geometry.location?.lat(), geometry.location?.lng()],
              viewport: geometry.viewport,
            });
            this.$emit("input", input_field.value);
          });
        });
      });
    },
  });
</script>
