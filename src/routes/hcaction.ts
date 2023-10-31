import Highcharts from 'highcharts';

export let chartPointer = { series: [] };

export default (node: HTMLElement, config: Highcharts.Options) => {
	const redraw = true;
	const oneToOne = true;
	const chart = Highcharts.chart(node, config);
	chartPointer = chart;

	const resizeObserver = new ResizeObserver(() => {
		chart.reflow();
	});

	resizeObserver.observe(node);

	return {
		update(config: Highcharts.Options) {
			chart.update(config, redraw, oneToOne);
		},
		destroy() {
			resizeObserver.disconnect();
			chart.destroy();
		}
	};
};