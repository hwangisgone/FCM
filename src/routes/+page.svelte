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


	let selectedColList = [];
	let selectedLabel = "";

	// MY CODEEEEEEEEEEE
	let C = 0;
	let m = 0;
	let eps = 0;
	let max_iteration = 0;

	let FCMdata: Array<any> = [];
	let validation_metrics = {};
	let centrs = [];
	let U_semisupervised = [];

	$: console.log(selectedColList);

	let gotData = false;

	const handleRUN = () => {
		isLoading = true;
		FCMdata = [];
		chartOptions = {};

		const U_ssfiltered = U_semisupervised.filter(obj => {
			// Check if any cluster value is not equal to 0
			return Object.keys(obj).some(key => key !== 'index' && obj[key] !== 0);
		});

		eel?.marketing_campaign(C, m, eps, max_iteration, selectedColList, selectedLabel, U_ssfiltered)(result => {
			isLoading = false;
			gotData = true;

			FCMdata = result.data;
			validation_metrics = result.metrics;
			centrs = result.centroids;
		});
	// const chart = Highcharts.chart(chartOptions);
	}

	let selectedX = "";
	let selectedY = "";
	let FCMclusterpoints = [];

	const setChartOptions = () => {
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
					text: selectedX
				}
			},
			yAxis: {
				title: {
					text: selectedY
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
						pointFormat: selectedX + ': {point.x}<br/>' + selectedY + ': {point.y}'
					},
				},
				series: {
					turboThreshold: 100000
				}
			},
			series: FCMclusterpoints
		};
	}

	const handleDRAW = () => {
		FCMclusterpoints.length = 0; // Empty the drawing series

		// Drawing points
		for (let i = 0; i < centrs.length; i++) {
			const key = centrs[i].name;

			const str_clr = defined_colors[i % defined_colors.length]
			const clusterpoint = FCMdata.map(
				p => { return {x: p[selectedX], y: p[selectedY], color: str_clr + p[key] + ')'} 
			});

			const centerX = Math.round(centrs[i][selectedX] * 100) / 100
			const centerY = Math.round(centrs[i][selectedY] * 100) / 100

			FCMclusterpoints.push({
				data: clusterpoint, 
				name: key, 
				color: str_clr + '1)', 
				zIndex: 0,
				id: key,
				enableMouseTracking: false
			});
			FCMclusterpoints.push({
				data: [[centerX, centerY]], 
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
					format: 'Y: {y}</br>X: {x}',
					y: -10
				}
			});
		}

		//		console.log(FCMclusterpoints);
		theChart = theChart;
		setChartOptions();
	}

	let initSS = false;
	let selectedIndex = false;
	let previousPoint = null;

	const initialDRAW = () => {
		isLoading = true;
		FCMdata = [];


		eel?.get_original_df(C, selectedColList)(result => {
			isLoading = false;
			initSS = true;
			FCMdata = result.data;
			U_semisupervised = result.U_s;
			
			// Empty the drawing series
			FCMclusterpoints.length = 0; 
			// Drawing points
			const clusterpoint = FCMdata.map(
				p => { return {x: p[selectedX], y: p[selectedY], index: p['index']} 
			});


			FCMclusterpoints.push({
				data: clusterpoint, 
				name: 'Point', 
				color: '#111122', 
				zIndex: 0,
				enableMouseTracking: true,
				allowPointSelect: true,
				point: {
					events: {
						click: function() {
							// if(previousPoint)
							// 	previousPoint.update({color: previousPoint.originalColor});
							// Set this points color to black
							this.update({color: 'red', originalColor: this.color});
							// Make it our previous point
							selectedIndex = this.index;
							// console.log("Index = " + this.index);
							// console.log(FCMdata[this.index]);
							// previousPoint = this;
						}
					}
				}
			});


console.log(FCMclusterpoints);
			theChart = theChart;
			setChartOptions();

				console.log("wtf?");
		});
	}

	const maybeDRAW = () => {
		if (selectedX != "" && selectedY != "") {
			if (centrs.length == 0) {
				initialDRAW();
			} else {
				handleDRAW();
			}
		}
	}

	import FloatInput from 	'./comp/FloatInput.svelte';
	import IntInput from 	'./comp/IntInput.svelte';
	import GetFileColumns from 	'./comp/GetFileColumns.svelte';

	import CentersTable from './comp/detached/CentersTable.svelte';
	import DrawWindow from './comp/detached/DrawWindow.svelte';
	import AssignPointValue from './comp/detached/AssignPointValue.svelte';

	import MetricDisplay from './comp/MetricDisplay.svelte';
	import Chart from './comp/Chart.svelte';

	$: FCMInputCondition = 
		C > 0 && m > 0 && max_iteration > 0 
		&& selectedColList.length > 1  // At least 2 columns
		&& initSS;  // Already drawn the graph once

	// import highchartsAction, { chartPointer } from './hcaction';

	let chartOptions = {};
	let theChart = { series: [] };
</script>




<div class="flex h-screen">
	<!-- Left Navigation Bar -->
	<div class="w-1/5 bg-base-300 rounded-r-lg p-3">
		<!-- Bind: Two-way binding of prop -->
		<GetFileColumns bind:selectedColList bind:selectedLabel/>
		<!-- Pass prop down one-way -->
		<DrawWindow {selectedColList} drawFunction={maybeDRAW} bind:selectedX bind:selectedY />

		<IntInput text="C = "	bind:inputValue={C} />
		<FloatInput text="m = "	bind:inputValue={m} />
		<FloatInput text="ε (eps) = "	bind:inputValue={eps} />
		<IntInput text="Max iteration: "	bind:inputValue={max_iteration} />


		<AssignPointValue bind:U_semisupervised index={selectedIndex} />

		<div class="grid grid-cols-1 gap-4 my-4 justify-items-end">
			<button disabled={!FCMInputCondition}
				type="button"
				on:click={() => {handleRUN(); } }
				class="btn btn-accent">Performs clustering</button
			>
		</div>
			<!-- <a href="/" class="underline mt-4">Back to home</a> -->
	</div>

		<!-- Main Content Area -->
	<div class="w-4/5 bg-base-100 p-3">
		<div class="w-full flex flex-col flex-wrap justify-center items-center pb-4 overflow-x-hidden">
			<h1 class="text-3xl">Fuzzy C-means clustering (FCM)</h1>
		</div>
		<!-- <div id="chart-container" class="border border-primary rounded-md" use:highchartsAction={chartOptions}></div> -->
		<Chart bind:config={chartOptions} bind:chart={theChart}/>

		
		<CentersTable bind:chart={theChart} />

		{#if isLoading}
			<Spinner />
		{/if}

		<MetricDisplay bind:input_metrics={validation_metrics} />
	</div>
</div>
