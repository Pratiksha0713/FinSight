<script lang="ts">
  export let years: number[] = [];
  export let companies: string[] = [];
  export let selectedYear: number | null = null;
  export let selectedCompany: string | null = null;
  export let onFilterChange: (year: number | null, company: string | null) => void;

  function handleYearChange(e) {
    onFilterChange(+e.target.value || null, selectedCompany);
  }

  function handleCompanyChange(e) {
    onFilterChange(selectedYear, e.target.value || null);
  }
</script>

<div class="flex flex-wrap gap-4 mb-4">
  <select on:change={handleYearChange} class="p-2 rounded border text-sm">
    <option value="">All Years</option>
    {#each years as year}
      <option value={year} selected={selectedYear === year}>{year}</option>
    {/each}
  </select>

  <select on:change={handleCompanyChange} class="p-2 rounded border text-sm">
    <option value="">All Companies</option>
    {#each companies as company}
      <option value={company} selected={selectedCompany === company}>{company}</option>
    {/each}
  </select>
</div>
