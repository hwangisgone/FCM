<script>
	import Highcharts from 'highcharts';
	export let config = {}; // Initialize with a default value
	export let chart;

	let HTMLElement;

	const redraw = true;
	const oneToOne = true;
	let drawn = false;


	import { onMount } from 'svelte'
	onMount(() => {
		chart = Highcharts.chart(HTMLElement, config);
		drawn = true;
  });
	// const resizeObserver = new ResizeObserver(() => {
	// 	chart.reflow();
	// });

	// 	resizeObserver.observe(node);

	// 	return {
	// 		update(config: Highcharts.Options) {
	// 			chart.update(config, redraw, oneToOne);
	// 		},
	// 		destroy() {
	// 			resizeObserver.disconnect();
	// 			chart.destroy();
	// 		}
	// 	};
	function updateChart(config) {
		if (drawn) {
			chart.update(config, redraw, oneToOne);
		}
	};

	$: updateChart(config);
</script>

<div id="chart-container" class="border border-primary rounded-md" bind:this={HTMLElement} />


<style>
	#chart-container {
		max-width: 100%;
		margin: auto;
	}
</style>