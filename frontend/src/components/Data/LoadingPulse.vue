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
    z-index: 100;
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(1, 0, 0, 0.3);
    display: flex;
    align-items: center;
    justify-content: center;
  }
  .lds-facebook {
    display: inline-block;
    position: relative;
    width: 80px;
    height: 80px;
    margin-top: -40px;

    div {
      display: inline-block;
      position: absolute;
      left: 8px;
      width: 16px;
      background: var(--color-lm-orange);
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
        height: 104px;
        background: #fff;
      }
      50%,
      100% {
        top: 24px;
        height: 72px;
      }
    }
  }
</style>
