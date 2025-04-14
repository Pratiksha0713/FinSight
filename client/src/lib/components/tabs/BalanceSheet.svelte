<script lang="ts">
  import EquityDebtChart from '../EquityDebtChart.svelte';
  import CurrentRatioLine from '../CurrentRatioLine.svelte';
  import DebtEquityLine from '../DebtEquityLine.svelte';
  import { toPng } from 'html-to-image';

  async function exportDashboard() {
    const node = document.getElementById('balance-dashboard');
    if (!node) return;
    await new Promise(resolve => setTimeout(resolve, 300)); // delay to allow charts to update
    const dataUrl = await toPng(node, { cacheBust: true });
    const link = document.createElement('a');
    link.download = 'balance-sheet-dashboard.png';
    link.href = dataUrl;
    link.click();
  }
</script>

<div class="text-center mt-6">
  <h2 class="text-2xl font-semibold mb-2 flex items-center justify-center">📊 Balance Sheet</h2>
  <p class="text-gray-400 mb-4">
    This dashboard compares Total Equity and Liabilities across companies and shows key balance sheet health metrics.
  </p>
</div>

<!-- ✅ Wrapper for exportable content -->
<div id="balance-dashboard" class="space-y-6">
  <EquityDebtChart />
  <CurrentRatioLine />
  <DebtEquityLine />
</div>

<!-- ✅ Export button -->
<div class="text-right mt-6">
  <button on:click={exportDashboard} class="bg-indigo-600 text-white px-4 py-2 rounded shadow hover:bg-indigo-700">
    📤 Export Balance Sheet Dashboard as PNG
  </button>
</div>
