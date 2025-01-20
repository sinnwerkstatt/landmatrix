<script lang="ts">
  import type { Loader as LoaderType } from "@googlemaps/js-api-loader"
  import { env } from "$env/dynamic/public"
  import type { Point } from "geojson"
  import { onMount } from "svelte"
  import { _ } from "svelte-i18n"

  interface Props {
    value?: string
    fieldname: string
    extras?: {
      countryCode: string
      onGoogleAutocomplete: (point: Point) => void
    }
  }

  let { value = $bindable(), fieldname, extras }: Props = $props()

  let autocomplete: google.maps.places.Autocomplete | undefined = $state()
  let inputField: HTMLInputElement | undefined = $state()

  let apiKey = env.PUBLIC_GAPI_KEY
  let loader: LoaderType

  const locationAutocomplete = async () => {
    if (!apiKey) return

    const { Loader } = await import("@googlemaps/js-api-loader")

    if (!loader) loader = new Loader({ apiKey, libraries: ["places"] })

    loader.importLibrary("places").then(({ Autocomplete }) => {
      autocomplete = new Autocomplete(inputField!, {
        fields: ["geometry"],
        strictBounds: true,
        componentRestrictions: extras?.countryCode
          ? { country: extras.countryCode }
          : undefined,
      })

      autocomplete?.addListener("place_changed", () => {
        value = inputField!.value

        const geometry = autocomplete!.getPlace().geometry
        if (geometry && geometry.location) {
          const point: Point = {
            type: "Point",
            coordinates: [
              parseFloat(geometry.location.lng().toFixed(5)),
              parseFloat(geometry.location.lat().toFixed(5)),
            ],
          }

          extras?.onGoogleAutocomplete?.(point)
        }
      })
    })
  }

  onMount(locationAutocomplete)

  $effect(() => {
    const cCode = extras?.countryCode
    autocomplete?.setComponentRestrictions(cCode ? { country: cCode } : null)
  })
</script>

<input
  class="inpt"
  bind:this={inputField}
  bind:value
  name={fieldname}
  placeholder={$_("Location")}
/>
