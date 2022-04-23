<div class="w-full h-full flex items-center justify-center relative {$$props.class}">
  <div class="lds-facebook block relative w-20 h-20 -mt-10">
    <div class="n n1" />
    <div class="n n2" />
    <div class="n n3" />
  </div>
</div>

<style>
  .n {
    @apply bg-orange w-4 inline-block absolute;
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
