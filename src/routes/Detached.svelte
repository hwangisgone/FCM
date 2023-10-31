<script>
	export let chart = { series: [] }; // Initialize with a default value\

	let moving = false;
	let left = window.innerWidth - 400;
	let top = window.innerHeight - window.innerHeight / 4;;
	let left2 = 0;
	let top2 = 0;

	function onMouseDown(e) {
		moving = true;
	}
	
	function onMouseMove(e) {
		if (moving) {
			left += e.movementX;
			top += e.movementY;
		}
	}
	
	function onMouseUp() {
		moving = false;
	}

	function hoverCenterPoint(i_series) {
		chart.series.forEach(series => {
			series.setState('inactive');
		})
		i_series.setState('hover');
	}

	function hoverNormalAll() {
		chart.series.forEach(series => {
			series.setState('normal');
		})
	}

	// const sortNames = (a, b) => {
	// 	if (a.name < b.name) { return -1; }
	// 	if (a.name > b.name) { return 1; }
	// 	return 0;
	// }
</script>

<svelte:window on:mouseup={onMouseUp} on:mousemove={onMouseMove} />

<div class="card card-compact w-96 bg-base-100 shadow-xl border border-primary absolute z-10" 
	style="left: {left}px; top: {top}px;"
	on:mouseout={() => hoverNormalAll()} on:blur={() => hoverNormalAll()}>
	<!-- <figure><img src="/images/stock/photo-1606107557195-0e29a4b5b4aa.jpg" alt="Shoes" /></figure> -->
	<div class="overflow-hidden rounded-2xl">
	<!-- <h2 class="card-title">Shoes!</h2> -->
		<table class="table table-xs table-pin-rows">
			<thead>
				<tr class="bg-primary drag-mouse text-base-100" on:mousedown={onMouseDown}>
					<th>Cluster</th> 
					<th>X</th> 
					<th>Y</th>
				</tr>
			</thead>
			<tbody>
				{#each chart.series as series}
					{#if series.data.length === 1}
						<tr class="hover" on:mouseover={() => hoverCenterPoint(series)} on:focus={() => hoverCenterPoint(series)} >
							<th>{series.name}</th>
							<th>{series.data[0].x}</th> 
							<th>{series.data[0].y}</th> 
						</tr>
<!-- 					{:else}
						{#each series.data as point}
							<tr class="hover" on:mouseover={() => hoverCenterPoint(point)} on:focus={() => hoverCenterPoint(point)} >
							<th>{series.name}</th>
							<th>{point.x}</th> 
							<th>{point.y}</th> 
						</tr>
					{/each} -->
					{/if}
				{/each}
			</tbody>
		</table>
<!--     <div class="card-actions justify-end">
		<button class="btn btn-primary">Buy Now</button>
	</div> -->
	</div>
</div>


<style>
	.drag-mouse {
		user-select: none;
		cursor: move;
/*		position: absolute;*/
	}
</style>