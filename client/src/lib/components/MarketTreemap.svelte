<script lang="ts">
  import { onMount } from 'svelte';
  import * as echarts from 'echarts';

  let chartEl: HTMLDivElement;
  let chart: echarts.ECharts;
  let data = [];

  onMount(async () => {
    //const res = await fetch('http://localhost:8000/data');
    const res = await fetch("https://finsight-p85x.onrender.com/data");

    const raw = await res.json();

    // Sanitize and aggregate Market Cap by Company
    const grouped = raw.reduce((acc, row) => {
      const company = row.Company;
      let value = row["Market Cap(in B USD)"];

      if (!acc[company]) {
        acc[company] = 0;
      }

      if (typeof value === "string") {
        value = String(value).replace(/[^0-9.-]/g, '');
      }

      acc[company] += parseFloat(value) || 0;
      return acc;
    }, {});

    // Format for ECharts
    data = Object.entries(grouped).map(([name, value]) => ({
      name,
      value: +value.toFixed(2)
    }));

    renderChart();
  });

  function renderChart() {
    if (!chartEl || !data.length) return;

    if (!chart) chart = echarts.init(chartEl);
    else chart.clear();

    chart.setOption({
      title: {
        text: 'Market Capitalization by Company',
        left: 'center',
        textStyle: {
          fontSize: 18,
          fontWeight: 'bold',
          color: '#fff'
        }
      },
      tooltip: {
        backgroundColor: '#1f2937',
        borderColor: '#4b5563',
        borderWidth: 1,
        textStyle: { color: '#f9fafb' },
        formatter: (info: any) => {
          return `<strong>${info.name}</strong><br/>Market Cap: $${info.value.toLocaleString()}B`;
        }
      },
      color: [
    
        '#22d3ee', // cyan
        '#f72585', // pink
        '#a78bfa', // purple
        '#ffd60a', // yellow
        '#3b6064', // orange
        '#ef4444', // red
        '#70e000', // green
        '#f472b6', // rose
        '#60a5fa', // blue
        '#facc15'  // gold
      ],
 series: [
  {
    type: 'treemap',
    roam: false, // prevents zoom/pan
    nodeClick: false, // disables clicking on nodes
    data,
    label: {
      show: true,
      formatter: '{b}',
      fontSize: 12,
      color: '#fff'
    },
    upperLabel: {
      show: false
    },
    leafDepth: 1,
    silent: true, // ✅ disables all interactions
    levels: [
      {
        itemStyle: {
          borderColor: '#111827',
          borderWidth: 2,
          gapWidth: 4
        }
      }
    ]
  }
]

    });
  }
</script>

<div bind:this={chartEl} style="width: 100%; height: 500px; margin-top: 2rem;"></div>
