<script lang="ts">
  interface Props {
    class?: string
  }

  let { class: className = "inline size-4" }: Props = $props()
</script>

<svg
  xmlns="http://www.w3.org/2000/svg"
  viewBox="0 0 448 512"
  class={className}
  fill="currentColor"
>
  <!--! Font Awesome Pro 6.0.0 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2022 Fonticons, Inc. -->
  <path
    d="M224 304c70.75 0 128-57.25 128-128V65.88c0-13.38-8.25-25.38-20.75-30L246.5 4.125C239.3 1.375 231.6 0 224 0S208.8 1.375 201.5 4.125L116.8 35.88C104.3 40.5 96 52.5 96 65.88V176C96 246.8 153.3 304 224 304zM184 71.63c0-2.75 2.25-5 5-5h21.62V45c0-2.75 2.25-5 5-5h16.75c2.75 0 5 2.25 5 5v21.62H259c2.75 0 5 2.25 5 5v16.75c0 2.75-2.25 5-5 5h-21.62V115c0 2.75-2.25 5-5 5H215.6c-2.75 0-5-2.25-5-5V93.38H189c-2.75 0-5-2.25-5-5V71.63zM144 160h160v16C304 220.1 268.1 256 224 256S144 220.1 144 176V160zM327.2 312.8L224 416L120.8 312.8c-69.93 22.3-120.8 87.25-120.8 164.6C.0006 496.5 15.52 512 34.66 512H413.3c19.14 0 34.66-15.46 34.66-34.61C447.1 400.1 397.1 335.1 327.2 312.8z"
  />
</svg>
