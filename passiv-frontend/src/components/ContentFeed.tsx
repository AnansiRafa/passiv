import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import { BASE_API_URL } from "../config";


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
    const fetchContent = async () => {
      try {
        const response = await fetch(`${BASE_API_URL}/api/content/`);
        const data = await response.json();
        console.log("Fetched data:", data); 
        setContentItems(data);
      } catch (error) {
        console.error("Failed to fetch content:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchContent();
  }, []);

  if (loading) {
    return <div className="text-center p-8 text-gray-500">Loading content...</div>;
  }

  return (
    <div className="p-8 max-w-6xl mx-auto">
      <h1 className="text-3xl font-bold mb-6 text-center">📚 Investment Insights</h1>
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
        {contentItems.map((item) => (
          <Link
            to={`/content/${item.id}`}
            key={item.id}
            className="block p-6 bg-white rounded-xl shadow hover:shadow-lg transition-all border border-gray-100"
          >
            <h2 className="text-xl font-semibold mb-2">{item.opportunity_name || "Untitled"}</h2>
            <p className="text-sm text-gray-600 mb-1">
              Version: v{item.version} • {new Date(item.timestamp).toLocaleDateString()}
            </p>
            <p className="text-sm text-gray-500 line-clamp-3">{item.content}</p>
          </Link>
        ))}
      </div>
    </div>
  );
};

export default ContentFeed;
