<script lang="ts">
  // import JSONFieldMixin from "../JSONField";
  import { onMount } from "svelte";
  import { _ } from "svelte-i18n";
  import type { FormField } from "../fields";
  import LowLevelDateYearField from "./LowLevelDateYearField.svelte";
  import LowLevelDecimalField from "./LowLevelDecimalField.svelte";

  export let formfield: FormField;
  export let value;
  let current = -1;

  function updateEntries() {
    // value = value.map((v, i) => {
    //   let current = i === this.current ? { current: true } : {};
    //   delete v.current;
    //   return { ...v, ...current };
    // });
    // this.$emit("input", this.filteredVals);
  }
  onMount(() => (value === null ? (value = []) : value));
</script>

<div class="whitespace-nowrap">
  {JSON.stringify(value)}
  <table class="w-100">
    <thead>
      <tr>
        <th>{$_("Current")}</th>
        <th>{$_("Date")}</th>
        <th>{$_("Area (ha)")}</th>
        <th />
      </tr>
    </thead>
    <tbody>
      <!--{#each value as val, i}-->
      <!--        <tr v-for="(val, i) in vals" :key="i" :class="{ 'is-current': val.current }">-->
      <!--          <td class="text-center" @click="updateCurrent(i)">-->
      <!--            <div class="form-check form-check-inline">-->
      <!--              <input-->
      <!--                :id="`${formfield.name}_current_${i}`"-->
      <!--                v-model="current"-->
      <!--                :name="`${formfield.name}_current`"-->
      <!--                :required="vals.length > 0 && (vals[0].date || vals[0].area)"-->
      <!--                class="form-check-input"-->
      <!--                type="radio"-->
      <!--                :value="i"-->
      <!--              />-->
      <!--            </div>-->
      <!--          </td>-->

      <!--        <td>-->
      <!--          <LowLevelDateYearField-->
      <!--            bind:value={val.date}-->
      <!--            required={formfield.required}-->
      <!--            on:input={updateEntries}-->
      <!--          />-->
      <!--        </td>-->
      <!--        <td>-->
      <!--          <LowLevelDecimalField-->
      <!--            bind:value={val.area}-->
      <!--            required={formfield.required}-->
      <!--            unit="ha"-->
      <!--            on:input={updateEntries}-->
      <!--          />-->
      <!--        </td>-->

      <!--          <td class="buttons">-->
      <!--            <a class="btn" @click.stop="addEntry"><i class="fa fa-plus"></i></a>-->
      <!--            <a-->
      <!--              :class="{ disabled: vals.length <= 1 }"-->
      <!--              class="btn"-->
      <!--              @click.stop="removeEntry(i)"-->
      <!--            >-->
      <!--              <i class="fa fa-minus"></i-->
      <!--            ></a>-->
      <!--          </td>-->
      <!--        </tr>-->
      <!--{/each}-->
    </tbody>
  </table>
</div>
