<script lang="ts">
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

	$: console.log(selectedLabel);
</script>


<div class="grid gap-4 grid-cols-1 my-4">
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


	<div class="flex flex-col h-[25vh] rounded-xl border-secondary border shadow-md overflow-hidden">
		<div class="bg-secondary text-secondary-content font-semibold flex px-2 justify-between">
			<span>Selected for clustering: </span>
			<div class="pr-6">{selectedColList.length}</div>
		</div>
		<div class="overflow-y-scroll bg-base-100 grow">
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

			{#if cols.length == 0} 
				<div class = "w-full h-full text-center bg-base-300 p-6 text-xl">No file selected</div>
			{:else}
	<div class="flex justify-between p-2 gap-2 w-full">
		<span class="text-base font-medium">Labeled data?</span>

		<select class="select select-bordered select-accent grow select-xs"
			bind:value={selectedLabel} >
			<option value="">None</option>
			{#each cols as value}
				<option {value}>{value}</option>
			{/each}
		</select>
	</div>
			{/if}		
		</div>
	</div>
</div>