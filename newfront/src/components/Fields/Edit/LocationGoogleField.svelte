<script lang="ts">
  import { Loader } from "@googlemaps/js-api-loader?client"
  import { createEventDispatcher, onMount } from "svelte"
  import { _ } from "svelte-i18n"

  export let value = ""
  export let countryCode = ""

  let autocomplete: google.maps.places.Autocomplete
  let inputField: HTMLInputElement

  const dispatch = createEventDispatcher()

  let loader: Loader

  function locationAutocomplete() {
    if (!loader)
      loader = new Loader({
        apiKey: import.meta.env.VITE_GAPI_KEY,
        libraries: ["places"],
      })
    loader.load().then(google => {
      // noinspection TypeScriptUnresolvedVariable,TypeScriptUnresolvedFunction
      autocomplete = new google.maps.places.Autocomplete(inputField, {
        fields: ["geometry"],
        strictBounds: true,
        componentRestrictions: countryCode ? { country: countryCode } : undefined,
      })
      autocomplete?.addListener("place_changed", () => {
        const geometry = autocomplete.getPlace().geometry
        if (!geometry) return
        dispatch("change", {
          latLng: [geometry.location?.lat(), geometry.location?.lng()],
          viewport: geometry.viewport,
        })
        value = inputField.value
      })
    })
  }

  onMount(locationAutocomplete)
  // onDestroy(() => {
  //   console.log("onDestroy. loader", loader);
  // });
  //
  // afterUpdate(() => {
  //   console.log("afterUpdate. loader", loader);
  // });

  $: autocomplete?.setComponentRestrictions({ country: countryCode })
</script>

<div class="input-group">
  <input bind:this={inputField} bind:value placeholder={$_("Location")} class="inpt" />
  <!--  on:keydown|preventDefault=.enter.prevent=""-->
</div>
