<script>
  import { onMount } from 'svelte';
  import * as echarts from 'echarts';

  let companies = [];
  let selected = '';
  let data = {};
  let chartEl;
  let chartInstance;

  onMount(async () => {
    try {
      //const res = await fetch('http://localhost:8000/pnl');
      const res = await fetch("/api/data");

      data = await res.json();
      companies = Object.keys(data);
      selected = companies[0];
    } catch (err) {
      console.error('Failed to fetch P&L data:', err);
    }
  });

  $: if (selected && data[selected]) {
    const selectedData = Object.values(data[selected]).sort((a, b) => a.Year - b.Year);
    const years = selectedData.map(row => row.Year);
    const revenue = selectedData.map(row => row.Revenue);
    const grossProfit = selectedData.map(row => row["Gross Profit"]);
    const netIncome = selectedData.map(row => row["Net Income"]);

    const option = {
      backgroundColor: 'transparent',
      title: {
        text: `${selected} P&L Overview (2009–2022)`,
        left: 'center',
        textStyle: {
          color: '#fff',
          fontSize: 20,
          fontWeight: 'bold'
        }
      },
      tooltip: {
        trigger: 'axis',
        axisPointer: {
          type: 'shadow'
        },
        backgroundColor: '#1e1e1e',
        borderColor: '#888',
        borderWidth: 1,
        textStyle: { color: '#fff' },
        padding: 10
      },
      legend: {
        data: ['Revenue', 'Gross Profit', 'Net Income'],
        textStyle: { color: '#ccc' },
        top: 40
      },
      grid: {
        top: 100,
        left: 60,
        right: 20,
        bottom: 50,
        containLabel: true
      },
      xAxis: {
        type: 'category',
        data: years,
        axisLabel: { color: '#aaa', fontSize: 12 },
        axisLine: { lineStyle: { color: '#666' } }
      },
      yAxis: {
        type: 'value',
        axisLabel: {
          color: '#aaa',
          formatter: value => value.toLocaleString()
        },
        axisLine: { lineStyle: { color: '#666' } },
        splitLine: { lineStyle: { color: '#333' } }
      },
      series: [
        {
          name: 'Revenue',
          type: 'bar',
          stack: 'total',
          emphasis: { focus: 'series' },
          itemStyle: { color: '#9657b0' },
          data: revenue
        },
        {
          name: 'Gross Profit',
          type: 'bar',
          stack: 'total',
          emphasis: { focus: 'series' },
          itemStyle: { color: '#AFBCC8' },
          data: grossProfit
        },
        {
          name: 'Net Income',
          type: 'line',
          smooth: true,
          symbol: 'circle',
          symbolSize: 8,
          lineStyle: { width: 3, color: '#facc15' },
          itemStyle: { color: '#facc15', borderWidth: 2 },
          data: netIncome
        }
      ]
    };

    if (chartInstance) {
      chartInstance.dispose();
    }
    chartInstance = echarts.init(chartEl);
    chartInstance.setOption(option);
  }
</script>

<style>
  .pnl-dashboard {
    padding: 2rem;
    display: flex;
    flex-direction: row;
    gap: 2.5rem;
    align-items: center;
    justify-content: center;
    height: 100vh;
    box-sizing: border-box;
  }

  .pnl-header {
    min-width: 320px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    gap: 2rem;
  }

  .pnl-header h2 {
    font-size: 2rem;
    font-weight: bold;
    color: #fff;
    text-transform: uppercase;
    letter-spacing: 0.05em;
  }

  .dropdown-label {
    color: #ccc;
    font-size: 1rem;
  }

  .dropdown {
    background: #1f1f1f;
    color: #fff;
    border: 1px solid #444;
    border-radius: 6px;
    padding: 0.5rem 1rem;
    font-size: 1rem;
    margin-top: 0.25rem;
  }

  .chart-wrapper {
    flex-grow: 1;
    height: 600px;
    border-radius: 16px;
    overflow: hidden;
    background: linear-gradient(to right, #1e293b, #111827);
    box-shadow: 0 16px 32px rgba(0, 0, 0, 0.5);
    min-width: 800px;
  }
</style>

<div class="pnl-dashboard">
  <div class="pnl-header">
    <h2>📊 Profit & Loss Dashboard</h2>
    <div>
      <div class="dropdown-label">Company:</div>
      <select id="company-select" class="dropdown" bind:value={selected}>
        {#each companies as c}
          <option value={c}>{c}</option>
        {/each}
      </select>
    </div>
  </div>

  <div class="chart-wrapper" bind:this={chartEl}></div>
</div>
