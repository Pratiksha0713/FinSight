<script lang="ts">
  import Overview from '$lib/components/tabs/Overview.svelte';
  import Cashflow from '$lib/components/tabs/Cashflow.svelte';
  import PnL from '$lib/components/tabs/PnL.svelte';
  import BalanceSheet from '$lib/components/tabs/BalanceSheet.svelte';
  import Comparison from '$lib/components/tabs/Comparison.svelte';

  
  let activeTab = 'Overview';
  const tabs = ['Overview', 'Cashflow', 'P&L', 'Balance Sheet', 'Comparison'];

  function getTabComponent(tab: string) {
    switch (tab) {
      case 'Overview': return Overview;
      case 'Cashflow': return Cashflow;
      case 'P&L': return PnL;
      case 'Balance Sheet': return BalanceSheet;
      case 'Comparison': return Comparison;
      default: return Overview;
    }
  }
</script>

<div class="text-center mt-8">

  <div class="flex justify-center gap-3 flex-wrap mb-8">
    {#each tabs as tab}
      <button
        class={`px-4 py-2 rounded-lg text-sm font-semibold transition ${
          activeTab === tab
            ? 'bg-white text-black'
            : 'bg-black text-white hover:bg-gray-800'
        }`}
        on:click={() => (activeTab = tab)}
      >
        {tab}
      </button>
    {/each}
  </div>

  <svelte:component this={getTabComponent(activeTab)} />
</div>
