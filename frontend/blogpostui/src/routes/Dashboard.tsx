import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import BlogForm from "../compontents/BlogPostForm";

interface BlogPost {
  id: number;
  title: string;
  content: string;
  image?: string | null;
}

const Dashboard = () => {
  const [posts, setPosts] = useState<BlogPost[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [showEditModal, setShowEditModal] = useState(false);
  const [currentEditPost, setCurrentEditPost] = useState<BlogPost | null>(null);

  const navigate = useNavigate();
  const token = localStorage.getItem("authToken");

  // Redirect if not authenticated
  useEffect(() => {
    if (!token) navigate("/login");
  }, [token, navigate]);

  // Fetch user's blog posts
  const fetchPosts = async () => {
    if (!token) return;
    setLoading(true);
    try {
      const res = await fetch("http://127.0.0.1:8000/api/blog/create/", {
  method: "GET",
  headers: {
    "Content-Type": "application/json",
    Authorization: `Bearer ${token}`, 
  },
      });

      const data = await res.json();
      if (res.ok || res.status === 200) {
        setPosts(data);
      } else {
        setError("Failed to fetch posts");
      }
      setLoading(false);
    } catch (err) {
      console.error(err);
      setError("Something went wrong!");
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPosts();
  }, [token]);

  // Delete post
  const handleDelete = async (id: number) => {
    if (!window.confirm("Are you sure you want to delete this post?")) return;
    if (!token) return;
    try {
      const res = await fetch(`http://127.0.0.1:8000/api/blog/${id}/`, {
        method: "DELETE",
        headers: { Authorization: `Bearer ${token}` },
      });
      if (res.ok) {
        setPosts(posts.filter((post) => post.id !== id));
      } else {
        alert("Failed to delete post");
      }
    } catch (err) {
      console.error(err);
      alert("Something went wrong!");
    }
  };

  const openEditModal = (post: BlogPost) => {
    setCurrentEditPost(post);
    setShowEditModal(true);
  };

  if (loading) return <p className="text-center mt-20">Loading posts...</p>;

  return (
    <div className="flex min-h-screen bg-gray-100">
      {/* Sidebar */}
      <aside className="w-64 bg-white shadow-md p-6">
        <h2 className="text-xl font-bold mb-6">Dashboard</h2>
        <button
          onClick={() => setShowCreateModal(true)}
          className="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 transition mb-4"
        >
          Create New Post
        </button>
        <button
          onClick={() => {
            localStorage.removeItem("authToken");
            navigate("/login");
          }}
          className="w-full bg-red-500 text-white py-2 rounded-lg hover:bg-red-600 transition"
        >
          Logout
        </button>
      </aside>

      {/* Main content */}
      <main className="flex-1 p-6">
        <h1 className="text-2xl font-bold mb-6">My Blog Posts</h1>
        {error && <p className="text-red-500 mb-4">{error}</p>}
        {posts.length === 0 ? (
          <p>No posts yet. Click "Create New Post" to start blogging!</p>
        ) : (
          <div className="overflow-x-auto">
            <table className="min-w-full bg-white shadow-md rounded-lg overflow-hidden">
              <thead className="bg-gray-200">
                <tr>
                  <th className="py-3 px-6 text-left font-medium">Title</th>
                  <th className="py-3 px-6 text-left font-medium">Content</th>
                  <th className="py-3 px-6 text-center font-medium">Image</th>
                  <th className="py-3 px-6 text-center font-medium">Actions</th>
                </tr>
              </thead>
              <tbody>
                {posts.map((post) => (
                  <tr key={post.id} className="border-b hover:bg-gray-50">
                    <td className="py-3 px-6">{post.title}</td>
                    <td className="py-3 px-6">{post.content.slice(0, 50)}...</td>
                  <td className="py-3 px-6 text-center">
  {post.image ? (
    <img
      src={post.image.startsWith("http") 
        ? post.image // Already a full URL, use as-is
        : `http://127.0.0.1:8000${post.image}`} // Relative path from backend
      alt={post.title}
      className="w-16 h-16 object-cover mx-auto rounded"
    />
  ) : (
    <span className="text-gray-400">No image</span>
  )}
</td>
                    <td className="py-3 px-6 text-center space-x-2">
                      <button
                        onClick={() => openEditModal(post)}
                        className="bg-yellow-400 text-white px-3 py-1 rounded hover:bg-yellow-300 transition"
                      >
                        Edit
                      </button>
                      <button
                        onClick={() => handleDelete(post.id)}
                        className="bg-red-500 text-white px-3 py-1 rounded hover:bg-red-600 transition"
                      >
                        Delete
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </main>

      {/* Create Blog Modal */}
      {showCreateModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg shadow-lg w-full max-w-2xl p-6 relative">
            <button
              onClick={() => setShowCreateModal(false)}
              className="absolute top-3 right-3 text-gray-500 hover:text-gray-800 text-xl font-bold"
            >
              &times;
            </button>
            <BlogForm
              mode="create"
              token={token!}
              onSuccess={() => {
                setShowCreateModal(false);
                fetchPosts();
              }}
            />
          </div>
        </div>
      )}

      {/* Edit Blog Modal */}
      {showEditModal && currentEditPost && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg shadow-lg w-full max-w-2xl p-6 relative">
            <button
              onClick={() => setShowEditModal(false)}
              className="absolute top-3 right-3 text-gray-500 hover:text-gray-800 text-xl font-bold"
            >
              &times;
            </button>
            <BlogForm
              mode="edit"
              id={currentEditPost.id}
              token={token!}
              initialData={{
                title: currentEditPost.title,
                content: currentEditPost.content,
                image: currentEditPost.image || null,
              }}
              onSuccess={() => {
                setShowEditModal(false);
                fetchPosts();
              }}
            />
          </div>
        </div>
      )}
    </div>
  );
};

export default Dashboard;
