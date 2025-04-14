<script lang="ts">
  import { onMount } from 'svelte';
  import * as echarts from 'echarts';

  let chartEl: HTMLDivElement;
  let chart: echarts.ECharts;

  onMount(async () => {
    const res = await fetch('http://localhost:8000/data');
    const data = await res.json();

    const grouped = data.reduce((acc, row) => {
      const { Company, Year, "Current Ratio": ratio } = row;
      if (!acc[Company]) acc[Company] = {};
      acc[Company][Year] = ratio;
      return acc;
    }, {});

    const years = Array.from(new Set(data.map(d => d.Year))).sort();

    const series = Object.entries(grouped).map(([company, yearMap]: any) => ({
      name: company,
      type: 'line',
      smooth: true,
      data: years.map(y => yearMap[y] ?? null),
      symbolSize: 6,
      lineStyle: { width: 2 },
      emphasis: {
        focus: 'series'
      }
    }));

    chart = echarts.init(chartEl);
    chart.setOption({
      backgroundColor: 'transparent',
      title: {
        text: 'Current Ratio Trend by Company',
        left: 'center',
        top: 10,
        textStyle: {
          color: '#ffffff',
          fontSize: 20,
          fontWeight: 'bold'
        }
      },
      tooltip: {
        trigger: 'axis',
        backgroundColor: '#1f2937',
        borderColor: '#4b5563',
        borderWidth: 1,
        textStyle: { color: '#f9fafb' }
      },
      legend: {
        top: 40,
        type: 'scroll',
        pageIconColor: '#22d3ee',
        textStyle: { color: '#ffffff' }
      },
      grid: {
        left: 50,
        right: 50,
        top: 90,
        bottom: 60
      },
      xAxis: {
        type: 'category',
        data: years,
        axisLabel: {
          color: '#ffffff'
        },
        axisLine: {
          lineStyle: { color: '#ffffff' }
        }
      },
      yAxis: {
        type: 'value',
        name: 'Current Ratio',
        nameTextStyle: { color: '#ffffff' },
        axisLabel: {
          color: '#ffffff'
        },
        splitLine: {
          lineStyle: { color: '#334155' }
        },
        axisLine: {
          lineStyle: { color: '#ffffff' }
        }
      },
      color: [
        '#f43f5e', '#22c55e', '#eab308', '#60a5fa', '#ec4899', '#8b5cf6',
        '#0ea5e9', '#14b8a6', '#f59e0b', '#a78bfa', '#10b981', '#f87171'
      ],
      series
    });
  });
</script>

<div bind:this={chartEl} style="width: 100%; height: 500px; margin-top: 2rem;"></div>
