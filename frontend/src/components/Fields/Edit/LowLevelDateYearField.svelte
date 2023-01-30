<script lang="ts">
  import dayjs from "dayjs"
  import customParseFormat from "dayjs/plugin/customParseFormat"
  import { onMount } from "svelte"
  import { _ } from "svelte-i18n"

  dayjs.extend(customParseFormat)

  export let name: string
  export let value: string | undefined
  export let required = false

  let inputField: HTMLInputElement

  const checkValidity = () => {
    const isValid =
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

  const onInput = (event: InputEvent) => {
    const targetValue = (event.target as HTMLInputElement).value

    value =
      targetValue === ""
        ? undefined
        : targetValue
            .replaceAll("/", "-")
            .replaceAll(".", "-")
            .replaceAll(",", "-")
            .trim()

    checkValidity()
  }

  onMount(checkValidity)
</script>

<div class="whitespace-nowrap">
  <input
    bind:this={inputField}
    value={value ?? ""}
    type="text"
    class="inpt"
    placeholder={$_("YYYY-MM-DD")}
    {required}
    {name}
    on:input|preventDefault={onInput}
  />
</div>
