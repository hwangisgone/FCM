<script lang="ts">
	import Detached from 	'./Detached.svelte';
	
	export let chart = { series: [] }; // Initialize with a default value\

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

<Detached text="Cluster centers" wStart=0.45 hStart=0.65>
	<table class="table table-xs table-pin-rows w-72 " on:mouseout={() => hoverNormalAll()} on:blur={() => hoverNormalAll()}>
		<thead>
			<tr class="">
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
				{/if}
			{/each}
		</tbody>
	</table>
</Detached>
