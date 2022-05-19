<script lang="ts">
  import { _ } from "svelte-i18n";
  import { formfields } from "$lib/stores";
  import ArrayField from "$components/Fields/Display/ArrayField.svelte";
  import BooleanField from "$components/Fields/Display/BooleanField.svelte";
  import DecimalField from "$components/Fields/Display/DecimalField.svelte";
  import JSONDateAreaChoicesField from "$components/Fields/Display/JSONDateAreaChoicesField.svelte";
  import TextField from "$components/Fields/Display/TextField.svelte";
  import type { FormField } from "$components/Fields/fields";
  import AutoField from "./Display/AutoField.svelte";
  import DateField from "./Display/DateField.svelte";
  import FileField from "./Display/FileField.svelte";
  import ForeignKeyField from "./Display/ForeignKeyField.svelte";
  import JSONActorsField from "./Display/JSONActorsField.svelte";
  import JSONDateAreaField from "./Display/JSONDateAreaField.svelte";
  import JSONDateChoiceField from "./Display/JSONDateChoiceField.svelte";
  import JSONExportsField from "./Display/JSONExportsField.svelte";
  import JSONJobsField from "./Display/JSONJobsField.svelte";
  import LengthField from "./Display/LengthField.svelte";
  import ManyToManyField from "./Display/ManyToManyField.svelte";
  import OCIDField from "./Display/OCIDField.svelte";
  import PointField from "./Display/PointField.svelte";
  import StatusField from "./Display/StatusField.svelte";

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
    ArrayField: ArrayField,
    AutoField: AutoField,
    BooleanField: BooleanField,
    CharField: TextField,
    TypedChoiceField: TextField,
    CountryForeignKey: ForeignKeyField,
    CurrencyForeignKey: ForeignKeyField,
    DateField: DateField,
    DecimalField: DecimalField,
    EmailField: TextField,
    FileField: FileField,
    FloatField: DecimalField,
    ForeignKey: ForeignKeyField,
    IntegerField: DecimalField,
    InvestorForeignKey: ForeignKeyField,
    JSONActorsField: JSONActorsField,
    JSONDateAreaChoicesField: JSONDateAreaChoicesField,
    JSONDateAreaField: JSONDateAreaField,
    JSONDateChoiceField: JSONDateChoiceField,
    JSONExportsField: JSONExportsField,
    JSONJobsField: JSONJobsField,
    LengthField: LengthField,
    ManyToManyField: ManyToManyField,
    ModelChoiceField: ForeignKeyField,
    NullBooleanField: BooleanField,
    OCIDField: OCIDField,
    PointField: PointField,
    StatusField: StatusField,
    SimpleArrayField: ArrayField,
    TextField: TextField,
    URLField: TextField,
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
