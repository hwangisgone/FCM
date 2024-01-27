<script lang="ts">
	import Detached from 	'./Detached.svelte';

	export let selectedColList = [];
	export let selectedX = "";
	export let selectedY = "";
	export let drawFunction;


</script>

<Detached text="Graph" wStart=0.075 hStart=0.4>
	<div class="p-2 grid grid-cols-5 gap-2">
		<span>X:</span>
		<select class="select select-bordered select-secondary select-xs w-32 col-span-4"
			bind:value={selectedX} on:change={drawFunction}>
			{#if selectedColList.length == 2}
				<option value=""></option>	
			{/if}
			{#each selectedColList as value}
				{#if value !== selectedY}
					<option {value}>{value}</option>
				{/if}
			{/each}
		</select>

		<span>Y:</span>
		<select class="select select-bordered select-secondary select-xs w-32 col-span-4"
			bind:value={selectedY} on:change={drawFunction}>
			{#each selectedColList as value}
				{#if value !== selectedX}
					<option {value}>{value}</option>
				{/if}
			{/each}
		</select>

		<button disabled={!(selectedX != "" && selectedY != "")}
			type="button"
			on:click={drawFunction}
			class="btn btn-primary col-span-5">Update Graph</button
		>
	</div>
</Detached>