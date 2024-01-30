<script lang='ts'>
	import Detached from 	'./Detached.svelte';

	export let U_semisupervised = [];
	export let index = 0;

	const generator = (idx) => {
		console.log(U_semisupervised);
		const result = [];
		if (U_semisupervised.length > 0) {
			const point = U_semisupervised[idx];
			Object.keys(point).forEach(key => {
				if (key !== 'index') {
					const item = { name: key, percentage: point[key] };
					result.push(item);
				}
			});
		}
		return result;
	}

	$: sliders = generator(index);
	
	const handleInput = (event) => {
		const changedSlider = event.target;
		const sliderName = changedSlider.dataset["name"]

		const thisSlider = sliders.find((slider) => slider.name === sliderName)
		const currentValue = thisSlider.percentage

		const newValue = Number(changedSlider.value);
		const difference = newValue - currentValue;

		thisSlider.percentage = newValue;

		if (difference < 0) {
			U_semisupervised[index][sliderName] = thisSlider.percentage;
			sliders = sliders;
			return;
		}
		
		const otherSliders = sliders.filter(slider => slider.name !== sliderName)
		const partialSum = otherSliders.reduce((sum, slider) => sum += slider.percentage, 0)
		const normaliser = (partialSum - difference) / partialSum

		sliders.forEach(slider => {
			if (slider.name !== sliderName) {
				if(partialSum > 0) {
					slider.percentage = slider.percentage * normaliser				
				} else {
					slider.percentage = -difference / otherSliders.length
				}
			}

			U_semisupervised[index][slider.name] = slider.percentage;
			console.log(U_semisupervised[index]);
			console.log(slider.name + " " + index + " " + slider.percentage);
		})

		sliders = sliders;
	}

</script>

<Detached text="Semi-supervised points" wStart=0.7 hStart=0.65>
	{#each sliders as {name, percentage}}
	<div>
		<input type="range" min="0" max="1" step="0.01" data-name={name} value={percentage} on:input={handleInput} />
		<span>{Math.max(percentage.toFixed(2), 0)}</span>
		<!-- 		Math.max to prevent -0 -->
	</div>
	{/each}
</Detached>