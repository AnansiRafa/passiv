import ReactMarkdown from "react-markdown";

export default function MD({ children }: { children: string }) {
  return (
    <ReactMarkdown
      components={{
        a: ({ node, ...props }) => (
          <a {...props} target="_blank" rel="nofollow sponsored">
            {props.children}
            <span className="ml-1 text-xs opacity-60">↗︎</span>
          </a>
        ),
      }}
    >
      {children}
    </ReactMarkdown>
  );
}