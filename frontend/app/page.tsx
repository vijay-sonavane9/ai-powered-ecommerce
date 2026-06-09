"use client";
import { useState } from "react";

export default function Home() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);

  // NEW: Shopping Cart State
  const [cart, setCart] = useState<any[]>([]);

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query) return;

    setLoading(true);
    try {
      const response = await fetch(`http://localhost:8000/search?query=${query}`);
      const data = await response.json();
      setResults(data.results || []);
    } catch (error) {
      console.error("Search failed:", error);
    }
    setLoading(false);
  };

  // NEW: Function to handle adding items to the cart
  const addToCart = (product: any) => {
    setCart([...cart, product]);
    // Optional: You could trigger a little toast notification here!
  };

  return (
    <main className="min-h-screen bg-gray-50 text-gray-900 font-sans pb-20">

      {/* NEW: Sleek Navigation Bar */}
      <nav className="bg-white shadow-sm sticky top-0 z-50">
        <div className="max-w-6xl mx-auto px-6 py-4 flex justify-between items-center">
          <div className="text-2xl font-black text-blue-600 tracking-tighter">
            AI<span className="text-gray-900">Mart</span>
          </div>
          <div className="flex items-center gap-4 cursor-pointer hover:bg-gray-100 p-2 rounded-lg transition">
            <span className="font-semibold text-gray-700">Cart</span>
            <div className="bg-blue-600 text-white text-sm font-bold w-8 h-8 flex items-center justify-center rounded-full shadow-md">
              {cart.length}
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <div className="max-w-3xl mx-auto w-full text-center mt-12 mb-12 px-6">
        <h1 className="text-5xl md:text-6xl font-extrabold mb-6 text-gray-900 tracking-tight leading-tight">
          Find exactly what you need, <span className="text-blue-600">instantly.</span>
        </h1>
        <p className="text-lg md:text-xl text-gray-600 mb-8">
          Don't search for product names. Describe your problem, your vibe, or your needs, and our AI will find the perfect match.
        </p>

        {/* Search Bar */}
        <form onSubmit={handleSearch} className="flex flex-col sm:flex-row gap-3">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="e.g. I need a warm jacket for a snowy trip..."
            className="flex-1 px-6 py-4 rounded-xl border border-gray-300 shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 text-lg transition"
          />
          <button
            type="submit"
            disabled={loading}
            className="px-8 py-4 bg-blue-600 text-white text-lg font-bold rounded-xl shadow-md hover:bg-blue-700 hover:shadow-lg transition disabled:bg-blue-400"
          >
            {loading ? "Scanning Data..." : "Search AI"}
          </button>
        </form>
      </div>

      {/* Product Grid Section */}
      <div className="max-w-6xl mx-auto w-full grid grid-cols-1 md:grid-cols-2 gap-8 px-6">
        {results.map((product: any) => (
          <div key={product.id} className="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden hover:shadow-xl transition duration-300 flex flex-col group">
            <div className="h-72 bg-white p-6 flex items-center justify-center overflow-hidden">
              <img
                src={product.image_url}
                alt={product.name}
                className="max-h-full max-w-full object-contain group-hover:scale-105 transition duration-500"
              />
            </div>
            <div className="p-6 flex-1 flex flex-col border-t border-gray-50">
              <div className="flex justify-between items-start mb-3 gap-4">
                <h2 className="text-xl font-bold text-gray-800 line-clamp-2">{product.name}</h2>
                <span className="text-2xl font-black text-gray-900">${product.price}</span>
              </div>
              <p className="text-gray-500 mb-6 flex-1 text-sm line-clamp-3 leading-relaxed">{product.description}</p>
              <button
                onClick={() => addToCart(product)}
                className="w-full py-4 bg-gray-900 hover:bg-gray-800 text-white font-bold rounded-xl shadow-md hover:shadow-lg transition active:scale-[0.98]"
              >
                Add to Cart
              </button>
            </div>
          </div>
        ))}
      </div>

    </main>
  );
}