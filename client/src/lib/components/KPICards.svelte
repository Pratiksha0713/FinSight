<script lang="ts">
  import { onMount } from 'svelte';

  let data: any[] = [];
  let totalRevenue = 0;
  let totalNetIncome = 0;
  let totalEbitda = 0;
  let avgRoe = 0;

  onMount(async () => {
    const res = await fetch("http://localhost:8000/data");
    data = await res.json();

    totalRevenue = sum(data, "Revenue");
    totalNetIncome = sum(data, "Net Income");
    totalEbitda = sum(data, "EBITDA");
    avgRoe = average(data, "ROE");
  });

  function sum(arr: any[], key: string) {
    return arr.reduce((acc, obj) => acc + (parseFloat(obj[key]) || 0), 0);
  }

  function average(arr: any[], key: string) {
    const values = arr.map((d) => parseFloat(d[key]) || 0);
    return values.reduce((a, b) => a + b, 0) / values.length;
  }

  function formatMoney(value: number) {
    return `$${(value / 1000).toFixed(1)}K`;
  }

  function formatPercent(value: number) {
    return `${value.toFixed(1)}%`;
  }
</script>

<style>
  .card-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 1.5rem;
    padding: 1rem 0;
  }

  .card {
    background-color: #1e1e1e;
    border-radius: 12px;
    padding: 1.2rem;
    text-align: center;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    transition: all 0.3s ease;
    transform: translateY(0);
    cursor: pointer;
  }

  .card:hover {
    transform: translateY(-6px) scale(1.05);
    box-shadow: 0 8px 20px rgba(255, 255, 255, 0.15);
  }

  .title {
    font-size: 0.9rem;
    color: #ccc;
  }

  .value {
    font-size: 1.6rem;
    font-weight: 700;
    margin-top: 0.3rem;
    color: #fff;
  }
</style>

<div class="card-grid my-6">
  <div class="card">
    <div class="title">📈 Total Revenue</div>
    <div class="value">{formatMoney(totalRevenue)}</div>
  </div>

  <div class="card">
    <div class="title">💰 Net Income</div>
    <div class="value">{formatMoney(totalNetIncome)}</div>
  </div>

  <div class="card">
    <div class="title">💼 EBITDA</div>
    <div class="value">{formatMoney(totalEbitda)}</div>
  </div>

  <div class="card">
    <div class="title">🧠 Avg ROE</div>
    <div class="value">{formatPercent(avgRoe)}</div>
  </div>
</div>
