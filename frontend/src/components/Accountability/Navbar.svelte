<script lang="ts">
    import Logo from "$components/Accountability/icons/Logo.svelte"
    import IconList from "$components/Accountability/icons/IconList.svelte"
    import IconToDo from "$components/Accountability/icons/IconToDo.svelte"
    import IconDocs from "$components/Accountability/icons/IconDocs.svelte"

    import NavbarItem from "$components/Accountability/atomic/NavbarItem.svelte"
</script>

<div class="h-full p-6 bg-white flex flex-col flex-nowrap items-center justify-between">
    <!-- Top section -->
    <div>
        <Logo />
        <div class="mt-10 flex flex-col flex-nowrap gap-4">
            <NavbarItem label="Deals" href="/accountability/deals/">
                <span slot="icon"><IconList /></span>
            </NavbarItem>
            <NavbarItem label="To Do" href="/accountability/todo/">
                <span slot="icon"><IconToDo /></span>
            </NavbarItem>
            <NavbarItem label="Doc" href="/accountability/doc/">
                <span slot="icon"><IconDocs /></span>
            </NavbarItem>
        </div>
    </div>

    <!-- Bottom section -->
    <div>
        MG
    </div>
</div>