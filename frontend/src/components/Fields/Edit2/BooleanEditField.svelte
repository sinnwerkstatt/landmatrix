<script lang="ts">
  import LowLevelNullBooleanField from "$components/Fields/Edit/LowLevelNullBooleanField.svelte"

  export let value: boolean | null
  export let fieldname: string
  export let extras = { nullable: false }
</script>

<LowLevelNullBooleanField bind:value {fieldname} nullable={extras.nullable} />
