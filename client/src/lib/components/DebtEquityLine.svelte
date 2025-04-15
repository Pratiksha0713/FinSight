<script lang="ts">
  import { onMount } from 'svelte';
  import * as echarts from 'echarts';

  let chartEl: HTMLDivElement;

  onMount(async () => {
    //const res = await fetch('http://localhost:8000/data');
    const res = await fetch("/api/data");
    const rawData = await res.json();

    const companyYearMap: Record<string, Record<number, number>> = {};
    const yearSet = new Set<number>();

    rawData.forEach((row: any) => {
      const company = row["Company"];
      const year = +row["Year"];
      const ratio = parseFloat(row["Debt/Equity Ratio"]);
      if (!isNaN(ratio) && ratio >= 0) {
        if (!companyYearMap[company]) companyYearMap[company] = {};
        companyYearMap[company][year] = ratio;
        yearSet.add(year);
      }
    });

    const years = Array.from(yearSet).sort((a, b) => a - b);
    const companies = Object.keys(companyYearMap);

    const vibrantColors = [
      '#ef4444', '#6366f1', '#10b981', '#f59e0b', '#8b5cf6',
      '#0ea5e9', '#ec4899', '#14b8a6', '#eab308', '#f97316',
      '#38bdf8', '#f472b6'
    ];

    const series = companies.map((company, idx) => ({
      name: company,
      type: 'line',
      symbol: 'circle',
      smooth: true,
      lineStyle: {
        width: 3
      },
      itemStyle: {
        color: vibrantColors[idx % vibrantColors.length],
        shadowBlur: 10,
        shadowColor: 'rgba(255,255,255,0.2)'
      },
      data: years.map(year => companyYearMap[company][year] ?? 0)
    }));

    const chart = echarts.init(chartEl);
    chart.setOption({
      title: {
        text: 'Debt to Equity Ratio Over Time',
        left: 'center',
        textStyle: {
          fontSize: 20,
          fontWeight: 'bold',
          color: '#ffffff' // ✅ white title
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
        top: 30,
        type: 'scroll',
        icon: 'circle',
        pageIconColor: '#22d3ee',
        textStyle: {
          fontSize: 12,
          color: '#ffffff' // ✅ white legend
        }
      },
      grid: {
        top: 80,
        left: '4%',
        right: '4%',
        bottom: '8%',
        containLabel: true
      },
      xAxis: {
        type: 'category',
        data: years,
        axisLabel: {
          rotate: 45,
          color: '#ffffff' // ✅ white labels
        },
        axisLine: { lineStyle: { color: '#ffffff' } }
      },
      yAxis: {
        type: 'value',
        name: 'Debt/Equity Ratio',
        nameTextStyle: { color: '#ffffff' },
        axisLabel: { color: '#ffffff' },
        axisLine: { lineStyle: { color: '#ffffff' } },
        splitLine: { lineStyle: { color: '#334155' } }
      },
      series
    });

    window.addEventListener("resize", () => chart.resize());
  });
</script>

<div bind:this={chartEl} style="width: 100%; height: 460px; margin-top: 2rem;"></div>
