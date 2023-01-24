<script lang="ts">
  import dayjs from "dayjs"
  import customParseFormat from "dayjs/plugin/customParseFormat"
  import { onMount } from "svelte"
  import { _ } from "svelte-i18n"

  dayjs.extend(customParseFormat)

  export let required = false
  export let value: string | undefined
  export let name: string

  export let emitUndefinedOnEmpty = false

  let inputField: HTMLInputElement

  const checkValidity = () => {
    const isValid =
      !value ||
      dayjs(
        value,
        ["YYYY", "YYYY-M", "YYYY-M-D", "YYYY-MM", "YYYY-MM-D", "YYYY-MM-DD"],
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

  onMount(checkValidity)

  const onInput = () => {
    if (!value) {
      if (emitUndefinedOnEmpty && value === "") value = undefined
      inputField.setCustomValidity("")
      return
    }
    value = value.replace("/", "-").replace(".", "-").replace(",", "-").trim()
    checkValidity()
  }
</script>

<div class="whitespace-nowrap">
  <input
    bind:this={inputField}
    bind:value
    type="text"
    class="inpt"
    placeholder={$_("YYYY-MM-DD")}
    {required}
    {name}
    on:input={onInput}
  />
</div>
