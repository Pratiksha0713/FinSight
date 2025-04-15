<script lang="ts">
  import { onMount } from 'svelte';
  import * as echarts from 'echarts';

  let chartEl: HTMLDivElement;
  let chart: echarts.ECharts;

  onMount(async () => {
    //const res = await fetch('http://localhost:8000/data');
    const res = await fetch("/api/data");

    const data = await res.json();

    const years = [...new Set(data.map((d: any) => d.Year))].sort();
    const ebitdaByYear = Object.fromEntries(years.map(y => [y, 0]));
    const netIncomeByYear = Object.fromEntries(years.map(y => [y, 0]));

    data.forEach((row: any) => {
      const year = row.Year;
      const ebitda = parseFloat(String(row["EBITDA"]).replace(/[^0-9.-]/g, '')) || 0;
      const net = parseFloat(String(row["Net Income"]).replace(/[^0-9.-]/g, '')) || 0;
      ebitdaByYear[year] += ebitda;
      netIncomeByYear[year] += net;
    });

    const ebitda = years.map(year => +ebitdaByYear[year].toFixed(2));
    const netIncome = years.map(year => +netIncomeByYear[year].toFixed(2));

    chart = echarts.init(chartEl);
    chart.setOption({
      title: {
        text: 'EBITDA vs Net Income Over Time',
        left: 'center',
        textStyle: {
          color: '#fff',
          fontSize: 18
        }
      },
      tooltip: {
        trigger: 'axis',
        formatter: (params: any) => {
          return `
            Year: ${params[0].axisValue}<br/>
            🟩 EBITDA: $${params[0].value.toLocaleString()}B<br/>
            🟦 Net Income: $${params[1].value.toLocaleString()}B
          `;
        }
      },
      legend: {
        data: ['EBITDA', 'Net Income'],
        top: 30,
        textStyle: { color: '#ccc' }
      },
      xAxis: {
        type: 'category',
        data: years,
        axisLabel: { color: '#ccc' }
      },
      yAxis: {
        type: 'value',
        axisLabel: { color: '#ccc' },
        name: '$B'
      },
      series: [
        {
          name: 'EBITDA',
          type: 'line',
          data: ebitda,
          smooth: true,
          lineStyle: { color: '#4CAF50' }
        },
        {
          name: 'Net Income',
          type: 'line',
          data: netIncome,
          smooth: true,
          lineStyle: { color: '#2196F3' }
        }
      ]
    });

    window.addEventListener("resize", () => chart.resize());
  });
</script>

<div bind:this={chartEl} style="width: 100%; height: 500px; margin-top: 2rem;"></div>
