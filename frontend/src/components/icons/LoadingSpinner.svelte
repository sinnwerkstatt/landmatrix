<script lang="ts">
  interface Props {
    class?: string
  }

  let { class: className = "" }: Props = $props()
</script>

<div class="loadingspinner {className}"></div>

<style>
  .loadingspinner {
    display: inline-block;
    width: 1em;
    height: 1em;
    border: 0.125em solid #eee;
    border-top-color: #bbb;
    border-radius: 50%;
    animation: loadingspin 1s linear infinite;
  }

  @keyframes loadingspin {
    100% {
      transform: rotate(360deg);
    }
  }
</style>
