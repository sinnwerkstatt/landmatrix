<script lang="ts">
  import { Loader } from "@googlemaps/js-api-loader?client"
  import { env } from "$env/dynamic/public"
  import type { Point } from "geojson"
  import { onMount } from "svelte"
  import { _ } from "svelte-i18n"

  export let value = ""
  export let fieldname: string

  export let extras: {
    countryCode: string
    onGoogleAutocomplete: (point: Point) => void
  } = {
    countryCode: "",
    onGoogleAutocomplete: () => {},
  }

  let autocomplete: google.maps.places.Autocomplete
  let inputField: HTMLInputElement

  let apiKey = env.PUBLIC_GAPI_KEY
  let loader: Loader

  const locationAutocomplete = () => {
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
        componentRestrictions: extras.countryCode
          ? { country: extras.countryCode }
          : undefined,
      })
      autocomplete?.addListener("place_changed", () => {
        value = inputField.value

        const geometry = autocomplete.getPlace().geometry
        if (geometry && geometry.location) {
          const point: Point = {
            type: "Point",
            coordinates: [
              parseFloat(geometry.location.lng().toFixed(5)),
              parseFloat(geometry.location.lat().toFixed(5)),
            ],
          }

          extras.onGoogleAutocomplete(point)
        }
      })
    })
  }

  onMount(locationAutocomplete)

  $: autocomplete?.setComponentRestrictions(
    extras.countryCode ? { country: extras.countryCode } : null,
  )
</script>

<input
  class="inpt"
  bind:this={inputField}
  bind:value
  name={fieldname}
  placeholder={$_("Location")}
/>
