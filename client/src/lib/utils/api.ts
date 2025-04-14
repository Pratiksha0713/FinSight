export async function fetchData() {
  const res = await fetch('http://localhost:8000/data');
  return await res.json();
}
