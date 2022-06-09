<script lang="ts">
  import { _ } from "svelte-i18n";
  import { formfields } from "$lib/stores";
  import DecimalField from "$components/Fields/Edit/DecimalField.svelte";
  import TextField from "$components/Fields/Edit/TextField.svelte";
  import type { FormField } from "$components/Fields/fields";
  import BooleanField from "./Edit/BooleanField.svelte";
  import CharField from "./Edit/CharField.svelte";
  import CountryForeignKey from "./Edit/CountryForeignKey.svelte";
  import CurrencyForeignKey from "./Edit/CurrencyForeignKey.svelte";
  import DateField from "./Edit/DateField.svelte";
  import EmailField from "./Edit/EmailField.svelte";
  import FileField from "./Edit/FileField.svelte";
  import JSONDateAreaField from "./Edit/JSONDateAreaField.svelte";
  import JSONDateChoiceField from "./Edit/JSONDateChoiceField.svelte";
  import JSONLeaseField from "./Edit/JSONLeaseField.svelte";
  import SimpleArrayField from "./Edit/SimpleArrayField.svelte";
  import TypedChoiceField from "./Edit/TypedChoiceField.svelte";
  import URLField from "./Edit/URLField.svelte";

  export let fieldname: string;
  export let value;
  export let model = "deal";

  export let showLabel = true;
  export let wrapperClasses = "mb-3 leading-5 flex flex-wrap";
  export let labelClasses = "font-medium md:w-5/12 lg:w-4/12";
  export let valueClasses = "text-lm-dark md:w-7/12 lg:w-8/12";
  export let disabled = false;

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
    BooleanField: BooleanField,
    CharField: CharField,
    OCIDField: CharField,
    CountryForeignKey: CountryForeignKey,
    CurrencyForeignKey: CurrencyForeignKey,
    DateField: DateField,
    DecimalField: DecimalField,
    EmailField: EmailField,
    FileField: FileField,
    IntegerField: DecimalField,
    JSONDateChoiceField: JSONDateChoiceField,
    NullBooleanField: BooleanField,
    SimpleArrayField: SimpleArrayField,
    TextField: TextField,
    TypedChoiceField: TypedChoiceField,
    URLField: URLField,
    JSONDateAreaField: JSONDateAreaField,
    JSONLeaseField: JSONLeaseField,
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
      <svelte:component
        this={field}
        bind:value
        {model}
        {disabled}
        {formfield}
        on:change
      />
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
