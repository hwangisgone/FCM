<script lang="ts">
	import Spinner from '$lib/Spinner.svelte';

	let eel = window.eel;
	eel?.set_host('ws://localhost:8888');

	let isLoading = false;

	// MY CODE
function Hex2RGBA(hexCode){
	var hex = hexCode.replace('#', '');

	if (hex.length === 3) {
		hex = hex[0] + hex[0] + hex[1] + hex[1] + hex[2] + hex[2];
	}

	var r = parseInt(hex.substring(0,2), 16),
		g = parseInt(hex.substring(2,4), 16),
		b = parseInt(hex.substring(4,6), 16);
	
	return 'rgba('+r+','+g+','+b+',';
}

	// 9 clrs
	const defined_colors = ['#058DC7', '#50B432', '#ED561B', '#DDDF00', '#24CBE5', '#64E572', '#FF9655', '#FFF263', '#6AF9C4', '#FF00FF', '#111111'].map(clr => Hex2RGBA(clr));

	// MY CODEEEEEEEEEEE
	let FCMdata: Array<any> = [];
	let C = 0;
	let m = 0;
	let eps = 0;
	let max_iteration = 0;

	let validation_metrics = {};
	let old_metrics = {}
	const metrics_name = {
		'dunn': "Dunn's index: ",
		'davies_bouldin': "Davies-Bouldin index: ",
		'swc': "Silhouette width criterion (SWC): "
	}

	let FCMclusterpoints = [];

	const handleRUN = () => {
		isLoading = true;
		FCMdata = [];
		eel?.marketing_campaign(C, m, eps, max_iteration)(result => {
			FCMclusterpoints.length = 0; // Empty
			FCMdata = result.data;

			old_metrics = validation_metrics;
			validation_metrics = result.metrics;
			let centrs = result.centroids;

			isLoading = false;


			for (let i = 0; i < centrs.length; i++) {
				const key = centrs[i].name;

				const str_clr = defined_colors[i % defined_colors.length]
				const clusterpoint = FCMdata.map(
					p => { return {x: p.x, y: p.y, color: str_clr + p[key] + ')'} 
				});

				FCMclusterpoints.push({
					data: clusterpoint, 
					name: key, 
					color: str_clr + '1)', 
					zIndex: 0,
					id: key,
					enableMouseTracking: false
				});
				FCMclusterpoints.push({
					data: [[centrs[i].x, centrs[i].y]], 
					name: 'Center of ' + key, 
					color: str_clr + '1)',
					marker: {
						fillColor: '#FFFFFF',
						lineColor: '#000000',
						symbol: 'diamond',
						lineWidth: 2,
						radius: 5,
						// states: {
						// 	hover: {
						// 		enabled: true,
						// 		radiusPlus: 5 // Increase the hover interaction range
						// 	}
						// }
					},
					zIndex: 1,
					linkedTo: key,
					dataLabels: {
						enabled: true,
						format: '{y}</br>{x} $',
						y: -10
					}
				});
			}
			
			// for (const key in FCMdata[0]) {
			// 	if (key !== 'x' && key !== 'y') {
			// 		console.log(`i: ${i}, Key: ${key}`);

			// 		const clusterpoint = FCMdata.map(
			// 			p => { return {x: p.x, y: p.y, color: defined_colors[i] + p[key] + ')'} 
			// 		});

			// 		FCMclusterpoints.push({data: clusterpoint, name: key, color: defined_colors[i] + '1)'});

			// 		i++;
			// 		i = i % defined_colors.length;
			// 	}
			// }

			console.log(FCMclusterpoints);
	theChart = theChart;
	chartOptions = { 
		chart: { 
			renderTo: 'chart-container', 
			type: 'scatter',
			zooming: {
				mouseWheel: true
			} 
		},
		title: {
			text: 'Scatter Plot'
		},
		xAxis: {
			title: {
				text: 'Income'
			}
		},
		yAxis: {
			title: {
				text: 'Age'
			}
		},
		legend: {
			enabled: true
		},
		plotOptions: {
			scatter: {
				marker: {
					radius: 2.5,
					symbol: 'circle',
					states: {
						hover: {
							enabled: true,
							lineColor: 'rgb(100,100,100)'
						}
					}
				},
				states: {
					hover: {
						marker: {
							enabled: false
						}
					}
				},
				tooltip: {
					pointFormat: 'Age: {point.y}<br/> Income: {point.x} $'
				},
			},
			series: {
				turboThreshold: 100000
			}
		},
		series: FCMclusterpoints
	};
		});	

	// const chart = Highcharts.chart(chartOptions);
	}

	import FloatInput from './FloatInput.svelte';
	import IntInput from './IntInput.svelte';
	import Detached from './Detached.svelte';
	import Chart from './Chart.svelte';

	$: FCMInputCondition = C > 0 && max_iteration > 0

	// import highchartsAction, { chartPointer } from './hcaction';
		
	let chartOptions = {};
	let theChart = { series: [] };
</script>




<div class="flex h-screen">
	<!-- Left Navigation Bar -->
	<div class="w-1/5 bg-base-300 rounded-r-lg p-3 pt-20">
		<label for="input_C" class="label">
			<span class="label-text">C =</span>
		</label>
		<IntInput id="input_C" bind:inputValue={C} />

		<label for="input_m" class="label">
			<span class="label-text">m =</span>
		</label>
		<FloatInput id="input_m" bind:inputValue={m} />

		<label for="input_eps" class="label">
			<span class="label-text">ε (eps) = </span>
		</label>
		<FloatInput id="input_eps" bind:inputValue={eps} />

		<label for="input_max_i" class="label">
			<span class="label-text">Max iteration: </span>
		</label>
		<IntInput id="input_max_i" bind:inputValue={max_iteration} />

		<div class="flex justify-end">
			<button disabled={!FCMInputCondition}
				type="button"
				on:click={handleRUN}
				class="my-4 rounded-lg btn btn-secondary">Load data 2</button
			>
		</div>

			<a href="/" class="underline mt-4">Back to home</a>
	</div>

		<!-- Main Content Area -->
	<div class="w-4/5 bg-base-100 p-3">
		<div class="w-full flex flex-col flex-wrap justify-center items-center pb-4 overflow-x-hidden">
			<h1 class="text-3xl">Fuzzy C-means clustering (FCM)</h1>
		</div>
		<!-- <div id="chart-container" class="border border-primary rounded-md" use:highchartsAction={chartOptions}></div> -->
		<Chart bind:config={chartOptions} bind:chart={theChart}/>

		<Detached bind:chart={theChart} />

		{#if isLoading}
			<Spinner />
		{/if}

		{#each Object.keys(validation_metrics) as key}
		  <div> {metrics_name[key]}
			{#if Object.keys(old_metrics).length !== 0}
				{#if key == 'davies_bouldin'}
					<div class:better-metric={validation_metrics[key] - old_metrics[key] < -0.01}>
						{validation_metrics[key]}
						{#if validation_metrics[key] - old_metrics[key] < -0.01}📈 
						({Math.round((validation_metrics[key] * 10000)/old_metrics[key] - 10000) / 100}%){/if}
					</div>
				{:else}
					<div class:better-metric={validation_metrics[key] - old_metrics[key] > 0.0001}>
						{validation_metrics[key]}
						{#if validation_metrics[key] - old_metrics[key] > 0.0001}📈 
						(+{Math.round((validation_metrics[key] * 10000)/old_metrics[key] - 10000) / 100}%){/if}
					</div>
				{/if}
			{:else}
				<div> {validation_metrics[key]}</div>
			{/if}
		  </div>
		{/each}
	</div>
</div>

<style>
	.better-metric {
		@apply text-success font-medium;
	}
</style>
