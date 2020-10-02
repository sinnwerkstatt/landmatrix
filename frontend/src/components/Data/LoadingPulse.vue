<template>
  <div class="lm-loading-container">
  <div class="lds-facebook">
    <div></div>
    <div></div>
    <div></div>
  </div>
  </div>
</template>

<style lang="scss">
  .lm-loading-container {
    z-index: 500000;
    position: absolute;
    bottom: -20px;
    left: 50%;
  }
  .lds-facebook {
    display: inline-block;
    position: relative;
    width: 80px;
    height: 80px;

    div {
      display: inline-block;
      position: absolute;
      left: 8px;
      width: 16px;
      background: #ffffff;
      animation: lds-facebook 1.2s cubic-bezier(0, 0.5, 0.5, 1) infinite;

      &:nth-child(1) {
        left: 8px;
        animation-delay: -0.24s;
      }

      &:nth-child(2) {
        left: 32px;
        animation-delay: -0.12s;
      }

      &:nth-child(3) {
        left: 56px;
        animation-delay: 0s;
      }
    }

    @keyframes lds-facebook {
      0% {
        top: 8px;
        height: 64px;
        background: #fc941f;
      }
      50%,
      100% {
        top: 24px;
        height: 32px;
      }
    }
  }
</style>
