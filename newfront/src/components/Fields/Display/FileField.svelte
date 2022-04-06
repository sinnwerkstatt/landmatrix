<script lang="ts">
  import type { FormField } from "$components/Fields/fields";
  import FilePdfIcon from "../../icons/FilePdfIcon.svelte";
  import EyeSlashIcon from "../../icons/EyeSlashIcon.svelte";

  export let formfield: FormField;
  export let value: string;
  export let model: string;
  export let fileNotPublic: boolean;

  export let data = () => {
    return { media_url: import.meta.env.VITE_MEDIA_URL };
  };
</script>

<div class="file_field">
  <a href={value} target="_blank">
    {#if fileNotPublic}
      <EyeSlashIcon />
    {/if}
    <FilePdfIcon />
    {value.replace("uploads/", "")}
  </a>
</div>

<!--  <div class="file_field">-->
<!--    <a :href="`${media_url}${value}`" target="_blank">-->
<!--      <i v-if="fileNotPublic" class="fas fa-eye-slash mr-1"></i>-->
<!--      <i class="far fa-file-pdf"></i>-->
<!--      {{ value.replace("uploads/", "") }}-->
<!--    </a>-->
<!--  </div>-->

<!--<script lang="ts">-->
<!--  import Vue from "vue";-->
<!--  import type { PropType } from "vue";-->
<!--  import type { FormField } from "$components/Fields/fields";-->

<!--  export default Vue.extend({-->
<!--    props: {-->
<!--      formfield: { type: Object as PropType<FormField>, required: true },-->
<!--      value: { type: String, required: true },-->
<!--      model: { type: String, required: true },-->
<!--      fileNotPublic: { type: Boolean, default: false },-->
<!--    },-->
<!--    data() {-->
<!--      return { media_url: import.meta.env.VITE_MEDIA_URL };-->
<!--    },-->
<!--  });-->
<!--</script>-->
