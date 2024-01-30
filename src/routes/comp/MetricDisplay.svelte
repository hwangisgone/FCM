<script>
	export let input_metrics = {};
	let new_metrics = {};
	let old_metrics = {};

	$: calcDiffCondition(input_metrics);

	function calcDiffCondition(input) {
		old_metrics = new_metrics;
		new_metrics = input;

		if (Object.keys(old_metrics).length === 0) return;

		for (const key in new_metrics) {	// New metrics may have new keys
			if (key in old_metrics) {		// Only do it when both have keys
				new_metrics[key].condition = 
					(new_metrics[key].result - old_metrics[key].result) 
						* Math.sign(new_metrics[key].mindiff) > new_metrics[key].mindiff;

				new_metrics[key].diff = Math.round((new_metrics[key].result/old_metrics[key].result) * 10000 - 10000) / 100;
				if (Math.sign(new_metrics[key].diff) > 0) {
					new_metrics[key].diff = "+".concat(new_metrics[key].diff);
				}
			}
		}

		// console.log(new_metrics);
	}
</script>


{#each Object.keys(new_metrics) as key}
	<div> <div class="font-semibold">{new_metrics[key].name}: </div>
		{#if Object.keys(old_metrics).length !== 0}
			<div class:better-metric={new_metrics[key].condition}>
				{new_metrics[key].result}
				{#if new_metrics[key].condition}📈 
					({new_metrics[key].diff}%)
				{/if}
			</div>
		{:else}
			<div>{new_metrics[key].result}</div>
		{/if}
	</div>
{/each}

<style>
	.better-metric {
		@apply text-success font-medium;
	}
</style>