<script>
  import { onMount } from 'svelte';
  import * as echarts from 'echarts';


  let chartEl;
  let loading = true;
  let error = null;

  let chart;
  let data = {};
  let tickers = [];
  let selectedTicker = '';

  const updateChart = (ticker) => {
    const tickerData = data[ticker];
    if (!tickerData) return;

    const years = Object.keys(tickerData).map(y => y.toString()).sort();
    const operating = years.map(y => tickerData[y]?.Operating ?? 0);
    const investing = years.map(y => tickerData[y]?.Investing ?? 0);
    const financing = years.map(y => tickerData[y]?.Financing ?? 0);

    const option = {
      backgroundColor: 'transparent',
      title: {
        text: `${ticker} Cash Flow Over Years`,
        left: 'center',
        top: 10,
        textStyle: {
          color: '#fff',
          fontSize: 20,
          fontWeight: 'bold'
        }
      },
      tooltip: {
        trigger: 'axis',
        backgroundColor: '#1e1e1e',
        borderColor: '#555',
        borderWidth: 1,
        textStyle: { color: '#fff', fontSize: 14 },
        padding: 12,
        axisPointer: {
          type: 'cross',
          label: {
            backgroundColor: '#444'
          }
        },
        extraCssText: 'box-shadow: 0 0 10px rgba(0,0,0,0.4); border-radius: 8px;'
      },
      legend: {
        top: 50,
        textStyle: {
          color: '#ccc',
          fontSize: 14
        },
        itemGap: 20
      },
      grid: {
        top: 110,
        left: 80,
        right: 50,
        bottom: 60
      },
      xAxis: {
        type: 'category',
        boundaryGap: false,
        data: years,
        axisLabel: {
          color: '#aaa',
          fontSize: 12,
          fontWeight: 'normal'
        },
        axisLine: { lineStyle: { color: '#666' } },
        splitLine: { show: false }
      },
      yAxis: {
        type: 'value',
        axisLabel: {
          color: '#aaa',
          fontSize: 12,
          formatter: value => value.toLocaleString()
        },
        axisLine: { lineStyle: { color: '#666' } },
        splitLine: { lineStyle: { color: '#333' } }
      },
      series: [
        {
          name: 'Operating',
          type: 'line',
          smooth: true,
          symbolSize: 8,
          showSymbol: true,
          lineStyle: {
            width: 3,
            color: '#4ea8de'
          },
          itemStyle: {
            color: '#4ea8de',
            shadowBlur: 10,
            shadowColor: 'rgba(78,168,222,0.6)'
          },
          areaStyle: {
            color: {
              type: 'linear',
              x: 0, y: 0, x2: 0, y2: 1,
              colorStops: [
                { offset: 0, color: 'rgba(78,168,222,0.3)' },
                { offset: 1, color: 'rgba(78,168,222,0)' }
              ]
            }
          },
          animationDuration: 1000,
          data: operating
        },
        {
          name: 'Investing',
          type: 'line',
          smooth: true,
          symbolSize: 8,
          lineStyle: {
            width: 3,
            color: '#a3e635'
          },
          itemStyle: {
            color: '#a3e635',
            shadowBlur: 10,
            shadowColor: 'rgba(163,230,53,0.6)'
          },
          areaStyle: {
            color: {
              type: 'linear',
              x: 0, y: 0, x2: 0, y2: 1,
              colorStops: [
                { offset: 0, color: 'rgba(163,230,53,0.3)' },
                { offset: 1, color: 'rgba(163,230,53,0)' }
              ]
            }
          },
          animationDuration: 1200,
          data: investing
        },
        {
          name: 'Financing',
          type: 'line',
          smooth: true,
          symbolSize: 8,
          lineStyle: {
            width: 3,
            color: '#facc15'
          },
          itemStyle: {
            color: '#facc15',
            shadowBlur: 10,
            shadowColor: 'rgba(250,204,21,0.6)'
          },
          areaStyle: {
            color: {
              type: 'linear',
              x: 0, y: 0, x2: 0, y2: 1,
              colorStops: [
                { offset: 0, color: 'rgba(250,204,21,0.3)' },
                { offset: 1, color: 'rgba(250,204,21,0)' }
              ]
            }
          },
          animationDuration: 1400,
          data: financing
        }
      ]
    };

    if (chart) {
      chart.setOption(option);
    }
  };

  onMount(async () => {
    try {
      //const res = await fetch('http://localhost:8000/cashflow');
      const res = await fetch("/api/cashflow");

      const raw = await res.text();
      data = JSON.parse(raw);
      tickers = Object.keys(data);
      selectedTicker = tickers[0];

      setTimeout(() => {
        chart = echarts.init(chartEl);
        updateChart(selectedTicker);
      }, 0);

      loading = false;
    } catch (err) {
      console.error("❌ Error loading chart:", err);
      error = err.message;
      loading = false;
    }
  });

  $: if (chart && selectedTicker) {
    updateChart(selectedTicker);
  }
</script>

<style>
  .dashboard-wrapper {
    padding: 2rem;
    max-width: 1200px;
    margin: 0 auto;
    display: flex;
    flex-direction: row;
    gap: 2rem;
    align-items: flex-start;
    justify-content: center;
  }

  .dropdown-panel {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
    margin-top: 1.5rem;
  }

  .title {
    font-size: 2rem;
    font-weight: 800;
    color: #fff;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    text-shadow: 0 2px 8px rgba(255, 255, 255, 0.15);
  }

  .dropdown-label {
    color: #ddd;
    font-size: 1.1rem;
    font-weight: 500;
  }

  .dropdown {
    background-color: #2a2a2a;
    color: #f9f9f9;
    border: 2px solid #555;
    border-radius: 8px;
    padding: 0.6rem 1.2rem;
    font-size: 1rem;
    font-weight: 500;
    cursor: pointer;
    transition: border-color 0.3s, background-color 0.3s;
  }

  .dropdown:hover,
  .dropdown:focus {
    border-color: #88c0d0;
    background-color: #333;
    outline: none;
  }

  .chart-container {
    flex: 1;
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid #333;
    box-shadow: 0 0 12px rgba(0, 0, 0, 0.4);
    min-width: 700px;
  }

  p {
    color: #ccc;
    text-align: center;
    font-size: 1rem;
  }
</style>

{#if loading}
  <p>⏳ Loading chart...</p>
{:else if error}
  <p style="color: red;">❌ {error}</p>
{:else}
  <div class="dashboard-wrapper">
    <div class="dropdown-panel">
      <div class="title">Cash Flow Visualizer</div>
      <label class="dropdown-label">Select a Company:</label>
      <select bind:value={selectedTicker} class="dropdown">
        {#each tickers as t}
          <option value={t}>{t}</option>
        {/each}
      </select>
    </div>

    <div class="chart-container">
      <div bind:this={chartEl} style="width: 100%; height: 500px;"></div>
    </div>
  </div>
{/if}





