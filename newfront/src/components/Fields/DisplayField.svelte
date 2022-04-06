<script lang="ts">
  import TextField from "$components/Fields/Display/TextField.svelte";
  import { formfields } from "$lib/stores";
  import type { FormField } from "$components/Fields/fields";
  import DecimalField from "$components/Fields/Display/DecimalField.svelte";
  import { _ } from "svelte-i18n";
  import BooleanField from "$components/Fields/Display/BooleanField.svelte";
  import ArrayField from "$components/Fields/Display/ArrayField.svelte";
  import JSONDateAreaChoicesField from "$components/Fields/Display/JSONDateAreaChoicesField.svelte";
  import JSONDateAreaField from "./Display/JSONDateAreaField.svelte";
  import JSONDateChoiceField from "./Display/JSONDateChoiceField.svelte";
  import DateField from "./Display/DateField.svelte";
  import JSONJobsField from "./Display/JSONJobsField.svelte";
  import FileField from "./Display/FileField.svelte";
  import JSONExportsField from "./Display/JSONExportsField.svelte";

  export let fieldname: string;
  export let value;
  export let model = "deal";

  export let showLabel = true;
  export let wrapperClasses = "mb-3 leading-5 flex flex-wrap";
  export let labelClasses = "font-medium md:w-5/12 lg:w-4/12";
  export let valueClasses = "text-lm-dark md:w-7/12 lg:w-8/12";

  //   fileNotPublic: { type: Boolean, default: false },
  //   visible: { type: Boolean, default: true },
  //   targetBlank: { type: Boolean, default: false },
  //   objectId: { type: Number, default: null, required: false },
  //   objectVersion: { type: Number, default: null, required: false },

  //   computed: {
  //     _visible(): boolean {
  //       if (!this.visible) return false;
  //       if (this.fieldname === "file_not_public") return false;
  //       if (this.formfield.class === "FileField") {
  //         return !this.fileNotPublic || this.$store.getters.userAuthenticated;
  //       }
  //       return true;
  //     },

  let formfield: FormField;
  $: formfield = { name: fieldname, ...$formfields[model][fieldname] };

  $: field = {
    JSONDateAreaChoicesField: JSONDateAreaChoicesField,
    JSONDateAreaField: JSONDateAreaField,
    JSONDateChoiceField: JSONDateChoiceField,
    JSONExportsField: JSONExportsField,
    JSONJobsField: JSONJobsField,
    ArrayField: ArrayField,
    NullBooleanField: BooleanField,
    BooleanField: BooleanField,
    CharField: TextField,
    EmailField: TextField,
    FileField: FileField,
    URLField: TextField,
    TextField: TextField,
    DateField: DateField,
    DecimalField: DecimalField,
    FloatField: DecimalField,
    IntegerField: DecimalField,
  }[formfield.class];
</script>

<div class={wrapperClasses}>
  {#if showLabel}
    <div class={labelClasses}>
      {$_(formfield.label)}
    </div>
  {/if}
  <div class={valueClasses}>
    {#if field}
      <svelte:component this={field} {value} {model} {formfield} />
      <!--  <div>-->
      <!--    <component-->
      <!--      :file-not-public="fileNotPublic"-->
      <!--      :target-blank="targetBlank"-->
      <!--      :object-id="objectId"-->
      <!--      :object-version="objectVersion"-->
      <!--    />-->
      <!--  </div>-->
    {:else}
      <span class="italic text-red-600">Unknown field: {formfield.class}</span>
    {/if}
  </div>
</div>
