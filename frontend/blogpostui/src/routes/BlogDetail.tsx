// src/pages/BlogDetail.tsx
import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
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

export default function BlogDetail() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();

  const [post, setPost] = useState<BlogPost | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchPost = async () => {
      try {
        const res = await fetch(`http://127.0.0.1:8000/api/blog/${id}/`);
        if (!res.ok) throw new Error("Failed to fetch post");
        const data: BlogPost = await res.json();
        setPost(data);
      } catch (err: any) {
        console.error(err);
        setError(err.message || "Something went wrong");
      } finally {
        setLoading(false);
      }
    };

    if (id) fetchPost();
  }, [id]);

  if (loading) return <p className="text-center mt-10">Loading...</p>;
  if (error) return <p className="text-center mt-10 text-red-500">{error}</p>;
  if (!post) return <p className="text-center mt-10">Post not found</p>;

  return (
    <div className="min-h-screen flex flex-col">
      <Header />

      <main className="flex-grow max-w-4xl mx-auto px-6 py-16 bg-gray-50">
        <button
          onClick={() => navigate(-1)}
          className="mb-6 text-blue-600 hover:underline"
        >
          ← Back
        </button>

        <article className="bg-white p-8 rounded-2xl shadow-lg">
          <h1 className="text-3xl font-bold text-gray-800 mb-4">{post.title}</h1>
          {post.image ? (
    <img
      src={post.image.startsWith("http") 
        ? post.image // Already a full URL, use as-is
        : `http://127.0.0.1:8000${post.image}`} // Relative path from backend
      alt={post.title}
          className="w-full h-96 object-cover mx-auto rounded-lg mb-6"

    />
  ) : (
    <span className="text-gray-400">No image</span>
  )}
          <p className="text-gray-700 whitespace-pre-line">{post.content}</p>
          {post.created_at && (
            <p className="text-gray-400 text-sm mt-4">
              Published: {new Date(post.created_at).toLocaleDateString()}
            </p>
          )}
        </article>
      </main>

      <Footer />
    </div>
  );
}
