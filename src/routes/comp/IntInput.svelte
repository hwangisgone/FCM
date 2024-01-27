<script context="module">
	let counter = 0;
</script>

<script>
	export let inputValue = 0; // Initialize with a default value
	export let text = "Int input:";

	function handleInputChange() {
		// Parse the input value as an integer
		// inputValue = parseInt(event.target.value, 10);
		if (inputValue == null) {
			inputValue = 0;
		}
	}

	let elID = "int_input" + counter++;

	// $: console.log("Int: ", inputValue);
</script>

<div class="form-control">
	<label for={elID} class="label">
		<span class="label-text">{text}</span>
	</label>
	<input id={elID}
		type="number"
		class="input input-bordered input-primary rounded-lg h-10"
		min="0"
		bind:value={inputValue}
		on:change={handleInputChange}
	/>
</div>