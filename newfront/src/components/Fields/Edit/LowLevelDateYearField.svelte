<script lang="ts">
  import dayjs from "dayjs";
  import customParseFormat from "dayjs/plugin/customParseFormat";

  dayjs.extend(customParseFormat);

  export let required = false;
  export let value: string | Date;

  let valid_state = "";
  let inputfield;

  const onChange = async () => {
    if (!value) {
      // this.$emit("input", null);
      valid_state = "";
      inputfield.setCustomValidity("");
      return;
    }
    value = value.replace("/", "-").replace(".", "-").replace(",", "-");

    const field_valid = dayjs(
      value,
      ["YYYY", "YYYY-M", "YYYY-M-D", "YYYY-MM", "YYYY-MM-D", "YYYY-MM-DD"],
      true
    ).isValid();
    if (field_valid) {
      valid_state = "is-valid";
      inputfield.setCustomValidity("");
    } else {
      valid_state = "border-2 border-red-600 text-red-700";
      inputfield.setCustomValidity("Invalid format. Use YYYY, YYYY-MM or YYYY-MM-DD");
    }
  };
</script>

<div class="whitespace-nowrap">
  <input
    bind:this={inputfield}
    bind:value
    type="text"
    class="inpt {valid_state}"
    placeholder="YYYY-MM-DD"
    {required}
    on:input={onChange}
  />
</div>
