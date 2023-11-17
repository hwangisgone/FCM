<script lang="ts">
	export let text = "Title";
	export let wStart = 0.5;
	export let hStart = 0.8;

	let moving = false;
	let left = window.innerWidth * wStart;
	let top = window.innerHeight * hStart;

	function onMouseDown() {
		moving = true;
	}
	
	function onMouseMove(e) {
		if (moving) {
			left += e.movementX * 0.8;
			top += e.movementY * 0.8;
		}
	}
	
	function onMouseUp() {
		moving = false;
	}

	let collapse = false;
</script>

<svelte:window on:mouseup={onMouseUp} on:mousemove={onMouseMove} />

<div class="card card-compact bg-base-100 shadow-xl border border-primary absolute overflow-hidden z-10 " 
	style="left: {left}px; top: {top}px;">
	<!-- <figure><img src="/images/stock/photo-1606107557195-0e29a4b5b4aa.jpg" alt="Shoes" /></figure> -->
	<!-- Title -->
	<div class="bg-primary drag-mouse text-base-200 text-center font-semibold px-4" 
		on:mousedown={onMouseDown}>{text}
		<input type="checkbox" class="checkbox" bind:checked={collapse} />
	</div>

	<div class:block={!collapse} class:none={collapse}>
		<slot />
	</div>
</div>


<style>
	.drag-mouse {
		user-select: none;
		cursor: move;
/*		position: absolute;*/
	}
</style>