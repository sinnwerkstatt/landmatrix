<script lang="ts">
  import dayjs from "dayjs";
  import customParseFormat from "dayjs/plugin/customParseFormat";
  import { onMount } from "svelte";
  import { _ } from "svelte-i18n";

  dayjs.extend(customParseFormat);

  export let required = false;
  export let value: string;
  export let name: string;

  let inputfield;

  function checkValidity() {
    console.log("doing validity check", value);
    const field_valid =
      !value ||
      dayjs(
        value,
        ["YYYY", "YYYY-M", "YYYY-M-D", "YYYY-MM", "YYYY-MM-D", "YYYY-MM-DD"],
        true
      ).isValid();
    if (field_valid) {
      inputfield.setCustomValidity("");
    } else {
      inputfield.setCustomValidity(
        $_("Invalid format. Use YYYY, YYYY-MM or YYYY-MM-DD")
      );
    }
  }

  onMount(checkValidity);

  const onInput = async () => {
    if (!value) {
      inputfield.setCustomValidity("");
      return;
    }
    value = value.replace("/", "-").replace(".", "-").replace(",", "-");
    checkValidity();
  };
</script>

<div class="whitespace-nowrap">
  <input
    bind:this={inputfield}
    bind:value
    type="text"
    class="inpt"
    placeholder={$_("YYYY-MM-DD")}
    {required}
    {name}
    on:input={onInput}
  />
</div>
