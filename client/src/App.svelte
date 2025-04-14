<script lang="ts">
  import Dashboard from './routes/Dashboard.svelte';
</script>

<main class="min-h-screen w-screen bg-gradient-to-br from-[#fdfcfb] via-[#fef6f3] to-[#fdfcfb] text-gray-900 font-inter overflow-x-hidden">
  <div class="relative w-full flex flex-col items-center">
    <header class="relative z-50 w-full bg-white/80 backdrop-blur-lg border-b border-gray-200 shadow-md px-8 py-6">
      <div class="max-w-screen-2xl mx-auto flex flex-col md:flex-row items-center justify-between gap-4 animate-fadeSlide">
        <div>
          <h1 class="text-4xl md:text-6xl font-black tracking-tight text-gray-900 whitespace-nowrap hover:scale-[1.03] transition-transform duration-300">
            HeronAI <span class="bg-gradient-to-r from-indigo-500 via-sky-500 to-fuchsia-500 bg-clip-text text-transparent drop-shadow-md">Financial Dashboard</span>
          </h1>
          <p class="text-base md:text-lg text-gray-600 italic mt-1 animate-fadeIn">
            🚀 Powered by data. Designed to impress.
          </p>
        </div>
      </div>
    </header>

    <section class="mt-10 w-full py-12 px-6 sm:px-12 lg:px-24 xl:px-32 flex justify-center items-start">
      <div class="w-full max-w-screen-2xl rounded-[2.5rem] bg-white/95 shadow-[0_20px_60px_rgba(0,0,0,0.1)] backdrop-blur-2xl p-10 md:p-16 border border-gray-100 transition-all duration-500 ease-in-out hover:shadow-[0_30px_100px_rgba(0,0,0,0.12)]">
        <div class="relative isolate overflow-hidden bg-gradient-to-br from-indigo-50 via-pink-50 to-yellow-50 p-10 mb-14 rounded-3xl shadow-inner border border-white/70">
          <div class="absolute -top-12 -right-12 w-48 h-48 bg-gradient-to-r from-violet-200 to-pink-300 opacity-20 rounded-full blur-3xl"></div>
          <h2 class="text-3xl sm:text-5xl font-extrabold text-gray-900 text-center leading-tight">
            ✨ Transforming Financial Data into Visual Mastery ✨ 
          </h2>
          <p class="text-md sm:text-lg text-gray-700 mt-4 text-center max-w-2xl mx-auto">
            Dive into clarity with interactive charts and intelligent dashboards. Monitor trends, evaluate KPIs, and make confident, data-backed decisions.
          </p>
        </div>
        <Dashboard />
      </div>
    </section>
  </div>
</main>

<style>
  main {
    font-family: 'Inter', system-ui, sans-serif;
    background-size: 300% 300%;
    animation: gradientShift 12s ease infinite;
  }

  h1 span {
    background: linear-gradient(to right, #6366f1, #3b82f6, #ec4899);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
  }

  @keyframes gradientShift {
    0%, 100% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
  }

  @keyframes fadeIn {
    0% { opacity: 0; transform: translateY(-5px); }
    100% { opacity: 1; transform: translateY(0); }
  }

  @keyframes fadeSlide {
    0% { opacity: 0; transform: translateY(-20px); }
    100% { opacity: 1; transform: translateY(0); }
  }

  .animate-fadeIn {
    animation: fadeIn 1s ease-out forwards;
  }

  .animate-fadeSlide {
    animation: fadeSlide 0.8s ease-in-out;
  }
</style>

</style>
