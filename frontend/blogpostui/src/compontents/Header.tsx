import { useState } from "react";
import { motion } from "framer-motion";
import { Menu, X } from "lucide-react";
import { useNavigate, useLocation } from "react-router-dom";

interface NavItem {
  name: string;
  href: string;
  scrollTo?: boolean;
}

export default function Header() {
  const [menuOpen, setMenuOpen] = useState(false);
  const navigate = useNavigate();
  const location = useLocation();

  const navItems: NavItem[] = [
    { name: "Home", href: "/" },
    { name: "Posts", href: "/", scrollTo: true },
    { name: "Login", href: "/login" },
    { name: "Signup", href: "/signup" },
  ];

  const scrollToPosts = () => {
    const element = document.getElementById("posts");
    if (element) element.scrollIntoView({ behavior: "smooth", block: "start" });
  };

  const handlePostsClick = () => {
    if (location.pathname === "/") {
      scrollToPosts(); // already on homepage → just scroll
    } else {
      navigate("/"); // go to homepage first
      setTimeout(scrollToPosts, 100); // scroll after short delay
    }
    setMenuOpen(false);
  };

  return (
    <header>
      <nav className="bg-gradient-to-r from-blue-600 to-indigo-700 shadow-lg fixed w-full top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <h1 className="text-2xl font-bold text-white">MyBlog</h1>

            <div className="hidden md:flex space-x-8">
              {navItems.map((item) =>
                item.scrollTo ? (
                  <button
                    key={item.name}
                    onClick={handlePostsClick}
                    className="text-gray-200 hover:text-yellow-300 font-medium transition"
                  >
                    {item.name}
                  </button>
                ) : (
                  <a
                    key={item.name}
                    href={item.href}
                    className="text-gray-200 hover:text-yellow-300 font-medium transition"
                  >
                    {item.name}
                  </a>
                )
              )}
            </div>

            <div className="md:hidden">
              <button
                onClick={() => setMenuOpen(!menuOpen)}
                className="text-white hover:text-yellow-300"
                aria-label="Toggle menu"
              >
                {menuOpen ? <X size={28} /> : <Menu size={28} />}
              </button>
            </div>
          </div>
        </div>

        {menuOpen && (
          <div className="md:hidden bg-indigo-700 shadow-md">
            <div className="px-4 pt-2 pb-3 space-y-2">
              {navItems.map((item) =>
                item.scrollTo ? (
                  <button
                    key={item.name}
                    onClick={handlePostsClick}
                    className="block w-full text-left text-gray-200 hover:text-yellow-300 transition"
                  >
                    {item.name}
                  </button>
                ) : (
                  <a
                    key={item.name}
                    href={item.href}
                    onClick={() => setMenuOpen(false)}
                    className="block text-gray-200 hover:text-yellow-300 transition"
                  >
                    {item.name}
                  </a>
                )
              )}
            </div>
          </div>
        )}
      </nav>

      <div className="flex-grow bg-gradient-to-r from-blue-500 to-indigo-600 flex items-center justify-center text-center px-6 pt-20 pb-10">
        <motion.div
          initial={{ opacity: 0, y: 40 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="max-w-2xl"
        >
          <h1 className="text-4xl sm:text-6xl font-extrabold text-white mb-6">
            Welcome to <span className="text-yellow-300">MyBlog</span>
          </h1>
          <p className="text-lg sm:text-xl text-gray-100 mb-8">
            A place to share your thoughts, read amazing posts, and connect with
            others.
          </p>
          <div className="flex flex-wrap justify-center gap-4">
            <button
              onClick={handlePostsClick}
              className="px-6 py-3 rounded-full bg-yellow-400 text-gray-900 font-semibold shadow-md hover:bg-yellow-300 transition"
            >
              Explore Posts
            </button>
            <a
              href="/signup"
              className="px-6 py-3 rounded-full bg-white text-blue-600 font-semibold shadow-md hover:bg-gray-100 transition"
            >
              Get Started
            </a>
          </div>
        </motion.div>
      </div>
    </header>
  );
}
