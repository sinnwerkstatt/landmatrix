<script lang="ts">
  export let data: { label: string; value: string }[] = []
</script>

<table class="w-full table-fixed text-a-sm">
  <tbody>
    {#each data as { label, value }}
      {@const val = value ? value : "--"}
      <tr class="border-b">
        <th scope="row" class="py-4 font-medium">{label}</th>
        <td class="font-regular py-4 pl-2 text-a-gray-500">{val}</td>
      </tr>
    {/each}
  </tbody>
</table>
