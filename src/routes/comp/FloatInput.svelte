<script context="module">
	let counter = 0;
</script>

<script>
	export let inputValue = 0.0;
	export let text = "Float input:";
	
	function handleInputChange() {
		// Parse the input value as an float
		// inputValue = parseFloat(event.target.value, 10);
		if (inputValue == null) {
			inputValue = 0.0;
		}
	}

	let elID = "float_input" + counter++;

	// $: console.log("Float: ", inputValue);
</script>

<div class="form-control">
	<label for={elID} class="label">
		<span class="label-text">{text}</span>
	</label>
	<input id={elID}
		type="number"
		class="input input-bordered input-primary rounded-lg w-100"
		min="0.0"
		bind:value={inputValue}
		on:change={handleInputChange}
		step="any"
	/>
</div>