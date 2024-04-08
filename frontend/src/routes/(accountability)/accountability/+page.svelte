<script lang="ts">
    import Button from "$components/Accountability/Button.svelte";

    function sayHi() {
        alert("Hi!")
    }
</script>

Hello Accountability!

<Button style="primary" type="outline" size="sm" notification={10} on:click={sayHi} />
<Button style="primary" type="outline" size="base" notification={10} on:click={sayHi} />
<Button style="primary" type="outline" size="lg" notification={10} on:click={sayHi} />