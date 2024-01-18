<script lang="ts">
  import { Loader } from "@googlemaps/js-api-loader?client"
  import { createEventDispatcher, onMount } from "svelte"
  import { _ } from "svelte-i18n"

  import { LABEL_CLASS, VALUE_CLASS, WRAPPER_CLASS } from "$components/Fields/consts"
  import Label2 from "$components/Fields/Display2/Label2.svelte"

  export let value = ""
  export let countryCode = ""
  export let fieldname: string
  export let label = ""
  export let wrapperClass = WRAPPER_CLASS
  export let labelClass = LABEL_CLASS
  export let valueClass = VALUE_CLASS

  let autocomplete: google.maps.places.Autocomplete
  let inputField: HTMLInputElement

  const dispatch = createEventDispatcher()

  let apiKey = import.meta.env.VITE_GAPI_KEY
  let loader: Loader

  function locationAutocomplete() {
    if (!apiKey) return
    if (!loader)
      loader = new Loader({
        apiKey,
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

  $: autocomplete?.setComponentRestrictions({ country: countryCode })
</script>

<div class={wrapperClass} data-fieldname={fieldname}>
  {#if label}
    <Label2 value={label} class={labelClass} />
  {/if}
  <div class={valueClass}>
    <input
      bind:this={inputField}
      bind:value
      placeholder={$_("Location")}
      class="inpt"
    />
  </div>
</div>
