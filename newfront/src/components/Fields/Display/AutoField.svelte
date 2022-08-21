<script lang="ts">
  import classNames from "classnames";
  import type { FormField } from "$components/Fields/fields";

  export let formfield: FormField;
  export let value: number;

  export let targetBlank = false;
  export let objectVersion: number | undefined = undefined;
  export let model: "deal" | "investor" = "deal";
</script>

<div class="auto_field" data-name={formfield.name}>
  <a
    class={classNames(
      "inline py-1 px-2 text-white text-xs font-bold text-center whitespace-nowrap align-baseline",
      model === "deal"
        ? "bg-orange hover:bg-orange-600"
        : "bg-pelorous hover:bg-pelorous-600 hover:text-pelorous-200"
    )}
    href="/{model}/{value}/{objectVersion ?? ''}"
    target={targetBlank ? "_blank" : undefined}
  >
    {value}
  </a>
</div>
