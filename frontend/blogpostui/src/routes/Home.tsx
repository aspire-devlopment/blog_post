// src/pages/Home.tsx
import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import Header from "../compontents/Header";
import Footer from "../compontents/footer";

interface BlogPost {
  id: number;
  title: string;
  content: string;
  image?: string | null;
  author__id?: number;
  created_at?: string;
}

export default function Home() {
  const [blogPosts, setBlogPosts] = useState<BlogPost[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  
  // Pagination state
  const [currentPage, setCurrentPage] = useState(1);
  const postsPerPage = 6;

  useEffect(() => {
    const fetchPosts = async () => {
      try {
        const res = await fetch("http://127.0.0.1:8000/api/allblog/");
        if (!res.ok) throw new Error("Failed to fetch posts");
        const data: BlogPost[] = await res.json();
        setBlogPosts(data);
      } catch (err: any) {
        console.error(err);
        setError(err.message || "Something went wrong");
      } finally {
        setLoading(false);
      }
    };
    fetchPosts();
  }, []);

  // Calculate pagination
  const indexOfLastPost = currentPage * postsPerPage;
  const indexOfFirstPost = indexOfLastPost - postsPerPage;
  const currentPosts = blogPosts.slice(indexOfFirstPost, indexOfLastPost);
  const totalPages = Math.ceil(blogPosts.length / postsPerPage);

  return (
    <div className="min-h-screen flex flex-col">
      <Header />

      <section id="posts" className="py-16 bg-gray-50 flex-grow">
        <div className="max-w-6xl mx-auto px-6">
          <h2 className="text-3xl font-bold text-center text-gray-800 mb-10">
            Latest Blog Posts
          </h2>

          {loading && <p className="text-center text-gray-500">Loading posts...</p>}
          {error && <p className="text-center text-red-500">{error}</p>}

          <div className="grid gap-8 sm:grid-cols-2 lg:grid-cols-3">
            {currentPosts.map((post) => (
              <motion.div
                key={post.id}
                whileHover={{ scale: 1.05 }}
                className="bg-white p-6 rounded-2xl shadow-lg hover:shadow-xl transition"
              >
                <h3 className="text-xl font-semibold text-blue-600 mb-2">{post.title}</h3>
                <p className="text-gray-600 mb-4">
                  {post.content.length > 100
                    ? post.content.substring(0, 100) + "..."
                    : post.content}
                </p>
                <a
                  href={`/blog/${post.id}`}
                  className="text-sm text-indigo-600 font-medium hover:underline"
                >
                  Read more →
                </a>
                {post.image ? (
                  <img
                    src={post.image.startsWith("http") 
                      ? post.image
                      : `http://127.0.0.1:8000${post.image}`}
                    alt={post.title}
                    className="w-full h-48 object-cover mx-auto rounded-lg mt-4"
                  />
                ) : (
                  <span className="text-gray-400">No image</span>
                )}
              </motion.div>
            ))}
          </div>

          {/* Pagination Controls */}
          <div className="flex justify-center mt-8 space-x-2">
            {Array.from({ length: totalPages }, (_, i) => i + 1).map((page) => (
              <button
                key={page}
                onClick={() => setCurrentPage(page)}
                className={`px-4 py-2 rounded ${
                  page === currentPage
                    ? "bg-blue-600 text-white"
                    : "bg-gray-200 text-gray-700 hover:bg-gray-300"
                }`}
              >
                {page}
              </button>
            ))}
          </div>
        </div>
      </section>

      <Footer />
    </div>
  );
}
