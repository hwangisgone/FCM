<script>
	export let input_metrics = {};
	let new_metrics = {};
	let old_metrics = {};

	$: calcDiffCondition(input_metrics);

	function calcDiffCondition(input) {
		old_metrics = new_metrics;
		new_metrics = input;

		if (Object.keys(old_metrics).length === 0) return;

		for (const key in new_metrics) {
			new_metrics[key].condition = 
				(new_metrics[key].result - old_metrics[key].result) 
					* Math.sign(new_metrics[key].mindiff) > new_metrics[key].mindiff;

			new_metrics[key].diff = Math.round((new_metrics[key]/old_metrics[key])*10000 - 10000) / 100;
		}

		console.log(new_metrics);
	}

</script>


{#each Object.keys(new_metrics) as key}
	<div> {new_metrics[key].name}: 
		{#if Object.keys(old_metrics).length !== 0}
			<div class:better-metric={new_metrics[key].condition}>
				{new_metrics[key].result}
				{#if new_metrics[key].condition}📈 
					({new_metrics[key].diff})%
				{/if}
			</div>
		{:else}
			<div> {new_metrics[key]}</div>
		{/if}
	</div>
{/each}

<style>
	.better-metric {
		@apply text-success font-medium;
	}
</style>