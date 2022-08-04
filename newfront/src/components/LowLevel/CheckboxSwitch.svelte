<script lang="ts">
  export let checked = false;
  export let title = "";
</script>

<label class="flex items-center gap-1 mb-1 cursor-pointer {$$props.class}" {title}>
  <input type="checkbox" bind:checked on:change|preventDefault />
  <span class={checked ? "text-orange" : "text-gray-500"}><slot /></span>
</label>

<style>
  input {
    appearance: none;
    margin: 0;
    background-color: #c9c9c9;
    display: grid;
    place-content: center;
    width: 2.25em;
    height: 1.25em;
    transition: background-color 100ms ease-in-out;
    cursor: pointer;
  }
  input:checked {
    background-color: var(--color-lm-orange);
  }

  input::before {
    content: "";
    width: 1em;
    height: 1em;
    transform: translateX(-50%);
    transition: 100ms transform ease-in-out;
    box-shadow: inset 1.15em 1.15em white;
    cursor: pointer;
  }

  input:checked::before {
    transform: translateX(50%);
  }
</style>
