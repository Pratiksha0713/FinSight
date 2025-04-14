<script>
  import KPICards from '../KPICards.svelte';
  import RevenueNetChart from '../RevenueNetChart.svelte';
  import EbitdaNetChart from '../EbitdaNetChart.svelte';
  import MarketTreemap from '../MarketTreemap.svelte';
  import { toPng } from 'html-to-image';

  async function exportPage() {
    const node = document.getElementById('dashboard-content');
    if (!node) return;

    const dataUrl = await toPng(node, { cacheBust: true });
    const link = document.createElement('a');
    link.download = 'dashboard-overview.png';
    link.href = dataUrl;
    link.click();
  }
</script>

<!-- ✅ WRAPPED in a container for export -->
<div id="dashboard-content" class="p-4 bg-white rounded shadow">

  <h2 class="text-2xl font-bold mt-6 mb-4">📊 Overview</h2>
  <p class="text-gray-600 mb-4">
    This tab includes KPI cards, Revenue vs Net Income, EBITDA trends, and Market Cap breakdown.
  </p>

  <KPICards />
  <RevenueNetChart />
  <EbitdaNetChart />
  <MarketTreemap />
</div>

<!-- ✅ Export Button -->
<div class="text-right mt-4">
  <button on:click={exportPage} class="bg-indigo-600 text-white px-4 py-2 rounded shadow hover:bg-indigo-700">
    📤 Export Entire Dashboard as PNG
  </button>
</div>
