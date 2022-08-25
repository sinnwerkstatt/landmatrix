<div class="relative flex h-full w-full items-center justify-center {$$props.class}">
  <div class="lds-facebook relative -mt-10 block h-20 w-20">
    <div class="n n1" />
    <div class="n n2" />
    <div class="n n3" />
  </div>
</div>

<style lang="postcss">
  .n {
    @apply absolute inline-block w-4 bg-orange;
    animation: lds-facebook 1s cubic-bezier(0, 0.5, 0.5, 1) infinite;
  }
  .n1 {
    left: 8px;
    animation-delay: -0.24s;
  }

  .n2 {
    left: 32px;
    animation-delay: -0.12s;
  }

  .n3 {
    left: 56px;
    animation-delay: 0s;
  }

  @keyframes lds-facebook {
    0% {
      top: 8px;
      height: 104px;
      background: #fff;
    }
    50%,
    100% {
      top: 24px;
      height: 72px;
    }
  }
</style>
