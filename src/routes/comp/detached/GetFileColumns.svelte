<script lang="ts">
	import Detached from 	'./Detached.svelte';

	export let selectedColList = [];
	export let selectedLabel = "";

	let cols = [];
	let eel = window.eel;
	// eel?.set_host('ws://localhost:8888');

	let enableGetFile = true;

	const getFILE = () => {
		eel?.load_data_csv()(columns => {
			console.log(columns);
			if (columns.length > 0) {
				cols = columns;
				enableGetFile = false;
			}
		});
	}

	let isLabeledData = false;

	const resetNoLabel = () => {
		if (!isLabeledData) 
			selectedLabel = "";
	}

	$: console.log(selectedLabel);
</script>


<div class="grid gap-2 grid-cols-1 my-4">
	<div class="flex gap-4 items-center">
		<input type="checkbox" 
			class="toggle toggle-secondary toggle-md -rotate-90 m-0 p-0" 
			bind:checked={enableGetFile}
		/>
		<button
			disabled={!enableGetFile}
			type="button"
			on:click={getFILE}
			class="btn btn-secondary grow">Get file</button
		>
	</div>

	<div class="flex justify-between">
		<span>Labeled data?</span>
		<input type="checkbox" 
			class="toggle toggle-accent toggle-md" 
			bind:checked={isLabeledData} 
			on:change={resetNoLabel}
		/>
	</div>

	{#if isLabeledData}
		<select class="select select-bordered select-accent w-full"
			bind:value={selectedLabel} >
			{#each cols as value}
				<option {value}>{value}</option>
			{/each}
		</select>
	{/if}
</div>

<Detached text="Selected columns" wStart=0.22 hStart=0.2>
	<div class="overflow-y-scroll max-h-64 grid grid-cols-1">
		<div class="bg-secondary text-secondary-content font-semibold flex px-2 justify-between">
			<span>Total</span>
			<div class="pr-3">{selectedColList.length}</div>
		</div>
		{#each cols as column}
			<div class="form-control px-2 hover:bg-base-300">
				<label class="label">
					<span class="label-text pr-2">{column}</span>
					<input type="checkbox" class="checkbox" 
						bind:group={selectedColList} value={column}
					/>
				</label>
			</div>
		{/each}
	</div>
</Detached>