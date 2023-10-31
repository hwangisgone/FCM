<script>
  export let inputValue = 0.0;
  
  function handleInputChange(event) {
    // Parse the input value as an integer
    inputValue = parseFloat(event.target.value, 10);
  }

  // // Regular expression to match float numbers
  // const floatRegex = /^[+-]?\d+(\.\d+)?$/;

  // function handleInput(event) {
  //   const newValue = event.target.value;
  //   if (floatRegex.test(newValue) || newValue === "") {
  //     inputValue = newValue;
  //   }
  // }
</script>

<input
  type="number"
  class="input input-bordered input-primary rounded-lg w-100"
  bind:value={inputValue}
  step="any"
/>

<style>
  /* You can add Tailwind classes for styling here */
</style>