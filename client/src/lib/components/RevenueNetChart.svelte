<script lang="ts">
  import { onMount } from 'svelte';
  import * as echarts from 'echarts';

  let chartEl: HTMLDivElement;
  let chart: echarts.ECharts;
  let data: any[] = [];

  onMount(async () => {
    //const res = await fetch('http://localhost:8000/data');
    const res = await fetch("https://finsight-p85x.onrender.com/data");

    data = await res.json();
    renderChart();
  });

  function tooltipFormatter(params: any) {
    const index = params[0].dataIndex;
    const d = data[index];
    return `
      <strong style="color:#fff;">Company: ${d.Company}</strong><br/>
      <span style="color:#ccc;">Year: ${d.Year}</span><br/>
      <span style="color:#ccc;">Revenue: $${d["Revenue"].toLocaleString()}</span><br/>
      <span style="color:#ccc;">Net Income: $${d["Net Income"].toLocaleString()}</span>
    `;
  }

  function renderChart() {
    if (!chartEl || !data.length) return;

    const xLabels = data.map(d => d.Year);
    const revenue = data.map(d => d["Revenue"]);
    const netIncome = data.map(d => d["Net Income"]);

    if (!chart) chart = echarts.init(chartEl);
    else chart.clear();

    chart.setOption({
      backgroundColor: 'transparent',
      title: {
        text: 'Revenue vs Net Income',
        textStyle: {
          color: '#ffffff',
          fontSize: 20,
          fontWeight: 'bold'
        },
        left: 'center',
        top: 10
      },
      tooltip: {
        trigger: 'axis',
        formatter: tooltipFormatter,
        backgroundColor: '#1f2937',
        borderColor: '#4b5563',
        borderWidth: 1,
        textStyle: { color: '#f9fafb' }
      },
      legend: {
        data: ['Revenue', 'Net Income'],
        top: 40,
        textStyle: { color: '#ffffff' }
      },
      xAxis: {
        type: 'category',
        data: xLabels,
        axisLabel: {
          color: '#ffffff'
        },
        axisLine: {
          lineStyle: { color: '#ffffff' }
        }
      },
      yAxis: [
        {
          type: 'value',
          name: 'Revenue',
          nameTextStyle: { color: '#ffffff' },
          axisLabel: {
            color: '#ffffff',
            formatter: value => value.toLocaleString()
          },
          axisLine: {
            lineStyle: { color: '#ffffff' }
          },
          splitLine: {
            lineStyle: { color: '#334155' }
          }
        },
        {
          type: 'value',
          name: 'Net Income',
          nameTextStyle: { color: '#ffffff' },
          axisLabel: {
            color: '#ffffff',
            formatter: value => value.toLocaleString()
          },
          axisLine: {
            lineStyle: { color: '#ffffff' }
          },
          splitLine: { show: false }
        }
      ],
      series: [
        {
          name: 'Revenue',
          type: 'bar',
          data: revenue,
          itemStyle: {
            color: '#6366f1'
          },
          emphasis: {
            itemStyle: {
              color: '#818cf8'
            }
          }
        },
        {
          name: 'Net Income',
          type: 'line',
          yAxisIndex: 1,
          data: netIncome,
          lineStyle: {
            width: 3,
            color: '#4ade80'
          },
          itemStyle: {
            color: '#4ade80'
          },
          smooth: true,
          symbol: 'circle',
          symbolSize: 8
        }
      ]
    });
  }
</script>

<div bind:this={chartEl} style="width: 100%; height: 500px; margin-top: 2rem;"></div>
