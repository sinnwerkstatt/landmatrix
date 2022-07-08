<script lang="ts">
  export let checked = false;
  export let label = "label";
</script>

<div class="flex {$$props.class}">
  <label class="switch align-middle relative block flex justify-center items-center">
    <input class="opacity-0 w-0 h-0" type="checkbox" bind:checked on:input on:change />
    <span
      class="slider transition-transform delay-300 bg-gray-300 absolute cursor-pointer inset-0"
    />
  </label>
  <p class={checked ? "text-orange" : "text-gray-500"}>{label}</p>
</div>

<style>
  /* The switch - the box around the slider */
  .switch {
    font-size: 1rem;
    width: 2.5em;
    height: 1.375em;
    margin: 0 0.3125em 0.3125em 0;
  }

  /* The slider */
  .slider {
    --color-highlight: orange;
    transition: transform 400ms, background-color 400ms;
  }

  .slider::before {
    position: absolute;
    content: "";
    height: 1.125em;
    width: 1.125em;
    left: 0.125em;
    bottom: 0.125em;
    background-color: white;
    transition: transform 100ms;
  }

  input:focus + .slider {
    border: 1px solid black;
  }
  input:checked + .slider {
    background-color: var(--color-highlight);
  }

  input:checked:disabled + .slider {
    opacity: 0.3;
    cursor: not-allowed;
  }

  input:focus + .slider {
    box-shadow: 0 0 1px var(--color-highlight);
  }

  input:checked + .slider:before {
    transform: translateX(1.125em);
  }
</style>
