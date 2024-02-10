<script lang="ts">
  import dayjs from "dayjs"
  import customParseFormat from "dayjs/plugin/customParseFormat"
  import { onMount } from "svelte"
  import { _ } from "svelte-i18n"

  dayjs.extend(customParseFormat)

  export let name: string
  export let value: string | null
  export let required = false

  let inputField: HTMLInputElement

  let isValid: boolean
  const checkValidity = () => {
    isValid =
      !value ||
      dayjs(
        value,
        [
          "YYYY",
          "YYYY-MM",
          "YYYY-MM-DD",
          "YYYY-MM-D",
          "YYYY-M",
          "YYYY-M-DD",
          "YYYY-M-D",
        ],
        true,
      ).isValid()

    if (isValid) {
      inputField.setCustomValidity("")
    } else {
      inputField.setCustomValidity(
        $_("Invalid format. Use YYYY, YYYY-MM or YYYY-MM-DD"),
      )
    }
  }

  const onInput = (event: Event) => {
    const targetValue = (event.target as HTMLInputElement).value

    value =
      targetValue === ""
        ? null
        : targetValue
            .replaceAll("/", "-")
            .replaceAll(".", "-")
            .replaceAll(",", "-")
            .trim()

    checkValidity()
  }

  onMount(checkValidity)
</script>

<div class="relative">
  <input
    bind:this={inputField}
    class="inpt w-36 {$$props.class ?? ''}"
    maxlength="10"
    {name}
    on:input|preventDefault={onInput}
    placeholder={$_("YYYY-MM-DD")}
    {required}
    type="text"
    value={value ?? ""}
  />
  {#if !isValid}
    <span class="absolute right-0 top-full whitespace-nowrap text-xs text-red-700">
      YYYY, YYYY-MM or YYYY-MM-DD
    </span>
  {/if}
</div>
