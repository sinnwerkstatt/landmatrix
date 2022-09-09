<script lang="ts">
  import { _ } from "svelte-i18n"

  import { formfields } from "$lib/stores"

  import ArrayField from "$components/Fields/Display/ArrayField.svelte"
  import AutoField from "$components/Fields/Display/AutoField.svelte"
  import BooleanField from "$components/Fields/Display/BooleanField.svelte"
  import DateField from "$components/Fields/Display/DateField.svelte"
  import DateTimeField from "$components/Fields/Display/DateTimeField.svelte"
  import DecimalField from "$components/Fields/Display/DecimalField.svelte"
  import FileField from "$components/Fields/Display/FileField.svelte"
  import ForeignKeyField from "$components/Fields/Display/ForeignKeyField.svelte"
  import JSONActorsField from "$components/Fields/Display/JSONActorsField.svelte"
  import JSONDateAreaChoicesField from "$components/Fields/Display/JSONDateAreaChoicesField.svelte"
  import JSONDateAreaField from "$components/Fields/Display/JSONDateAreaField.svelte"
  import JSONDateChoiceField from "$components/Fields/Display/JSONDateChoiceField.svelte"
  import JSONExportsField from "$components/Fields/Display/JSONExportsField.svelte"
  import JSONJobsField from "$components/Fields/Display/JSONJobsField.svelte"
  import JSONLeaseField from "$components/Fields/Display/JSONLeaseField.svelte"
  import LengthField from "$components/Fields/Display/LengthField.svelte"
  import ManyToManyField from "$components/Fields/Display/ManyToManyField.svelte"
  import OCIDField from "$components/Fields/Display/OCIDField.svelte"
  import PointField from "$components/Fields/Display/PointField.svelte"
  import TextField from "$components/Fields/Display/TextField.svelte"
  import TypedChoiceField from "$components/Fields/Display/TypedChoiceField.svelte"
  import WorkflowInfosField from "$components/Fields/Display/WorkflowInfosField.svelte"
  import type { FormField } from "$components/Fields/fields"

  export let fieldname: string
  export let value
  export let model:
    | "deal"
    | "location"
    | "contract"
    | "datasource"
    | "investor"
    | "involvement" = "deal"

  export let showLabel = false
  export let wrapperClasses = "mb-3 leading-5 flex flex-wrap"
  export let labelClasses = "font-medium md:w-5/12 lg:w-4/12"
  export let valueClasses = "text-lm-dark md:w-7/12 lg:w-8/12"

  export let fileNotPublic = false
  export let targetBlank = false
  export let objectVersion: number | undefined = undefined

  //   visible: { type: Boolean, default: true },

  //   computed: {
  //     _visible(): boolean {
  //       if (!this.visible) return false;
  //       if (this.fieldname === "file_not_public") return false;
  //       if (this.formfield.class === "FileField") {
  //         return !fileNotPublic || this.$store.getters.userAuthenticated;
  //       }
  //       return true;
  //     },

  let formfield: FormField
  $: formfield = { name: fieldname, ...$formfields[model][fieldname] }

  $: field = {
    BooleanField: BooleanField,
    DateField: DateField,
    JSONActorsField: JSONActorsField,
    JSONDateAreaChoicesField: JSONDateAreaChoicesField,
    JSONDateAreaField: JSONDateAreaField,
    JSONDateChoiceField: JSONDateChoiceField,
    JSONExportsField: JSONExportsField,
    JSONJobsField: JSONJobsField,
    JSONLeaseField: JSONLeaseField,
    ManyToManyField: ManyToManyField,
    NullBooleanField: BooleanField,
    OCIDField: OCIDField,
    PointField: PointField,
    WorkflowInfosField: WorkflowInfosField,
  }[formfield.class]
</script>

<div class={wrapperClasses}>
  {#if showLabel}
    <div class={labelClasses}>
      {$_(formfield.label)}
    </div>
  {/if}
  <div class={valueClasses}>
    {#if formfield.class === "AutoField"}
      <AutoField {value} {model} {formfield} {targetBlank} {objectVersion} />
    {:else if ["ArrayField", "SimpleArrayField"].includes(formfield.class)}
      <ArrayField {value} {formfield} />
    {:else if formfield.class === "TypedChoiceField"}
      <TypedChoiceField {value} {formfield} />
    {:else if ["CharField", "EmailField", "TextField", "URLField"].includes(formfield.class)}
      <TextField {value} {formfield} />
    {:else if ["DecimalField", "FloatField", "IntegerField"].includes(formfield.class)}
      <DecimalField {value} {formfield} />
    {:else if formfield.class === "DateTimeField"}
      <DateTimeField {value} />
    {:else if formfield.class === "LengthField"}
      <LengthField {value} {formfield} />
    {:else if ["CountryForeignKey", "CurrencyForeignKey", "ForeignKey", "InvestorForeignKey", "ModelChoiceField"].includes(formfield.class)}
      <ForeignKeyField {value} {formfield} />
    {:else if formfield.class === "FileField"}
      <FileField {value} {formfield} {fileNotPublic} />
    {:else if field}
      <svelte:component this={field} {value} {model} {formfield} />
      <!--  old Vue -->
      <!--      :object-id="objectId"-->
      <!--      :object-version="objectVersion"-->
    {:else}
      <span class="italic text-red-600">Unknown field: {formfield.class}</span>
    {/if}
  </div>
</div>
