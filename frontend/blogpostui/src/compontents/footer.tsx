// src/components/Footer.tsx
export default function Footer() {
  return (
    <footer className="bg-gradient-to-r from-indigo-700 to-blue-600 text-center py-6 mt-auto">
      <p className="text-gray-200">
        © {new Date().getFullYear()} MyBlog. All rights reserved.
      </p>
    </footer>
  );
}
