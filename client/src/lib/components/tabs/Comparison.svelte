<script lang="ts">
  import { onMount } from 'svelte';
  import * as echarts from 'echarts';

  let tickers = [];
  let selectedCompany = '';
  let data = [];

  let chartEl;
  let chart;

  const fetchCompanyData = async (company: string) => {
    //const res = await fetch('http://localhost:8000/data');
    const res = await fetch("https://finsight-p85x.onrender.com/data");

    const all = await res.json();
    tickers = [...new Set(all.map((d) => d.Company))];

    const companyData = all.filter((d) => d.Company === company);
    data = companyData.map((d) => ({
      year: d.Year,
      marketCap: d["Market Cap(in B USD)"],
      fcf: d["Free Cash Flow per Share"]
    }));

    drawChart();
  };

  const drawChart = () => {
    const years = data.map(d => d.year);
    const marketCap = data.map(d => d.marketCap);
    const fcf = data.map(d => d.fcf);

    if (!chart) chart = echarts.init(chartEl);
    else chart.clear();

    chart.setOption({
      backgroundColor: '#0f172a',
      tooltip: {
        trigger: 'axis',
        axisPointer: { type: 'shadow' },
        backgroundColor: '#1e293b',
        borderColor: '#38bdf8',
        borderWidth: 1,
        textStyle: { color: '#f1f5f9' }
      },
      legend: {
        data: ['Market Cap (B USD)', 'FCF/Share'],
        textStyle: { color: '#f1f5f9' }
      },
      grid: { left: '5%', right: '5%', bottom: '15%', containLabel: true },
      xAxis: [{
        type: 'category',
        data: years,
        axisLabel: { color: '#e2e8f0', rotate: 45 },
        axisLine: { lineStyle: { color: '#475569' } }
      }],
      yAxis: [
        {
          type: 'value',
          name: 'Market Cap (B USD)',
          nameTextStyle: { color: '#cbd5e1' },
          axisLabel: { color: '#e2e8f0' },
          axisLine: { lineStyle: { color: '#475569' } },
        },
        {
          type: 'value',
          name: 'FCF/Share',
          nameTextStyle: { color: '#cbd5e1' },
          axisLabel: { color: '#e2e8f0' },
          axisLine: { lineStyle: { color: '#475569' } },
        }
      ],
      series: [
        {
          name: 'Market Cap (B USD)',
          type: 'pictorialBar',
          symbol: 'rect',
          symbolRepeat: true,
          symbolSize: [20, 8],
          symbolMargin: 2,
          data: marketCap,
          itemStyle: {
            color: '#facc15',
            borderRadius: 4
          },
          z: 10
        },
        {
          name: 'FCF/Share',
          type: 'line',
          yAxisIndex: 1,
          data: fcf,
          smooth: true,
          lineStyle: {
            width: 4,
            color: '#38bdf8',
            shadowColor: 'rgba(56, 189, 248, 0.6)',
            shadowBlur: 12
          },
          symbol: 'circle',
          symbolSize: 10,
          itemStyle: { color: '#38bdf8' },
          z: 20
        }
      ]
    });
  };

  onMount(async () => {
    //const res = await fetch('http://localhost:8000/data');
    const res = await fetch("https://finsight-p85x.onrender.com/data");

    const all = await res.json();
    tickers = [...new Set(all.map((d) => d.Company))];
    selectedCompany = tickers[0];
    await fetchCompanyData(selectedCompany);
  });

  const handleChange = async (e) => {
    selectedCompany = e.target.value;
    await fetchCompanyData(selectedCompany);
  };
</script>

<!-- UI -->
<div class="max-w-6xl mx-auto px-6 py-12">
  <h2 class="text-3xl font-bold text-center text-white mb-6">📊 Market Cap vs 💵 FCF/Share</h2>

  <div class="flex justify-center mb-8">
    <select bind:value={selectedCompany} on:change={handleChange}
      class="bg-slate-800 text-white border border-slate-600 px-4 py-2 rounded-md">
      {#each tickers as t}
        <option value={t}>{t}</option>
      {/each}
    </select>
  </div>

  <div class="bg-slate-900 p-6 rounded-2xl shadow-xl">
    <div bind:this={chartEl} style="height: 480px;" />
  </div>
</div>

<style>
  :global(body) {
    background-color: #0f172a;
  }
</style>