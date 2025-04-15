<script lang="ts">
  import { onMount } from 'svelte';
  import * as echarts from 'echarts';

  let chartEl: HTMLDivElement;

  onMount(async () => {
    //const res = await fetch('http://localhost:8000/data');
    const res = await fetch("/api/data");

    const rawData = await res.json();

    const companyMap = {};
    rawData.forEach((d) => {
      const company = d['Company'];
      const equity = parseFloat(d['Share Holder Equity']) || 0;
      const debt = parseFloat(d['Debt/Equity Ratio']) * equity || 0;

      if (!companyMap[company]) companyMap[company] = { equity: 0, debt: 0 };
      companyMap[company].equity += equity;
      companyMap[company].debt += debt;
    });

    const companies = Object.keys(companyMap);
    const equityData = companies.map((c) => companyMap[c].equity.toFixed(2));
    const debtData = companies.map((c) => companyMap[c].debt.toFixed(2));

    const chart = echarts.init(chartEl);

    chart.setOption({
      backgroundColor: 'transparent',
      title: {
        text: 'Equity vs Debt by Company',
        left: 'center',
        textStyle: {
          color: '#fff',
          fontSize: 20,
          fontWeight: 'bold',
          textShadowColor: '#000',
          textShadowBlur: 4
        }
      },
      tooltip: {
        trigger: 'axis',
        backgroundColor: '#1f2937',
        borderColor: '#9ca3af',
        borderWidth: 1,
        textStyle: { color: '#f9fafb', fontSize: 14 },
        padding: 12,
        axisPointer: { type: 'shadow' }
      },
      legend: {
        top: 30,
        data: ['Equity', 'Debt'],
        textStyle: {
          color: '#e5e7eb',
          fontSize: 14
        }
      },
      grid: {
        top: 70,
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
      },
      xAxis: {
        type: 'category',
        data: companies,
        axisLabel: {
          rotate: 45,
          color: '#d1d5db',
          fontWeight: 'bold'
        }
      },
      yAxis: {
        type: 'value',
        name: '$B',
        nameTextStyle: {
          color: '#d1d5db'
        },
        axisLabel: {
          color: '#d1d5db',
          formatter: '{value}'
        },
        splitLine: {
          lineStyle: {
            color: '#374151'
          }
        }
      },
      series: [
        {
          name: 'Equity',
          type: 'bar',
          stack: 'total',
          itemStyle: {
            color: '#ff69b4', // bright pink
            shadowBlur: 12,
            shadowColor: 'rgba(255, 0, 221, 0.94)'
          },
          emphasis: { focus: 'series' },
          data: equityData
        },
        {
          name: 'Debt',
          type: 'bar',
          stack: 'total',
          itemStyle: {
            color: '#02CCFE', // vibrant blue
            shadowBlur: 12,
            shadowColor: 'rgba(132, 181, 241, 0.99)'
          },
          emphasis: { focus: 'series' },
          data: debtData
        }
      ]
    });
  });
</script>

<div bind:this={chartEl} style="width: 100%; height: 500px; margin-top: 2rem;"></div>
