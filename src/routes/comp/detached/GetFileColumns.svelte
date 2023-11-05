<script lang="ts">
	import Detached from 	'./Detached.svelte';

	export let selectedColList = [];
	let cols = [];

	let eel = window.eel;
	// eel?.set_host('ws://localhost:8888');

	const getFILE = () => {
		eel?.load_data_csv()(columns => {
			console.log(columns);
			cols = columns;
		});
	}
</script>

<button
	type="button"
	on:click={getFILE}
	class="mt-4 rounded-lg btn btn-secondary">Get file</button
>

<Detached text="Selected columns" wStart=0.4 hStart=0.8>
	<div class="overflow-y-scroll max-h-72 grid grid-cols-1">
		<div class="bg-secondary text-secondary-content font-semibold flex px-2 justify-between">
			<span>Total</span>
			<div class="pr-3">0</div>
		</div>
		{#each cols as column}
			<div class="form-control px-2 hover:bg-base-300">
				<label class="label">
					<span class="label-text">{column}</span>
					<input type="checkbox" class="checkbox" bind:group={selectedColList} value={column}/>
				</label>
			</div>
		{/each}
	</div>
</Detached>