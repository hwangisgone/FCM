<script>
  export let inputValue = 0; // Initialize with a default value

  function handleInputChange(event) {
    // Parse the input value as an integer
    inputValue = parseInt(event.target.value, 10);
  }

  $: console.log(inputValue);
</script>

<input
  type="number"
  class="input input-bordered input-primary rounded-lg"
  bind:value={inputValue}
  on:input={handleInputChange}
/>