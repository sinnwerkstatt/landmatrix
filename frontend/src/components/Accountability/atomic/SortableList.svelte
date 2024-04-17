<script lang="ts">
    // A component to create sortable lists of SidebarTab elements based
    // on an array of objects containing at least id, name and position information
    import SidebarTab from "./SidebarTab.svelte";

    let container:HTMLElement;

    const placeholder = [
        { id: 1, name: "Element 1", position: 0 },
        { id: 2, name: "Element 2", position: 1 },
        { id: 3, name: "Element 3", position: 2 }
    ];

    export let items: { id: number, name: string, position?: number }[] = placeholder;

    items = items.sort((a, b) => a && b ? a.position - b.position : -1)

    let refs:[HTMLElement] | [] = []

    let draggedItem:HTMLElement | null = null;

    function handleDragstart(e, i) {
        refs[i].style.opacity = "0.4";
        draggedItem = refs[i];
    }

    function handleDragend(e, i) {
        refs[i].style.opacity = "1";
        updatePosition(container);
        draggedItem = null;
    }

    function handleDragover(e, container:HTMLElement) {
        const afterElement = getDragAfterElement(container, e.clientY);
        if (afterElement == null) {
            container.appendChild(draggedItem);
        } else {
            container.insertBefore(draggedItem, afterElement);
        }
    }

    function getDragAfterElement(container, y) {
        const draggableElements = refs.filter(ref => ref !== draggedItem)
                                      .filter(ref => ref.parentElement == container)

        return draggableElements.reduce((closest, child) => {
            const box = child.getBoundingClientRect();
            const offset = y - box.top - box.height / 2;
            if (offset < 0 && offset > closest.offset) {
                return { offset: offset, element: child }
            } else {
                return closest;
            }
        }, { offset: Number.NEGATIVE_INFINITY }).element;
        
    }

    function updatePosition(container:HTMLElement) {
        const elements = [...container.querySelectorAll("li")];
        const ids = elements.map(e => Number(e.id));

        ids.forEach((id, i) => {
            const index = items.findIndex(e => e.id === id);
            items[index].position = i;
        });
    }

</script>

<ul class="flex flex-col gap-2" 
    on:dragover|preventDefault={(e) => {handleDragover(e, container)}} bind:this={container}>
    {#each items as { id, name, position }, i}
        <li bind:this={refs[i]} {id} class="select-none" style="opacity: 1;"
            draggable="false"
            on:dragstart={(e) => {handleDragstart(e, i)}} on:dragend={(e) => {handleDragend(e, i)}} >

            <SidebarTab {id} label={name} handle={true} menu={true} on:edit on:bookmark />

        </li>
    {/each}
</ul>