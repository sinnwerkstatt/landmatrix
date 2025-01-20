<script lang="ts">
  import dayjs from "dayjs"
  import customParseFormat from "dayjs/plugin/customParseFormat"
  import { onMount } from "svelte"
  import { _ } from "svelte-i18n"
  import type { FormEventHandler } from "svelte/elements"

  dayjs.extend(customParseFormat)

  interface Props {
    name: string
    value: string | null
    required?: boolean
    class?: string
    onchange?: () => void
  }

  let {
    name,
    value = $bindable(),
    required = false,
    class: className = "",
    onchange,
  }: Props = $props()

  let inputField: HTMLInputElement | undefined = $state()

  let isValid: boolean = $state(true)
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

    inputField?.setCustomValidity(
      isValid ? "" : $_("Invalid format. Use YYYY, YYYY-MM or YYYY-MM-DD"),
    )
  }

  const oninput: FormEventHandler<HTMLInputElement> = event => {
    event.preventDefault()
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
    onchange?.()
  }

  onMount(checkValidity)
</script>

<div class="relative">
  <input
    bind:this={inputField}
    class="inpt w-36 {className}"
    maxlength="10"
    {name}
    {oninput}
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
