import { useState, ChangeEvent, FormEvent } from "react";

interface BlogFormProps {
  mode: "create" | "edit";
  id?: number;
  initialData?: {
    title: string;
    content: string;
    image?: string | null;
  };
  onSuccess: () => void;
  token: string;
}

const BlogForm: React.FC<BlogFormProps> = ({
  mode,
  id,
  initialData,
  onSuccess,
  token,
}) => {
  const [title, setTitle] = useState(initialData?.title || "");
  const [content, setContent] = useState(initialData?.content || "");
  const [image, setImage] = useState<File | null>(null);
  const [error, setError] = useState("");

  const handleFileChange = (e: ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) setImage(e.target.files[0]);
  };

  const handleSubmit = async (e: FormEvent) => {
  e.preventDefault();

  if (!title || !content) {
    setError("Title and content are required");
    return;
  }

  try {
    const url =
      mode === "create"
        ? "http://127.0.0.1:8000/api/blog/create/"
        : `http://127.0.0.1:8000/api/blog/${id}/`;
    const method = mode === "create" ? "POST" : "POST"; // ✅ allow POST for update too

    // Always use FormData
    const formData = new FormData();
    formData.append("title", title);
    formData.append("content", content);
    if (image) {
      formData.append("image", image);
    }

    const res = await fetch(url, {
      method,
      headers: {
        Authorization: `Bearer ${token}`,
        // ❌ Don’t set Content-Type, fetch will set it automatically for FormData
      },
      body: formData,
    });

    const data = await res.json();

    if (res.ok) {
      onSuccess();
    } else {
      setError(data.detail || data.error || "Something went wrong");
    }
  } catch (err) {
    console.error(err);
    setError("Something went wrong!");
  }
};

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {error && <p className="text-red-500">{error}</p>}

      <div>
        <label className="block text-sm font-medium text-gray-600">Title</label>
        <input
          type="text"
          className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          required
        />
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-600">Content</label>
        <textarea
          className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400"
          value={content}
          onChange={(e) => setContent(e.target.value)}
          required
        />
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-600">Image (optional)</label>
        <input type="file" accept="image/*" onChange={handleFileChange} />
      </div>

      <button
        type="submit"
        className="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 transition"
      >
        {mode === "create" ? "Create Post" : "Update Post"}
      </button>
    </form>
  );
};

export default BlogForm;
