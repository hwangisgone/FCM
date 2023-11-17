<script lang="ts">
	import Detached from 	'./Detached.svelte';

	export let selectedColList = [];
	export let selectedX = "";
	export let selectedY = "";
	export let handleDRAW;

</script>

<Detached text="Drawing" wStart=0.22 hStart=0.7>
	<div class="p-2 grid grid-cols-5 gap-2">
		<span>X:</span>
		<select class="select select-bordered select-secondary select-xs w-32 col-span-4"
			bind:value={selectedX} >
			{#each selectedColList as value}
				{#if value !== selectedY}
					<option {value}>{value}</option>
				{/if}
			{/each}
		</select>

		<span>Y:</span>
		<select class="select select-bordered select-secondary select-xs w-32 col-span-4"
			bind:value={selectedY} >
			{#each selectedColList as value}
				{#if value !== selectedX}
					<option {value}>{value}</option>
				{/if}
			{/each}
		</select>

		<button disabled={!(selectedX != "" && selectedY != "")}
			type="button"
			on:click={handleDRAW}
			class="btn btn-primary col-span-5">Draw Graph</button
		>
	</div>
</Detached>