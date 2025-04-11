import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";

interface ContentItem {
  id: number;
  version: number;
  timestamp: string;
  opportunity_name?: string;
  content?: string;
}

const ContentDetail = (): JSX.Element => {
  const { id } = useParams();
  const [contentItem, setContentItem] = useState<ContentItem | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchContent = async () => {
      try {
        const response = await fetch(`/api/content/${id}/`);
        if (!response.ok) {
          throw new Error("Failed to fetch content detail.");
        }
        const data = await response.json();
        setContentItem(data);
      } catch (err: any) {
        setError(err.message || "An error occurred.");
      } finally {
        setLoading(false);
      }
    };

    fetchContent();
  }, [id]);

  if (loading) {
    return <div className="p-8 text-center text-gray-500">Loading content...</div>;
  }

  if (error) {
    return <div className="p-8 text-center text-red-500">Error: {error}</div>;
  }

  if (!contentItem) {
    return <div className="p-8 text-center text-gray-400">Content not found.</div>;
  }

  return (
    <div className="p-8 max-w-3xl mx-auto">
      <Link to="/" className="text-blue-500 underline mb-4 block">
        ← Back to feed
      </Link>

      <h1 className="text-3xl font-bold mb-2">{contentItem.opportunity_name || "Untitled"}</h1>
      <p className="text-sm text-gray-600 mb-6">
        Version v{contentItem.version} • {new Date(contentItem.timestamp).toLocaleDateString()}
      </p>
      <article className="prose prose-lg max-w-none">
        {contentItem.content}
      </article>
    </div>
  );
};

export default ContentDetail;