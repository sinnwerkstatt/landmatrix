<script lang="ts">
  import { _ } from "svelte-i18n";

  export let value: number;
  export let name: string;
  export let unit = "";
  export let required = false;
  export let max: number;
  export let min: number;
  export let decimals = 2;

  $: step = 1 / 10 ** decimals;

  // Nice to have: on up/down-arrow: change the number where the cursor is on..
  // methods: {
  //   updowndings(e) {
  //     if (["ArrowUp", "ArrowDown"].includes(e.key)) {
  //       e.preventDefault();
  //       console.log(e.key);
  //       console.log(e.target.selectionStart);
  //       console.log(e.target);
  //     }
  //   },
  // },

  $: placeholder = min && max ? `${min} – ${max}` : step === 1 ? "" : "123.45";

  // },
  // watch: {
  //   value(newValue) {
  //     this.val = JSON.parse(JSON.stringify(newValue));
  //   },
  //   val(v) {
  //     if (!v && v !== 0) {
  //       this.$emit("input", null);
  //       return;
  //     }
  //     if (this.maxValue && v > this.maxValue) this.val = this.maxValue;
  //     if (this.minValue && v < this.minValue) this.val = this.minValue;
  //
  //     let v_str = v.toString();
  //     if (v_str.includes(".")) {
  //       let number = v_str.split(".");
  //       let decs = number[1];
  //       decs = decs.length > this.decimals ? decs.slice(0, this.decimals) : decs;
  //       v_str = `${number[0]}.${decs}`;
  //       this.val = v_str;
  //     }
  //     this.$emit("input", +v);
  //   },
  // },
</script>

<div class="whitespace-nowrap flex">
  <input
    bind:value
    type="number"
    class="inpt"
    {placeholder}
    {required}
    {min}
    {max}
    {step}
    {name}
  />
  {#if unit}
    <div
      class="flex justify-center items-center border border-l-0 border-gray-300 py-1.5 px-3 bg-gray-200 text-gray-600"
    >
      {$_(unit)}
    </div>
  {/if}
</div>
