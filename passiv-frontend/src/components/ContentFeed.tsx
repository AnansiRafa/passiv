import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

interface ContentItem {
  id: number;
  version: number;
  timestamp: string;
  opportunity_name?: string;
  content?: string;
}

const ContentFeed = (): JSX.Element => {
  const [contentItems, setContentItems] = useState<ContentItem[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`${import.meta.env.VITE_API_BASE_URL}/api/content/`)
      .then((res) => res.json())
      .then((data) => setContentItems(data))
      .catch((err) => console.error("Failed to fetch content:", err))
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return <div className="text-center p-8">Loading content...</div>;
  }

  return (
    <div className="max-w-5xl mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-6 text-center">📚 Investment Insights</h1>
      <div className="grid gap-6">
        {contentItems.map((item) => (
          <div
            key={item.id}
            className="border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900 p-6 rounded-xl shadow hover:shadow-lg transition"
          >
            <Link to={`/content/${item.id}`}>
              <h2 className="text-xl font-semibold text-blue-600 hover:underline">
                {item.opportunity_name || "Untitled"}
              </h2>
            </Link>
            <div className="text-sm text-gray-500 mb-2">
              Version: v{item.version} • {new Date(item.timestamp).toLocaleDateString()}
            </div>
            <p className="text-gray-700 dark:text-gray-300 line-clamp-3">
              {item.content || "No content available."}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ContentFeed;
